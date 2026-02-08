# CMM Data Sources: API and MCP Availability Analysis

**Purpose:** Identify programmatic access pathways for Gold Q&A source document retrieval  
**Date:** December 21, 2025

---

## Executive Summary

From our prioritized source list, I have identified the following programmatic access landscape:

| Access Type | Count | Sources |
|-------------|-------|---------|
| **REST API (documented)** | 4 | UN Comtrade, OpenMindat, IEA (limited), EIA |
| **Bulk CSV/Data Release** | 5 | USGS MCS, USGS MRDS, CMI Models, NREL LIBRA, ICMM |
| **GitHub Repositories** | 4 | CMI DREEM/CoCuNi/LISA, NREL LIBRA, OpenMindat packages |
| **MCP Servers (existing)** | 2 | Materials Project (not CMM-specific), Data Commons |
| **MCP Servers (buildable)** | 3-4 | UN Comtrade, OpenMindat, USGS (potential) |
| **No programmatic access** | 3 | LANL SAFE, ANL BatPaC/GREET, Columbia Monitor |

---

## 1. Sources with Documented REST APIs

### 1.1 UN Comtrade API ★★★★★

| Attribute | Detail |
|-----------|--------|
| **API Type** | REST API with JSON responses |
| **Authentication** | API key required (free registration) |
| **Rate Limits** | 500 calls/day with key; 100,000 records/call |
| **Documentation** | https://comtradeplus.un.org/; R package `comtradr` |
| **Python Package** | Available via `comtradeapicall` |
| **R Package** | `comtradr` (CRAN) — well-documented |
| **MCP Potential** | High — structured API ideal for MCP wrapper |

**Relevance to Gold Q&A:** Trade flows (Q-TF), bilateral relationships (G-BM)

**Sample Query (R):**
```r
library(comtradr)
ct_get_data(
  commodity_code = "2846",  # Rare earth compounds
  reporter = "CHN",
  partner = "USA",
  start_date = "2023",
  end_date = "2023"
)
```

**HS Codes for CMM (per UNCTAD mapping):**
- REE: 2846 (RE compounds), 280530 (RE metals)
- Lithium: 253090, 283691 (ores/carbonate), 282520 (hydroxide)
- Cobalt: 8105 (Co and articles), 282200 (Co oxides)
- Graphite: 250410 (natural), 380110 (artificial)
- Gallium: 811292
- Germanium: 811292

---

### 1.2 OpenMindat API ★★★★☆

| Attribute | Detail |
|-----------|--------|
| **API Type** | REST API |
| **Authentication** | API key (free with Mindat account, "data contributor" status) |
| **Documentation** | https://api.mindat.org/schema/redoc/ |
| **Python Package** | `openmindat` (PyPI) |
| **R Package** | `OpenMindat` (CRAN) |
| **MCP Potential** | High — already has structured client packages |

**Relevance to Gold Q&A:** Geological occurrence (T-GO), mineral properties (T-EC)

**Endpoints:**
- `/geomaterials/` — mineral species with properties
- `/localities/` — occurrence locations
- `/ima/` — IMA-approved mineral list

**Sample Query (Python):**
```python
from openmindat import MindatApi
api = MindatApi("YOUR_API_KEY")
results = api.get_geomaterials(elements=["Dy", "Tb"])
```

---

### 1.3 IEA Critical Minerals Data Explorer ★★★☆☆

| Attribute | Detail |
|-----------|--------|
| **API Type** | Limited — primarily interactive web tool |
| **Bulk Download** | Some CSV exports available |
| **Documentation** | https://www.iea.org/data-and-statistics/data-tools/critical-minerals-data-explorer |
| **MCP Potential** | Low — would require scraping |

**Relevance to Gold Q&A:** Demand projections (Q-EP, S-CC)

**Access Method:** Manual export from web interface; no documented programmatic API.

---

### 1.4 EIA API ★★★★☆

| Attribute | Detail |
|-----------|--------|
| **API Type** | REST API |
| **Authentication** | API key (free registration) |
| **Documentation** | https://www.eia.gov/opendata/ |
| **Coverage** | Coal, energy — limited CMM relevance |
| **MCP Potential** | Medium — existing API could be wrapped |

**Relevance to Gold Q&A:** Limited (coal sector context only)

---

## 2. Sources with Bulk Data Downloads (No API)

### 2.1 USGS Mineral Commodity Summaries ★★★★★

| Attribute | Detail |
|-----------|--------|
| **Access Type** | Annual data releases in CSV format |
| **Location** | https://www.usgs.gov/centers/national-minerals-information-center/data |
| **Format** | CSV tables + PDF reports |
| **Update Frequency** | Annual (January release) |
| **MCP Potential** | Medium — would require file parsing |

