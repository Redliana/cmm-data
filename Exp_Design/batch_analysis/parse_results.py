"""Download and parse Vertex AI batch output into structured recommendations.

Usage:
    python parse_results.py                          # download from GCS + parse
    python parse_results.py --local output/raw.jsonl  # parse a local file
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from pathlib import Path

from config import (
    GCP_PROJECT,
    GCS_BUCKET,
    GCS_OUTPUT_PREFIX,
    OUTPUT_DIR,
)


@dataclass
class CellScore:
    """Evaluation of one paper against one matrix cell."""

    cell_id: str
    relevance_score: int
    justification: str
    suggested_question_angle: str
    supports_l3_l4: bool


@dataclass
class PaperEvaluation:
    """Parsed evaluation for one paper."""

    osti_id: str
    overall_cmm_relevance: int
    depth_assessment: str
    cell_evaluations: list[CellScore]
    best_matching_cells: list[str]
    recommended_for_gold_qa: bool

    @property
    def max_cell_score(self) -> int:
        if not self.cell_evaluations:
            return 0
        return max(cs.relevance_score for cs in self.cell_evaluations)


def download_batch_output() -> Path:
    """Download batch output JSONL from GCS."""
    from google.cloud import storage

    client = storage.Client(project=GCP_PROJECT)
    bucket = client.bucket(GCS_BUCKET)

    # Find the output file(s) under the output prefix
    blobs = list(bucket.list_blobs(prefix=GCS_OUTPUT_PREFIX))
    jsonl_blobs = [b for b in blobs if b.name.endswith(".jsonl")]

    if not jsonl_blobs:
        raise FileNotFoundError(f"No JSONL files found at gs://{GCS_BUCKET}/{GCS_OUTPUT_PREFIX}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    local_path = OUTPUT_DIR / "batch_output_raw.jsonl"

    # If multiple output files, concatenate them
    with open(local_path, "w", encoding="utf-8") as out:
        for blob in sorted(jsonl_blobs, key=lambda b: b.name):
            print(f"Downloading gs://{GCS_BUCKET}/{blob.name} ...")
            content = blob.download_as_text(encoding="utf-8")
            out.write(content)
            if not content.endswith("\n"):
                out.write("\n")

    print(f"Downloaded to {local_path}")
    return local_path


def _salvage_truncated_json(text: str) -> dict | None:
    """Attempt to extract usable data from a truncated JSON response.

    When Gemini hits MAX_TOKENS, the JSON is cut mid-stream. We salvage
    by finding the last complete cell_evaluation object and reconstructing
    a valid JSON structure from what we have.
    """
    import re

    # Extract top-level fields that appear before cell_evaluations
    osti_match = re.search(r'"osti_id"\s*:\s*"([^"]*)"', text)
    relevance_match = re.search(r'"overall_cmm_relevance"\s*:\s*(\d+)', text)
    depth_match = re.search(r'"depth_assessment"\s*:\s*"((?:[^"\\]|\\.)*)"', text)

    if not osti_match:
        return None

    # Find complete cell_evaluation objects using a greedy approach:
    # Each complete object has all 5 required fields and ends with }
    cell_pattern = re.compile(
        r"\{\s*"
        r'"cell_id"\s*:\s*"([^"]*)"\s*,\s*'
        r'"relevance_score"\s*:\s*(\d+)\s*,\s*'
        r'"justification"\s*:\s*"((?:[^"\\]|\\.)*)"\s*,\s*'
        r'"suggested_question_angle"\s*:\s*"((?:[^"\\]|\\.)*)"\s*,\s*'
        r'"supports_l3_l4"\s*:\s*(true|false)\s*'
        r"\}",
        re.DOTALL,
    )

    cell_evals = []
    for m in cell_pattern.finditer(text):
        cell_evals.append(
            {
                "cell_id": m.group(1),
                "relevance_score": int(m.group(2)),
                "justification": m.group(3),
                "suggested_question_angle": m.group(4),
                "supports_l3_l4": m.group(5) == "true",
            }
        )

    if not cell_evals:
        return None

    best_cells = [ce["cell_id"] for ce in cell_evals if ce["relevance_score"] >= 4]

    return {
        "osti_id": osti_match.group(1),
        "overall_cmm_relevance": int(relevance_match.group(1)) if relevance_match else 0,
        "depth_assessment": depth_match.group(1) if depth_match else "",
        "cell_evaluations": cell_evals,
        "best_matching_cells": best_cells,
        "recommended_for_gold_qa": len(best_cells) > 0,
    }


def parse_response_line(line: str) -> tuple[PaperEvaluation | None, bool]:
    """Parse one line of batch output into a PaperEvaluation.

    Returns (evaluation, was_salvaged). was_salvaged=True means the response
    was truncated but we recovered partial cell evaluations.
    """
    try:
        data = json.loads(line)
    except json.JSONDecodeError:
        return None, False

    # Vertex AI batch output structure:
    # {"response": {"candidates": [{"content": {"parts": [{"text": "..."}]}}]}}
    response = data.get("response", {})
    candidates = response.get("candidates", [])
    if not candidates:
        return None, False

    content = candidates[0].get("content", {})
    parts = content.get("parts", [])
    if not parts:
        return None, False

    text = parts[0].get("text", "")
    salvaged = False

    try:
        result = json.loads(text)
    except json.JSONDecodeError:
        # Attempt to salvage truncated JSON (MAX_TOKENS cutoff)
        result = _salvage_truncated_json(text)
        if result is None:
            return None, False
        salvaged = True

    cell_evaluations = []
    for ce in result.get("cell_evaluations", []):
        cell_evaluations.append(
            CellScore(
                cell_id=ce.get("cell_id", ""),
                relevance_score=int(ce.get("relevance_score", 0)),
                justification=ce.get("justification", ""),
                suggested_question_angle=ce.get("suggested_question_angle", ""),
                supports_l3_l4=bool(ce.get("supports_l3_l4", False)),
            )
        )

    return PaperEvaluation(
        osti_id=str(result.get("osti_id", "")),
        overall_cmm_relevance=int(result.get("overall_cmm_relevance", 0)),
        depth_assessment=result.get("depth_assessment", ""),
        cell_evaluations=cell_evaluations,
        best_matching_cells=result.get("best_matching_cells", []),
        recommended_for_gold_qa=bool(result.get("recommended_for_gold_qa", False)),
    ), salvaged


def build_recommendation_matrix(
    evaluations: list[PaperEvaluation],
) -> dict[str, list[dict]]:
    """Map each cell_id -> list of (osti_id, score, justification, angle) sorted by score."""
    matrix: dict[str, list[dict]] = defaultdict(list)

    for ev in evaluations:
        for cs in ev.cell_evaluations:
            matrix[cs.cell_id].append(
                {
                    "osti_id": ev.osti_id,
                    "relevance_score": cs.relevance_score,
                    "justification": cs.justification,
                    "suggested_question_angle": cs.suggested_question_angle,
                    "supports_l3_l4": cs.supports_l3_l4,
                    "overall_cmm_relevance": ev.overall_cmm_relevance,
                }
            )

    # Sort each cell's papers by relevance_score descending
    for cell_id in matrix:
        matrix[cell_id].sort(key=lambda x: x["relevance_score"], reverse=True)

    return dict(matrix)


def parse_batch_results(local_path: Path) -> tuple[list[PaperEvaluation], dict]:
    """Parse all results from a batch output JSONL file.

    Returns (evaluations, stats_dict).
    """
    evaluations: list[PaperEvaluation] = []
    stats = {
        "total_lines": 0,
        "parsed_ok": 0,
        "salvaged": 0,
        "salvaged_cells": 0,
        "parse_failures": 0,
        "recommended_papers": 0,
        "high_relevance_papers": 0,  # overall >= 4
    }

    with open(local_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            stats["total_lines"] += 1

            ev, salvaged = parse_response_line(line)
            if ev is None:
                stats["parse_failures"] += 1
                continue

            stats["parsed_ok"] += 1
            if salvaged:
                stats["salvaged"] += 1
                stats["salvaged_cells"] += len(ev.cell_evaluations)
            evaluations.append(ev)

            if ev.recommended_for_gold_qa:
                stats["recommended_papers"] += 1
            if ev.overall_cmm_relevance >= 4:
                stats["high_relevance_papers"] += 1

    return evaluations, stats


def save_results(
    evaluations: list[PaperEvaluation],
    rec_matrix: dict[str, list[dict]],
    stats: dict,
) -> None:
    """Save parsed results to JSON files."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Paper evaluations
    evals_path = OUTPUT_DIR / "paper_evaluations.json"
    evals_data = []
    for ev in evaluations:
        d = {
            "osti_id": ev.osti_id,
            "overall_cmm_relevance": ev.overall_cmm_relevance,
            "depth_assessment": ev.depth_assessment,
            "cell_evaluations": [asdict(cs) for cs in ev.cell_evaluations],
            "best_matching_cells": ev.best_matching_cells,
            "recommended_for_gold_qa": ev.recommended_for_gold_qa,
        }
        evals_data.append(d)

    with open(evals_path, "w", encoding="utf-8") as f:
        json.dump(evals_data, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(evals_data)} evaluations to {evals_path}")

    # Recommendation matrix
    matrix_path = OUTPUT_DIR / "recommendation_matrix.json"
    with open(matrix_path, "w", encoding="utf-8") as f:
        json.dump(rec_matrix, f, indent=2, ensure_ascii=False)
    print(f"Saved recommendation matrix ({len(rec_matrix)} cells) to {matrix_path}")

    # Parse stats
    stats_path = OUTPUT_DIR / "parse_stats.json"
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
    print(f"Saved parse stats to {stats_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Parse Vertex AI batch output into recommendations"
    )
    parser.add_argument(
        "--local",
        type=str,
        help="Parse a local JSONL file instead of downloading from GCS",
    )
    args = parser.parse_args()

    if args.local:
        local_path = Path(args.local)
    else:
        local_path = download_batch_output()

    if not local_path.exists():
        print(f"File not found: {local_path}")
        return

    print(f"Parsing {local_path} ...")
    evaluations, stats = parse_batch_results(local_path)

    print(f"\n--- Parse Stats ---")
    print(f"Total lines: {stats['total_lines']}")
    print(f"Parsed OK: {stats['parsed_ok']}")
    print(f"  Complete: {stats['parsed_ok'] - stats['salvaged']}")
    print(
        f"  Salvaged (truncated): {stats['salvaged']} ({stats['salvaged_cells']} cells recovered)"
    )
    print(f"Parse failures: {stats['parse_failures']}")
    print(f"Recommended papers: {stats['recommended_papers']}")
    print(f"High relevance (>=4): {stats['high_relevance_papers']}")

    # Build recommendation matrix
    rec_matrix = build_recommendation_matrix(evaluations)

    # Coverage check
    cells_with_papers = sum(
        1 for papers in rec_matrix.values() if any(p["relevance_score"] >= 3 for p in papers)
    )
    print(f"\nCells with at least one score>=3 paper: {cells_with_papers}/100")

    save_results(evaluations, rec_matrix, stats)


if __name__ == "__main__":
    main()
