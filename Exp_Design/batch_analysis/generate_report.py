"""Generate a markdown recommendation report from parsed batch results.

Usage:
    python generate_report.py
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from config import (
    OUTPUT_DIR,
    COMMODITY_CATEGORIES,
    COMMODITY_DISPLAY,
    SUBDOMAIN_CATEGORIES,
    SUBDOMAIN_DISPLAY,
    DOMAIN_GROUPS,
    COMPLEXITY_LEVELS,
    DOCUMENT_CATALOG,
)
from matrix_parser import parse_matrix, MatrixCell


def _load_paper_titles() -> dict[str, str]:
    """Load OSTI ID -> title mapping from document catalog."""
    with open(DOCUMENT_CATALOG, encoding="utf-8") as f:
        docs = json.load(f)
    return {str(d["osti_id"]): d.get("title", "Unknown") for d in docs}


def _load_results() -> tuple[list[dict], dict[str, list[dict]], dict]:
    """Load paper_evaluations.json, recommendation_matrix.json, parse_stats.json."""
    evals_path = OUTPUT_DIR / "paper_evaluations.json"
    matrix_path = OUTPUT_DIR / "recommendation_matrix.json"
    stats_path = OUTPUT_DIR / "parse_stats.json"

    with open(evals_path, encoding="utf-8") as f:
        evaluations = json.load(f)
    with open(matrix_path, encoding="utf-8") as f:
        rec_matrix = json.load(f)
    with open(stats_path, encoding="utf-8") as f:
        stats = json.load(f)

    return evaluations, rec_matrix, stats


def _cell_lookup(matrix: list[MatrixCell]) -> dict[str, MatrixCell]:
    """Build cell_id -> MatrixCell lookup."""
    return {c.cell_id: c for c in matrix}


def generate_report() -> Path:
    """Generate the full recommendation report."""
    matrix = parse_matrix()
    cell_map = _cell_lookup(matrix)
    evaluations, rec_matrix, stats = _load_results()
    titles = _load_paper_titles()

    lines: list[str] = []

    def w(text: str = "") -> None:
        lines.append(text)

    # ---- Executive Summary ----
    w("# CMM Gold Q&A Paper Recommendation Report")
    w()
    w("## Executive Summary")
    w()

    total_papers = stats.get("parsed_ok", 0)
    recommended = stats.get("recommended_papers", 0)
    high_rel = stats.get("high_relevance_papers", 0)
    cells_covered = sum(
        1 for papers in rec_matrix.values()
        if any(p["relevance_score"] >= 3 for p in papers)
    )
    cells_strong = sum(
        1 for papers in rec_matrix.values()
        if any(p["relevance_score"] >= 4 for p in papers)
    )
    gap_count = 100 - cells_covered

    w(f"- **Papers evaluated**: {total_papers}")
    w(f"- **Papers recommended** (any cell score >= 4): {recommended}")
    w(f"- **High overall CMM relevance** (>= 4): {high_rel}")
    w(f"- **Matrix cells covered** (score >= 3): {cells_covered}/100")
    w(f"- **Strongly covered cells** (score >= 4): {cells_strong}/100")
    w(f"- **Gap cells** (no paper with score >= 3): {gap_count}")
    w()

    # ---- Coverage by Commodity ----
    w("## Coverage by Commodity")
    w()
    w("| Commodity | Papers Evaluated | Cells | Cells Covered (>=3) | Avg Top Score |")
    w("|-----------|-----------------|-------|--------------------|--------------| ")

    for comm in COMMODITY_CATEGORIES:
        comm_cells = [c for c in matrix if c.commodity == comm]
        comm_cell_ids = {c.cell_id for c in comm_cells}

        # Count papers that evaluated this commodity's cells
        paper_count = 0
        for ev in evaluations:
            ev_cells = {ce["cell_id"] for ce in ev.get("cell_evaluations", [])}
            if ev_cells & comm_cell_ids:
                paper_count += 1

        covered = 0
        top_scores: list[int] = []
        for cid in comm_cell_ids:
            papers = rec_matrix.get(cid, [])
            if papers:
                best = papers[0]["relevance_score"]
                top_scores.append(best)
                if best >= 3:
                    covered += 1

        avg_top = f"{sum(top_scores) / len(top_scores):.1f}" if top_scores else "N/A"
        w(f"| {COMMODITY_DISPLAY.get(comm, comm)} ({comm}) | {paper_count} | "
          f"{len(comm_cells)} | {covered} | {avg_top} |")

    w()

    # ---- Coverage by Subdomain ----
    w("## Coverage by Subdomain")
    w()
    w("| Subdomain | Cells | Cells Covered (>=3) | Avg Top Score |")
    w("|-----------|-------|--------------------|--------------| ")

    for sub in SUBDOMAIN_CATEGORIES:
        sub_cells = [c for c in matrix if c.subdomain == sub]
        sub_cell_ids = {c.cell_id for c in sub_cells}

        covered = 0
        top_scores = []
        for cid in sub_cell_ids:
            papers = rec_matrix.get(cid, [])
            if papers:
                best = papers[0]["relevance_score"]
                top_scores.append(best)
                if best >= 3:
                    covered += 1

        avg_top = f"{sum(top_scores) / len(top_scores):.1f}" if top_scores else "N/A"
        w(f"| {SUBDOMAIN_DISPLAY[sub]} ({sub}) | {len(sub_cells)} | {covered} | {avg_top} |")

    w()

    # ---- Cell-Level Recommendations ----
    w("## Cell-Level Recommendations")
    w()

    for domain_name, subdomains in DOMAIN_GROUPS.items():
        w(f"### {domain_name} Domain")
        w()

        for sub in subdomains:
            sub_cells = sorted(
                [c for c in matrix if c.subdomain == sub],
                key=lambda c: c.question_number,
            )

            w(f"#### {SUBDOMAIN_DISPLAY[sub]} ({sub})")
            w()

            for cell in sub_cells:
                cid = cell.cell_id
                papers = rec_matrix.get(cid, [])
                top_5 = papers[:5]

                w(f"**Q{cell.question_number}: {cid}**")
                w(f"- Commodity: {cell.commodity} | Level: {cell.complexity_display} ({cell.complexity_level}) | Stratum: {cell.stratum}")
                w(f"- Topic: {cell.topic_focus}")
                w()

                if not top_5:
                    w("*No papers evaluated for this cell.*")
                else:
                    w("| Rank | OSTI ID | Score | Title | Question Angle |")
                    w("|------|---------|-------|-------|---------------|")
                    for rank, p in enumerate(top_5, 1):
                        osti_id = p["osti_id"]
                        title = titles.get(osti_id, "Unknown")
                        # Truncate title if long
                        if len(title) > 60:
                            title = title[:57] + "..."
                        angle = p.get("suggested_question_angle", "")
                        if len(angle) > 60:
                            angle = angle[:57] + "..."
                        w(f"| {rank} | {osti_id} | {p['relevance_score']}/5 | {title} | {angle} |")

                w()

    # ---- Gap Analysis ----
    w("## Gap Analysis")
    w()
    w("Cells with no paper scoring >= 3 (need external sources or additional papers):")
    w()

    gap_cells = []
    for cell in sorted(matrix, key=lambda c: c.question_number):
        papers = rec_matrix.get(cell.cell_id, [])
        best_score = papers[0]["relevance_score"] if papers else 0
        if best_score < 3:
            gap_cells.append((cell, best_score))

    if not gap_cells:
        w("*No gaps -- all cells have at least one paper with relevance score >= 3.*")
    else:
        w(f"**{len(gap_cells)} cells** need additional source material:")
        w()
        w("| Q# | Cell ID | Commodity | Subdomain | Level | Topic | Best Score |")
        w("|----|---------|-----------|-----------|-------|-------|------------|")
        for cell, score in gap_cells:
            w(f"| Q{cell.question_number} | {cell.cell_id} | {cell.commodity} | "
              f"{cell.subdomain} | {cell.complexity_level} | {cell.topic_focus} | "
              f"{score}/5 |")
        w()

        # Group gaps by commodity
        gap_by_comm = defaultdict(list)
        for cell, score in gap_cells:
            gap_by_comm[cell.commodity].append(cell)

        w("### Gap Distribution by Commodity")
        w()
        for comm in COMMODITY_CATEGORIES:
            if comm in gap_by_comm:
                w(f"- **{comm}**: {len(gap_by_comm[comm])} cells -- "
                  f"{', '.join(c.subdomain + '/' + c.complexity_level for c in gap_by_comm[comm])}")

    w()
    w("---")
    w()
    w(f"*Report generated from {total_papers} paper evaluations across 100 matrix cells.*")

    # Write report
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = OUTPUT_DIR / "recommendation_report.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Report written to {report_path}")

    return report_path


def main() -> None:
    generate_report()


if __name__ == "__main__":
    main()
