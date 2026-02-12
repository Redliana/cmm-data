"""Generate Vertex AI batch input JSONL from document catalog + allocation matrix.

Each line is one GenerateContentRequest for a single paper, asking Gemini to
evaluate the paper against its relevant matrix cells.

Usage:
    python prepare_batch.py              # write output/batch_input.jsonl
    python prepare_batch.py --dry-run    # print stats without writing
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from config import (
    COMMODITY_DISPLAY,
    DOCUMENT_CATALOG,
    MAX_OUTPUT_TOKENS,
    OCR_DIR,
    OUTPUT_DIR,
    SUBDOMAIN_CATEGORY_PREFIX,
    SUBDOMAIN_DISPLAY,
    TEMPERATURE,
)
from matrix_parser import MatrixCell, get_relevant_cells, parse_matrix

# ---------------------------------------------------------------------------
# Structured output schema (Vertex AI responseSchema)
# ---------------------------------------------------------------------------
RESPONSE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "osti_id": {"type": "STRING"},
        "overall_cmm_relevance": {
            "type": "INTEGER",
            "description": "1-5 scale: 1=no CMM relevance, 5=highly relevant with deep CMM content",
        },
        "depth_assessment": {
            "type": "STRING",
            "description": "Brief assessment of the paper's depth and specificity for CMM topics",
        },
        "cell_evaluations": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "cell_id": {"type": "STRING"},
                    "relevance_score": {
                        "type": "INTEGER",
                        "description": "1-5: how well this paper supports creating a gold Q&A for this cell",
                    },
                    "justification": {
                        "type": "STRING",
                        "description": "Why this score; what specific content maps to this cell",
                    },
                    "suggested_question_angle": {
                        "type": "STRING",
                        "description": "A specific question angle this paper could support for this cell",
                    },
                    "supports_l3_l4": {
                        "type": "BOOLEAN",
                        "description": "Whether the paper has enough depth for L3/L4 complexity questions",
                    },
                },
                "required": [
                    "cell_id",
                    "relevance_score",
                    "justification",
                    "suggested_question_angle",
                    "supports_l3_l4",
                ],
            },
        },
        "best_matching_cells": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Cell IDs where this paper scored >= 4",
        },
        "recommended_for_gold_qa": {
            "type": "BOOLEAN",
            "description": "True if any cell_evaluation has relevance_score >= 4",
        },
    },
    "required": [
        "osti_id",
        "overall_cmm_relevance",
        "depth_assessment",
        "cell_evaluations",
        "best_matching_cells",
        "recommended_for_gold_qa",
    ],
}

# ---------------------------------------------------------------------------
# System instruction
# ---------------------------------------------------------------------------
SYSTEM_INSTRUCTION = """\
You are an expert analyst specializing in critical minerals and materials (CMM) \
supply chains, with deep knowledge of extraction chemistry, processing metallurgy, \
geology, trade flows, economic parameters, policy/regulatory frameworks, and \
supply chain topology.

Your task is to evaluate whether a given research paper is suitable for creating \
gold-standard evaluation Q&A pairs for a CMM knowledge benchmark. You will be \
given the paper's metadata (title, abstract, authors, subjects) and a set of \
specific matrix cells from a 100-question allocation matrix.

For each matrix cell, assess how well the paper's content could support creating \
a high-quality question-answer pair at the specified complexity level and topic.

Scoring guide (relevance_score 1-5):
- 5: Paper directly and deeply addresses this cell's topic; could be primary source
- 4: Paper substantially covers this topic; strong supporting source
- 3: Paper has moderate relevance; partial coverage of the topic
- 2: Paper has tangential relevance; minor supporting information
- 1: Paper has no meaningful connection to this cell's topic

