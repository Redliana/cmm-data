# CMM Supply Chain Data Collection Session Log
**Date:** December 30, 2025
**Project:** CM2US Foundation Model Development - LLM Fine-Tuning Data Collection
**Location:** `/Users/wash198/Documents/Projects/Science_Projects/MPII_CMM/LLM_Fine_Tuning/Claude`

---

## Session Overview

This session focused on collecting training data for fine-tuning LLMs on Critical Minerals and Materials (CMM) supply chain knowledge. The work continued from a previous session and culminated in automated retrieval of DOE technical reports from OSTI.gov.

---

## Part 1: Previous Session Summary (Context)

### Initial Data Collection Completed

The following data sources were collected in the prior session:

| Source | Files | Size | Description |
|--------|-------|------|-------------|
| LISA Model (Vensim) | 12 CSVs | 380 KB | Lithium supply chain lookup tables from INL |
| USGS Mineral Commodities | 167 CSVs | 4.5 MB | 2023 Mineral Commodity Summaries |
| USGS Ore Deposits | 12 CSVs | 196 MB | National Geochemical Database |
| NETL REE & Coal | 388 CSVs | 7.3 GB | Geodatabase converted to CSV |

### Schema Documentation Generated

Three schema reference files were created in `schemas/`:
- `all_schemas.json` (7.8 MB) - Complete JSON schema
- `schema_summary.csv` (115 KB) - Quick-reference CSV
- `SCHEMA_REFERENCE.md` (42 KB) - Human-readable markdown

**Total:** 579 CSV files, 5.6M data rows documented

---

## Part 2: Current Session - OSTI.gov Document Retrieval

### User Request

> "Generate training examples from this data"

Initial task was to generate training examples, but user redirected to:

> "We need to retrieve more training data. Let's move on to OSTI.gov, where I hope we can automate retrieving full journal preprints based on specific criteria that I will provide to you. Start here: https://www.osti.gov/api/v1/docs"

### User Provided Experimental Design

User directed to methodology document:
```
/Users/wash198/Documents/Projects/Science_Projects/MPII_CMM/LLM_Fine_Tuning/Exp_Design/CMM_LLM_Baseline_Gold_QA_Methodology.md
```

This document specified:
- 10 priority commodities with weightings
- 10 sub-domains for evaluation
- 4 cognitive complexity levels
- Temporal stratification requirements

### OSTI API Investigation

**API Endpoint:** `https://www.osti.gov/api/v1/records`

**Key Parameters Identified:**
- `q` - General full-text search
- `has_fulltext` - Filter for documents with PDFs
- `title`, `author`, `subject` - Field-specific search
- `publication_date_start/end` - Date range filtering
- `rows`, `page` - Pagination

**Authentication:** None required
**Output Formats:** JSON, XML, BibTeX
**Full Text:** Available as PDF downloads via `links[rel="fulltext"]`

### Search Strategy Developed

Based on the CMM methodology, search queries were constructed for:

**10 Commodities (by priority weight):**
1. Heavy REE (Dy, Tb) - 15%
2. Cobalt - 12%
3. Lithium - 12%
4. Gallium - 10%
5. Graphite - 10%
6. Light REE (Nd, Pr) - 10%
7. Nickel - 8%
8. Copper - 8%
9. Germanium - 5%
10. Other (Mn, Ti, PGM, W) - 10%

**5 Sub-Domains:**
- T-EC: Extraction Chemistry
- T-PM: Processing Metallurgy
- T-GO: Geological Occurrence
- S-ST: Supply Chain Topology
- G-PR: Policy/Regulatory

### Retrieval Script Created

**File:** `OSTI_retrieval/osti_retrieval.py`

Key features:
- Automated search across all commodities and sub-domains
- PDF download with metadata preservation
- Deduplication via tracking file
- Rate limiting (1 second between requests)
- Error handling and retry logic
- Catalog export functionality

```python
# Usage examples:
python osti_retrieval.py --all --max-per-query 50
python osti_retrieval.py --commodity HREE --max-per-query 100
python osti_retrieval.py --subdomain T-EC
python osti_retrieval.py --catalog
```

### Virtual Environment Setup

Python virtual environment created due to Homebrew Python restrictions:
```bash
cd /Users/wash198/Documents/Projects/Science_Projects/MPII_CMM/LLM_Fine_Tuning/Claude
python3 -m venv .venv
source .venv/bin/activate
pip install requests
```

### Retrieval Execution

**Test Run:**
- Commodity: HREE
- Max per query: 5
- Result: 21 PDFs (59 MB) - Success

**Full Retrieval:**
- Started: 2025-12-30T12:53:33
- Completed: 2025-12-30T14:50:11
- Duration: ~2 hours

### Retrieval Results

**Summary Statistics:**
| Metric | Value |
|--------|-------|
| Queries Executed | 72 |
| Total Records Found | 3,566 |
| PDFs Downloaded | 1,112 |
| PDFs Skipped (duplicates) | 904 |
| Errors (503, timeouts) | 752 |
| Total Size | 6.2 GB |