**Available Data Releases:**
- `mcs2025-data-tables.zip` — structured CSV of all commodity statistics
- Individual commodity PDFs with embedded tables

**Relevance to Gold Q&A:** Primary source for Q-PS, Q-TF, Q-EP (35-40 questions)

---

### 2.2 USGS Mineral Resources Data System (MRDS) ★★★★☆

| Attribute | Detail |
|-----------|--------|
| **Access Type** | Bulk download (shapefile, CSV) |
| **Location** | https://mrdata.usgs.gov/mrds/ |
| **Format** | CSV, Shapefile, Geodatabase |
| **MCP Potential** | Medium — geospatial data requires preprocessing |

**Relevance to Gold Q&A:** Geological occurrence (T-GO)

---

### 2.3 CMI System Dynamics Models (DREEM, CoCuNi, LISA) ★★★★☆

| Attribute | Detail |
|-----------|--------|
| **Access Type** | GitHub repositories |
| **Locations** | https://github.com/IdahoLabResearch/DREEM; https://github.com/CMI-Hub |
| **Format** | Vensim models (.mdl), CSV data files |
| **MCP Potential** | Low — model files require Vensim; CSV data accessible |

**Relevance to Gold Q&A:** System dynamics validation (Q-PS, S-CC)

---

### 2.4 NREL LIBRA ★★★☆☆

| Attribute | Detail |
|-----------|--------|
| **Access Type** | GitHub repository |
| **Location** | https://github.com/NREL/LIBRA |
| **Format** | Model data tables, CSV |
| **MCP Potential** | Low |

**Relevance to Gold Q&A:** Battery supply chain (S-CC)

---

### 2.5 ICMM Global Mining Dataset ★★★☆☆

| Attribute | Detail |
|-----------|--------|
| **Access Type** | Zenodo bulk download |
| **Location** | https://zenodo.org/records/ICMM (search required) |
| **Format** | CSV |
| **Coverage** | 8,508 mines/facilities, 47 commodities |
| **MCP Potential** | Low — static dataset |

**Relevance to Gold Q&A:** Supply chain topology (S-ST)

---

## 3. Sources Requiring Manual Access

### 3.1 LANL SAFE Database ★★★★☆ (for T-EC)

| Attribute | Detail |
|-----------|--------|
| **Access Type** | Web interface with query forms |
| **Location** | https://safe.lanl.gov |
| **Format** | Tabular results (exportable) |
| **API** | None documented |
| **MCP Potential** | Would require scraping or collaboration with LANL |

**Relevance to Gold Q&A:** Critical for REE separation chemistry (T-EC)

**Workaround:** Manual query and export of f-element separation data.

---

### 3.2 Argonne BatPaC / GREET ★★★☆☆

| Attribute | Detail |
|-----------|--------|
| **Access Type** | Excel model download |
| **Locations** | https://www.anl.gov/cse/batpac-battery-manufacturing-cost-estimation; https://greet.anl.gov/ |
| **Format** | Excel (.xlsx) with embedded calculations |
| **API** | None |
| **MCP Potential** | Low — would require Excel parsing |

**Relevance to Gold Q&A:** Battery material intensity (T-PM, S-CC)

---

### 3.3 Columbia Critical Materials Monitor ★★★☆☆

| Attribute | Detail |
|-----------|--------|
| **Access Type** | Interactive web visualization |
| **Location** | https://criticalmaterials.energypolicy.columbia.edu/ |
| **API** | None — data derived from UN Comtrade |
| **MCP Potential** | Low — better to use underlying UN Comtrade API |

**Relevance to Gold Q&A:** Already curated HS code mappings useful as reference

---

## 4. Existing MCP Servers (Potentially Relevant)

### 4.1 Materials Project MCP Server ★★☆☆☆

| Attribute | Detail |
|-----------|--------|
| **Repository** | https://github.com/pathintegral-institute/mcp.science |
| **Function** | Query Materials Project database for crystal structures, band gaps, formation energies |
| **Relevance** | Limited — focused on computed materials properties, not supply chain |
| **Use Case** | Could support materials science questions but not CMM supply chain |

### 4.2 Google Data Commons MCP Server ★★★☆☆

| Attribute | Detail |
|-----------|--------|
| **Repository** | PyPI: `datacommons-mcp` |
| **Function** | Access to statistical data across many domains |
| **Relevance** | Medium — may have some minerals/energy data but not CMM-specific |

---

## 5. MCP Development Opportunities

