"""Central configuration for the Vertex AI batch analysis pipeline."""

from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BATCH_DIR = Path(__file__).resolve().parent
REPO_ROOT = BATCH_DIR.parent  # Exp_Design/
OUTPUT_DIR = BATCH_DIR / "output"

DOCUMENT_CATALOG = REPO_ROOT.parent / "OSTI_retrieval" / "document_catalog.json"
OCR_DIR = REPO_ROOT.parent / "OSTI_OCR_Extracted" / "batch_output"
ALLOCATION_MATRIX_MD = REPO_ROOT / "CMM_Gold_QA_Allocation_Matrix.md"

# ---------------------------------------------------------------------------
# GCP / Vertex AI
# ---------------------------------------------------------------------------
GCP_PROJECT = "rcgenai"
GCP_REGION = "us-central1"
GCS_BUCKET = "fine_tuning_osti_docs"
GCS_INPUT_PREFIX = "batch_analysis/input"
GCS_OUTPUT_PREFIX = "batch_analysis/output"

GEMINI_MODEL = "gemini-2.5-pro"
TEMPERATURE = 0.2
MAX_OUTPUT_TOKENS = 4096

# ---------------------------------------------------------------------------
# Commodity categories (from document_catalog commodity_category values)
# ---------------------------------------------------------------------------
COMMODITY_CATEGORIES: list[str] = [
    "HREE",
    "CO",
    "LI",
    "GA",
    "GR",
    "LREE",
    "NI",
    "CU",
    "GE",
    "OTH",
]

# Display names for commodity codes
COMMODITY_DISPLAY: dict[str, str] = {
    "HREE": "Heavy Rare Earth Elements",
    "CO": "Cobalt",
    "LI": "Lithium",
    "GA": "Gallium",
    "GR": "Graphite",
    "LREE": "Light Rare Earth Elements",
    "NI": "Nickel",
    "CU": "Copper",
    "GE": "Germanium",
    "OTH": "Other (PGMs, Tungsten, Manganese, Titanium)",
}

# ---------------------------------------------------------------------------
# Subdomain categories
# ---------------------------------------------------------------------------
SUBDOMAIN_CATEGORIES: list[str] = [
    "T-EC",
    "T-PM",
    "T-GO",
    "Q-PS",
    "Q-TF",
    "Q-EP",
    "G-PR",
    "G-BM",
    "S-CC",
    "S-ST",
]

SUBDOMAIN_DISPLAY: dict[str, str] = {
    "T-EC": "Extraction Chemistry",
    "T-PM": "Processing Metallurgy",
    "T-GO": "Geological Occurrence",
    "Q-PS": "Production Statistics",
    "Q-TF": "Trade Flows",
    "Q-EP": "Economic Parameters",
    "G-PR": "Policy/Regulatory",
    "G-BM": "Bilateral/Multilateral",
    "S-CC": "Cross-Commodity",
    "S-ST": "Supply Chain Topology",
}

# Domain groupings
DOMAIN_GROUPS: dict[str, list[str]] = {
    "Technical": ["T-EC", "T-PM", "T-GO"],
    "Quantitative": ["Q-PS", "Q-TF", "Q-EP"],
    "Geopolitical": ["G-PR", "G-BM"],
    "Systemic": ["S-CC", "S-ST"],
}

# ---------------------------------------------------------------------------
# Mapping: document commodity_category -> relevant matrix commodities
# ---------------------------------------------------------------------------
# Commodity-specific papers evaluate all cells for that commodity.
# Subdomain-specific papers evaluate all 10 commodity cells in that subdomain.
CATEGORY_TO_COMMODITIES: dict[str, list[str]] = {cat: [cat] for cat in COMMODITY_CATEGORIES}

# Subdomain categories from document_catalog (prefixed with "subdomain_")
SUBDOMAIN_CATEGORY_PREFIX = "subdomain_"

# Complexity level display names
COMPLEXITY_LEVELS: dict[str, str] = {
    "L1": "Factual",
    "L2": "Relational",
    "L3": "Inferential",
    "L4": "Analytical",
}
