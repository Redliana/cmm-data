"""Parse CMM_Gold_QA_Allocation_Matrix.md into structured MatrixCell objects."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from config import (
    ALLOCATION_MATRIX_MD,
    COMMODITY_CATEGORIES,
    SUBDOMAIN_CATEGORIES,
    SUBDOMAIN_CATEGORY_PREFIX,
    SUBDOMAIN_DISPLAY,
    COMPLEXITY_LEVELS,
)


@dataclass
class MatrixCell:
    """One cell in the 100-question allocation matrix."""

    question_number: int
    cell_id: str  # e.g. "CMM-HREE-TEC-L1-001"
    commodity: str  # e.g. "HREE"
    subdomain: str  # e.g. "T-EC"
    complexity_level: str  # e.g. "L1"
    stratum: str  # "A" or "B"
    topic_focus: str  # e.g. "Primary REE separation method"

    @property
    def subdomain_display(self) -> str:
        return SUBDOMAIN_DISPLAY.get(self.subdomain, self.subdomain)

    @property
    def complexity_display(self) -> str:
        return COMPLEXITY_LEVELS.get(self.complexity_level, self.complexity_level)


# Regex for table rows in the detailed cell assignments sections.
# Matches: | Q# | CMM-...-... | COMMODITY | L# | A/B | Topic |
_ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|"  # Q#
    r"\s*(CMM-[A-Z0-9\-]+)\s*\|"  # cell ID
    r"\s*([A-Z]+)\s*\|"  # commodity
    r"\s*(L[1-4])\s*\|"  # level
    r"\s*([AB])\s*\|"  # stratum
    r"\s*(.+?)\s*\|$",  # topic focus
)

# Map cell-ID subdomain codes to canonical subdomain keys
_ID_SUBDOMAIN_MAP: dict[str, str] = {
    "TEC": "T-EC",
    "TPM": "T-PM",
    "TGO": "T-GO",
    "QPS": "Q-PS",
    "QTF": "Q-TF",
    "QEP": "Q-EP",
    "GPR": "G-PR",
    "GBM": "G-BM",
    "SCC": "S-CC",
    "SST": "S-ST",
}


def _extract_subdomain(cell_id: str) -> str:
    """Extract canonical subdomain from a cell ID like CMM-HREE-TEC-L1-001."""
    parts = cell_id.split("-")
    # The subdomain code is typically the 3rd segment (index 2),
    # but OTH cells can shift: CMM-OTH-GBM-L4-002
    for part in parts[2:]:
        if part in _ID_SUBDOMAIN_MAP:
            return _ID_SUBDOMAIN_MAP[part]
    raise ValueError(f"Cannot extract subdomain from cell ID: {cell_id}")


def parse_matrix(md_path: Path | None = None) -> list[MatrixCell]:
    """Parse the allocation matrix markdown into a list of 100 MatrixCells."""
    path = md_path or ALLOCATION_MATRIX_MD
    text = path.read_text(encoding="utf-8")

    cells: list[MatrixCell] = []
    for line in text.splitlines():
        m = _ROW_RE.match(line.strip())
        if not m:
            continue
        q_num = int(m.group(1))
        cell_id = m.group(2)
        commodity = m.group(3)
        level = m.group(4)
        stratum = m.group(5)
        topic = m.group(6)

        subdomain = _extract_subdomain(cell_id)

        cells.append(
            MatrixCell(
                question_number=q_num,
                cell_id=cell_id,
                commodity=commodity,
                subdomain=subdomain,
                complexity_level=level,
                stratum=stratum,
                topic_focus=topic,
            )
        )

    return cells


def get_relevant_cells(
    matrix: list[MatrixCell],
    commodity_category: str,
) -> list[MatrixCell]:
    """Return the matrix cells a paper should be evaluated against.

    - Commodity papers (HREE, CO, etc.) -> all cells for that commodity
      across all 10 subdomains.
    - Subdomain papers (subdomain_G-PR, etc.) -> all 10 commodity cells
      in that subdomain row.
    """
    if commodity_category.startswith(SUBDOMAIN_CATEGORY_PREFIX):
        subdomain = commodity_category[len(SUBDOMAIN_CATEGORY_PREFIX) :]
        return [c for c in matrix if c.subdomain == subdomain]
    else:
        return [c for c in matrix if c.commodity == commodity_category]


def matrix_to_dicts(matrix: list[MatrixCell]) -> list[dict]:
    """Serialize matrix cells to JSON-friendly dicts."""
    return [
        {
            "question_number": c.question_number,
            "cell_id": c.cell_id,
            "commodity": c.commodity,
            "subdomain": c.subdomain,
            "subdomain_display": c.subdomain_display,
            "complexity_level": c.complexity_level,
            "complexity_display": c.complexity_display,
            "stratum": c.stratum,
            "topic_focus": c.topic_focus,
        }
        for c in matrix
    ]


# ---------------------------------------------------------------------------
# CLI verification
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    cells = parse_matrix()
    print(f"Parsed {len(cells)} cells")

    # Verify commodity distribution
    from collections import Counter

    by_commodity = Counter(c.commodity for c in cells)
    print("\nBy commodity:")
    for k, v in sorted(by_commodity.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")

    by_subdomain = Counter(c.subdomain for c in cells)
    print("\nBy subdomain:")
    for k, v in sorted(by_subdomain.items()):
        print(f"  {k}: {v}")

    by_level = Counter(c.complexity_level for c in cells)
    print("\nBy complexity level:")
    for k, v in sorted(by_level.items()):
        print(f"  {k}: {v}")

    by_stratum = Counter(c.stratum for c in cells)
    print("\nBy stratum:")
    for k, v in sorted(by_stratum.items()):
        print(f"  {k}: {v}")

    # Verify relevant cells for a sample commodity and subdomain
    print("\n--- Relevant cells for HREE paper ---")
    hree_cells = get_relevant_cells(cells, "HREE")
    print(f"  {len(hree_cells)} cells")
    for c in hree_cells:
        print(f"    {c.cell_id} ({c.subdomain} {c.complexity_level})")

    print("\n--- Relevant cells for subdomain_G-PR paper ---")
    gpr_cells = get_relevant_cells(cells, "subdomain_G-PR")
    print(f"  {len(gpr_cells)} cells")
    for c in gpr_cells:
        print(f"    {c.cell_id} ({c.commodity} {c.complexity_level})")