Based on available APIs, the following MCP servers could be developed to support Gold Q&A construction:

### 5.1 UN Comtrade MCP Server (Recommended) ★★★★★

**Justification:** Well-documented API with R/Python packages; high CMM relevance for trade flow questions.

**Implementation:**
```python
from mcp.server.fastmcp import FastMCP
import comtradeapicall

mcp = FastMCP("UN Comtrade CMM Server")

@mcp.tool()
async def get_cmm_trade_flows(
    commodity_hs: str,
    reporter: str,
    partner: str,
    year: int
) -> dict:
    """Query bilateral trade flows for critical minerals."""
    # Implementation using comtradeapicall
    ...
```

### 5.2 OpenMindat MCP Server (Feasible) ★★★★☆

**Justification:** Existing Python package; useful for geological/mineralogical questions.

**Implementation:** Wrap `openmindat` package in MCP server.

### 5.3 USGS Data MCP Server (Medium Effort) ★★★☆☆

**Justification:** Would require parsing downloaded CSV files; no live API.

**Implementation:** Pre-load MCS data; expose query functions.

---

## 6. Recommended Data Gathering Workflow

Given the API landscape, I recommend the following phased approach:

### Phase 1: Bulk Downloads (Immediate)

| Source | Action | Output |
|--------|--------|--------|
| USGS MCS 2024/2025 | Download CSV data releases | Structured production/trade tables |
| USGS MRDS | Download deposit database | Geospatial occurrence data |
| CMI Models | Clone GitHub repos | Model documentation + data files |
| ICMM Dataset | Download from Zenodo | Facility registry |

### Phase 2: API Queries (Week 1)

| Source | Action | Output |
|--------|--------|--------|
| UN Comtrade | Query HS codes for 10 commodity groups (2020-2024) | Trade flow datasets |
| OpenMindat | Query mineral properties for CMM minerals | Mineral characteristics |

### Phase 3: Manual Extraction (Week 1-2)

| Source | Action | Output |
|--------|--------|--------|
| LANL SAFE | Manual query of REE separation data | Extraction chemistry parameters |
| ANL BatPaC | Download and parse Excel model | Material intensity factors |
| IEA Explorer | Manual export of demand projections | Scenario data |

### Phase 4: MCP Development (Optional, Week 2+)

If programmatic Gold Q&A validation is desired, develop UN Comtrade MCP server for automated trade flow queries.

---

## 7. Summary Table: Programmatic Access by Priority Source

| Rank | Source | API | Bulk DL | GitHub | MCP | Access Quality |
|------|--------|-----|---------|--------|-----|----------------|
| 1 | USGS MCS | ✗ | ✓ | ✗ | ✗ | ★★★★☆ |
| 2 | UN Comtrade | ✓ | ✓ | ✗ | Buildable | ★★★★★ |
| 3 | USGS Yearbook | ✗ | Partial | ✗ | ✗ | ★★★☆☆ |
| 4 | IEA Explorer | Limited | ✓ | ✗ | ✗ | ★★★☆☆ |
| 5 | LANL SAFE | ✗ | ✗ | ✗ | ✗ | ★★☆☆☆ |
| 6 | ANL BatPaC/GREET | ✗ | ✓ | ✗ | ✗ | ★★★☆☆ |
| 7 | CMI Models | ✗ | ✓ | ✓ | ✗ | ★★★★☆ |
| 8 | OpenMindat | ✓ | ✓ | ✓ | Buildable | ★★★★★ |
| 9 | Columbia Monitor | ✗ | ✗ | ✗ | ✗ | ★★☆☆☆ |
| 10 | USGS MRDS | ✗ | ✓ | ✗ | ✗ | ★★★★☆ |

---

## 8. Conclusion

**No existing MCP servers directly serve CMM supply chain data.** However, two sources have well-documented REST APIs suitable for MCP wrapper development:

1. **UN Comtrade** — ideal for trade flow questions (Q-TF, G-BM)
2. **OpenMindat** — useful for mineralogical questions (T-GO, T-EC)

For immediate Gold Q&A construction, I recommend:

1. **Download USGS MCS 2025 data release** (CSV) — covers ~40% of questions
2. **Register for UN Comtrade API key** and query CMM HS codes
3. **Register for OpenMindat API token** for mineral property queries
4. **Clone CMI GitHub repositories** for system dynamics reference data
5. **Manually extract LANL SAFE data** for REE separation chemistry

This hybrid approach (bulk download + API queries + manual extraction) provides comprehensive source coverage without requiring MCP development in the initial phase.

---

*End of Analysis*