**Results by Commodity:**

| Category | PDFs | Size | Priority Weight |
|----------|------|------|-----------------|
| HREE (Dy, Tb) | 155 | 608 MB | 15% |
| LREE (Nd, Pr) | 128 | 565 MB | 10% |
| Cobalt | 143 | 579 MB | 12% |
| Lithium | 115 | 569 MB | 12% |
| Gallium | 160 | 859 MB | 10% |
| Graphite | 70 | 461 MB | 10% |
| Nickel | 29 | 265 MB | 8% |
| Copper | 42 | 641 MB | 8% |
| Germanium | 29 | 92 MB | 5% |
| Other (Mn, Ti, PGM, W) | 51 | 383 MB | 10% |

**Results by Sub-Domain:**

| Sub-Domain | PDFs | Size |
|------------|------|------|
| T-EC (Extraction Chemistry) | 10 | 44 MB |
| T-PM (Processing Metallurgy) | 42 | 226 MB |
| T-GO (Geological Occurrence) | 30 | 213 MB |
| S-ST (Supply Chain Topology) | 57 | 214 MB |
| G-PR (Policy/Regulatory) | 51 | 523 MB |

### Output Directory Structure

```
OSTI_retrieval/
├── osti_retrieval.py           # Retrieval script
├── downloaded_ids.txt          # Tracking file (1,112 IDs)
├── document_catalog.json       # Full metadata catalog
├── retrieval_stats.json        # Execution statistics
└── pdfs/
    ├── HREE/                   # 155 PDFs + metadata
    ├── LREE/                   # 128 PDFs + metadata
    ├── CO/                     # 143 PDFs + metadata
    ├── LI/                     # 115 PDFs + metadata
    ├── GA/                     # 160 PDFs + metadata
    ├── GR/                     # 70 PDFs + metadata
    ├── NI/                     # 29 PDFs + metadata
    ├── CU/                     # 42 PDFs + metadata
    ├── GE/                     # 29 PDFs + metadata
    ├── OTH/                    # 51 PDFs + metadata
    ├── subdomain_T-EC/         # 10 PDFs + metadata
    ├── subdomain_T-PM/         # 42 PDFs + metadata
    ├── subdomain_T-GO/         # 30 PDFs + metadata
    ├── subdomain_S-ST/         # 57 PDFs + metadata
    └── subdomain_G-PR/         # 51 PDFs + metadata
```

### Known Issues and Notes

1. **503 Errors:** OSTI servers occasionally returned 503 (Service Unavailable). The script can be re-run to retry failed downloads.

2. **Patent Documents:** USPTO patent links returned 406 errors - these are not traditional preprints and were excluded.

3. **Rate Limiting:** 1-second delay between requests to be respectful to OSTI servers.

4. **Metadata Preservation:** Each PDF has a corresponding `*_metadata.json` file with full bibliographic information.

---

## Cumulative Data Collection Summary

| Source | Files | Size | Type |
|--------|-------|------|------|
| LISA Model | 12 | 380 KB | CSV (Vensim tables) |
| USGS Mineral Commodities | 167 | 4.5 MB | CSV |
| USGS Ore Deposits | 12 | 196 MB | CSV |
| NETL REE & Coal | 388 | 7.3 GB | CSV (from geodatabase) |
| OSTI Technical Reports | 1,112 | 6.2 GB | PDF |
| **TOTAL** | **1,691** | **~13.7 GB** | Mixed |

---

## Next Steps (Not Yet Started)

1. **Generate Training Examples:** Create Q&A pairs from collected data aligned with methodology
2. **PDF Text Extraction:** Convert OSTI PDFs to text for training
3. **Retry Failed Downloads:** Re-run OSTI script to capture 503 errors
4. **Additional Data Sources:** Consider other repositories (e.g., USGS publications, CRS reports)

---

## Files Created This Session

| File | Description |
|------|-------------|
| `OSTI_retrieval/osti_retrieval.py` | Automated retrieval script |
| `OSTI_retrieval/pdfs/*` | 1,112 PDF documents |
| `OSTI_retrieval/document_catalog.json` | Metadata catalog |
| `OSTI_retrieval/downloaded_ids.txt` | Download tracking |
| `OSTI_retrieval/retrieval_stats.json` | Execution statistics |
| `.venv/` | Python virtual environment |
| `session_log_2025-12-30.md` | This session log |

---

## Commands Reference

```bash
# Activate virtual environment
cd /Users/wash198/Documents/Projects/Science_Projects/MPII_CMM/LLM_Fine_Tuning/Claude
source .venv/bin/activate

# Run full retrieval
python OSTI_retrieval/osti_retrieval.py --all --max-per-query 50

# Retrieve specific commodity
python OSTI_retrieval/osti_retrieval.py --commodity HREE --max-per-query 100

# Retrieve specific subdomain
python OSTI_retrieval/osti_retrieval.py --subdomain T-EC

# Export catalog only
python OSTI_retrieval/osti_retrieval.py --catalog
```

---

*Session log generated by Claude Code (Opus 4.5)*