For L3 (Inferential) and L4 (Analytical) cells, the paper needs sufficient depth \
for multi-step reasoning or synthesis questions. set supports_l3_l4=true only if \
the paper goes beyond surface-level coverage."""


def _format_cells_for_prompt(cells: list[MatrixCell]) -> str:
    """Format matrix cells into a numbered list for the prompt."""
    lines = []
    for i, c in enumerate(cells, 1):
        lines.append(
            f"{i}. Cell {c.cell_id}\n"
            f"   Subdomain: {c.subdomain_display} ({c.subdomain})\n"
            f"   Complexity: {c.complexity_display} ({c.complexity_level})\n"
            f"   Topic: {c.topic_focus}"
        )
    return "\n".join(lines)


def _get_category_label(commodity_category: str) -> str:
    """Human-readable label for a commodity_category value."""
    if commodity_category.startswith(SUBDOMAIN_CATEGORY_PREFIX):
        sub = commodity_category[len(SUBDOMAIN_CATEGORY_PREFIX) :]
        return f"Subdomain: {SUBDOMAIN_DISPLAY.get(sub, sub)} ({sub})"
    return f"Commodity: {COMMODITY_DISPLAY.get(commodity_category, commodity_category)} ({commodity_category})"


def _try_ocr_abstract(osti_id: str) -> str | None:
    """Attempt to load an OCR-extracted abstract for papers missing descriptions.

    Falls back to the first ~500 characters of OCR full text if the abstract
    field is empty (common for OCR-processed files).
    """
    ocr_path = OCR_DIR / f"{osti_id}.json"
    if not ocr_path.exists():
        return None
    try:
        data = json.loads(ocr_path.read_text(encoding="utf-8"))
        abstract = (data.get("abstract") or "").strip()
        if abstract:
            return abstract

        # Fall back to truncated full text
        text = (data.get("text") or "").strip()
        if text:
            # Skip common boilerplate headers/disclaimers, take meaningful text
            # Truncate to ~500 chars at a sentence boundary
            snippet = text[:600]
            last_period = snippet.rfind(".")
            if last_period > 200:
                snippet = snippet[: last_period + 1]
            return snippet
    except (json.JSONDecodeError, KeyError):
        pass
    return None


def build_user_prompt(doc: dict, cells: list[MatrixCell]) -> tuple[str, bool]:
    """Build the user prompt for one paper. Returns (prompt_text, limited_metadata)."""
    osti_id = doc["osti_id"]
    title = doc.get("title", "Unknown")
    description = (doc.get("description") or "").strip()
    authors = doc.get("authors", [])
    subjects = doc.get("subjects", [])
    pub_date = doc.get("publication_date", "Unknown")
    commodity_category = doc.get("commodity_category", "Unknown")

    limited_metadata = False

    # Handle empty abstracts with OCR fallback
    if not description:
        ocr_abstract = _try_ocr_abstract(str(osti_id))
        if ocr_abstract:
            description = ocr_abstract
            abstract_source = "(abstract recovered from OCR extraction)"
        else:
            limited_metadata = True
            abstract_source = (
                "(no abstract available -- evaluation based on title and subjects only)"
            )
    else:
        abstract_source = ""

    authors_str = "; ".join(authors[:5])
    if len(authors) > 5:
        authors_str += f" (and {len(authors) - 5} more)"

    subjects_str = "; ".join(subjects) if subjects else "None listed"
    category_label = _get_category_label(commodity_category)

    cells_text = _format_cells_for_prompt(cells)

    prompt = f"""\
Evaluate this paper for creating gold-standard CMM evaluation Q&A pairs.

**Paper Metadata:**
- OSTI ID: {osti_id}
- Title: {title}
- Authors: {authors_str}
- Publication Date: {pub_date}
- Category: {category_label}
- Subjects: {subjects_str}

**Abstract:** {abstract_source}
{description}

{"**NOTE: Limited metadata available. Score conservatively.**" if limited_metadata else ""}

**Evaluate against these {len(cells)} matrix cells:**

{cells_text}

Provide your evaluation with a relevance_score (1-5) for each cell, justification, \
suggested question angle, and whether the paper supports L3/L4 complexity."""

    return prompt, limited_metadata


def build_request(doc: dict, cells: list[MatrixCell]) -> dict:
    """Build a single Vertex AI GenerateContentRequest in camelCase JSONL format."""
    prompt_text, _ = build_user_prompt(doc, cells)

    return {
        "request": {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt_text}],
                }
            ],
            "systemInstruction": {
                "parts": [{"text": SYSTEM_INSTRUCTION}],
            },
            "generationConfig": {
                "temperature": TEMPERATURE,
                "maxOutputTokens": MAX_OUTPUT_TOKENS,
                "responseMimeType": "application/json",
                "responseSchema": RESPONSE_SCHEMA,
            },
        }
    }


def prepare_batch(
    dry_run: bool = False,
) -> Path | None:
    """Generate the batch input JSONL file.

    Returns the output path, or None if dry_run.
    """
    # Load matrix
    matrix = parse_matrix()
    print(f"Parsed {len(matrix)} matrix cells")

    # Load document catalog
    with open(DOCUMENT_CATALOG, encoding="utf-8") as f:
        docs = json.load(f)
    print(f"Loaded {len(docs)} documents from catalog")

    # Stats tracking
    stats: dict[str, int] = Counter()
    cell_counts: dict[str, int] = Counter()
    requests: list[dict] = []

    for doc in docs:
        osti_id = doc["osti_id"]
        category = doc.get("commodity_category", "")

        # Get relevant cells
        cells = get_relevant_cells(matrix, category)
        if not cells:
            stats["no_relevant_cells"] += 1
            continue

        cell_counts[category] += 1
        stats["total_requests"] += 1

        has_description = bool((doc.get("description") or "").strip())
        if not has_description:
            ocr_abstract = _try_ocr_abstract(str(osti_id))
            if ocr_abstract:
                stats["ocr_fallback"] += 1
            else:
                stats["limited_metadata"] += 1
        else:
            stats["has_abstract"] += 1

        if not dry_run:
            request = build_request(doc, cells)
            requests.append(request)

    # Print stats
    print(f"\n--- Batch Preparation Stats ---")
    print(f"Total requests: {stats.get('total_requests', 0)}")
    print(f"  With abstract: {stats.get('has_abstract', 0)}")
    print(f"  OCR fallback: {stats.get('ocr_fallback', 0)}")
    print(f"  Limited metadata: {stats.get('limited_metadata', 0)}")
    print(f"  No relevant cells (skipped): {stats.get('no_relevant_cells', 0)}")

    print(f"\nDocuments per category:")
    for cat, count in sorted(cell_counts.items(), key=lambda x: -x[1]):
        cells = get_relevant_cells(matrix, cat)
        print(f"  {cat}: {count} docs x {len(cells)} cells each")

    if dry_run:
        print("\n[DRY RUN] No output written.")
        return None

    # Write JSONL
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "batch_input.jsonl"

    with open(output_path, "w", encoding="utf-8") as f:
        for req in requests:
            f.write(json.dumps(req, ensure_ascii=False) + "\n")

    print(f"\nWrote {len(requests)} requests to {output_path}")

    # Estimate token cost
    total_bytes = output_path.stat().st_size
    est_input_tokens = total_bytes // 4  # rough estimate
    est_output_tokens = len(requests) * 800  # ~800 tokens per structured response
    est_cost = (est_input_tokens * 1.25 / 1_000_000) + (est_output_tokens * 5.0 / 1_000_000)
    print(f"\nEstimated tokens: ~{est_input_tokens:,} input, ~{est_output_tokens:,} output")
    print(f"Estimated batch cost (50% discount): ~${est_cost:.2f}")

    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Vertex AI batch input JSONL")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print stats without writing output",
    )
    args = parser.parse_args()
    prepare_batch(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
