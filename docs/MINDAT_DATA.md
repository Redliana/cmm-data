# Mindat.org Mineralogical Database - Critical Minerals Data

This directory contains mineralogical data retrieved from the Mindat.org database via the OpenMindat API, focused on critical minerals and materials relevant to the Critical Minerals Modeling (CMM) project.

## Table of Contents

1. [Overview](#overview)
2. [Data Source](#data-source)
3. [Directory Structure](#directory-structure)
4. [Data Files](#data-files)
5. [Field Descriptions](#field-descriptions)
6. [Usage with MindatLoader](#usage-with-mindatloader)
7. [Critical Elements Coverage](#critical-elements-coverage)
8. [Key Ore Minerals](#key-ore-minerals)
9. [Data Statistics](#data-statistics)
10. [License and Attribution](#license-and-attribution)
11. [References](#references)

---

## Overview

Mindat.org is the world's largest open mineralogical database, containing information on over 6,000 IMA-approved mineral species, hundreds of thousands of mineral localities worldwide, and extensive data on mineral properties, crystal structures, and classifications.

This data collection supports the CMM project by providing:

- **Mineral species data** for elements designated as critical by the U.S. Department of Energy
- **Locality/occurrence data** showing global distribution of critical mineral deposits
- **Detailed physical and chemical properties** for key ore minerals used in extraction and processing
- **Classification systems** (Dana, Strunz) for systematic organization

---

## Data Source

| Attribute | Value |
|-----------|-------|
| **Source** | Mindat.org |
| **API** | OpenMindat REST API |
| **Python Package** | `openmindat` (v0.1.2) |
| **API Documentation** | https://api.mindat.org/schema/redoc/ |
| **Data Retrieved** | January 2026 |
| **License** | CC BY-NC-SA 4.0 |

### API Access

Data was retrieved using the OpenMindat Python package with authenticated API access. To replicate or update this data:

```python
import os
os.environ["MINDAT_API_KEY"] = "your_api_key_here"

from cmm_data import MindatLoader
loader = MindatLoader()
```

API keys can be obtained by registering at [mindat.org](https://www.mindat.org) and applying for Data Contributor status.

---

## Directory Structure

```
Mindat/
├── README.md                    # This file
├── geomaterials/                # Mineral species data by element
│   ├── element_Li_ima.json      # Lithium-bearing IMA minerals
│   ├── element_Co_ima.json      # Cobalt-bearing IMA minerals
│   ├── element_Ni_ima.json      # Nickel-bearing IMA minerals
│   ├── element_Mn_ima.json      # Manganese-bearing IMA minerals
│   ├── element_Al_ima.json      # Aluminum-bearing IMA minerals
│   ├── ... (42 element files)
│   └── all_minerals.json        # Complete IMA minerals list (6,190 minerals)
├── localities/                  # Mineral occurrence localities by element
│   ├── element_Li.json          # Lithium localities worldwide
│   ├── element_Co.json          # Cobalt localities worldwide
│   ├── element_Cu.json          # Copper localities worldwide
│   ├── element_Al.json          # Aluminum localities worldwide
│   ├── ... (27 element files)
└── ore_minerals/                # Detailed properties for key ore minerals
    └── key_ore_minerals.json    # 64 primary ore minerals with full properties
```

---

## Data Files

### 1. Geomaterials (Mineral Species)

**Location:** `geomaterials/`

Contains mineral species data filtered by element. Each file contains IMA-approved minerals that include the specified element in their chemical formula.

| File Pattern | Description | Example |
|--------------|-------------|---------|
| `element_{Symbol}_ima.json` | Minerals containing element | `element_Li_ima.json` |
| `all_minerals.json` | Complete IMA mineral list | 6,190 minerals |

**Sample record structure:**
```json
{
  "id": 3733,
  "name": "Spodumene",
  "ima_formula": "LiAlSi<sub>2</sub>O<sub>6</sub>",
  "ima_symbol": "Spd",
  "ima_status": ["APPROVED", "GRANDFATHERED"],
  "ima_year": 0,
  "discovery_year": 1800,
  "mindat_formula": "LiAl(Si<sub>2</sub>O<sub>6</sub>)",
  "type_localities": [28947],
  "description_short": "A lithium aluminium silicate...",
  "query_element": "Li",
  "query_element_name": "Lithium"
}
```

### 2. Localities (Mineral Occurrences)

**Location:** `localities/`

Contains geographic locations where minerals containing specific elements have been found. Includes coordinates, country information, and site descriptions.

| File Pattern | Description | Records (approx.) |
|--------------|-------------|-------------------|
| `element_Li.json` | Lithium localities | 5,811 |
| `element_Co.json` | Cobalt localities | 8,798 |
| `element_Ni.json` | Nickel localities | 14,783 |
| `element_Cu.json` | Copper localities | 81,087 |
| `element_Al.json` | Aluminum localities | 101,015 |
| ... | ... | ... |

**Sample record structure:**
```json
{
  "id": 3241,
  "txt": "Dara-i-Pioz Massif, Districts of Republican Subordination, Tajikistan",
  "country": "Tajikistan",
  "latitude": 39.45035,
  "longitude": 70.716342,
  "elements": "-Fe-Na-Si-O-Al-Ca-Mg-F-Pb-Ce-H-Ti-K-P-U-Ba-Cl-Li-Be-...",
  "description_short": "Alkaline massif with boron-rich granitoids...",
  "discovery_year": 0,
  "discovered_before": 1968,
  "locality_type": 293,
  "loc_status": 0,
  "wikipedia": "https://de.wikipedia.org/wiki/Dara-i-Pioz",
  "datemodify": "2026-01-11 14:50:44"
}
```

### 3. Key Ore Minerals (Detailed Properties)

**Location:** `ore_minerals/key_ore_minerals.json`

Contains comprehensive physical, chemical, optical, and crystallographic properties for 64 primary ore minerals of critical elements.

**Sample record structure (150 fields):**
```json
{
  "id": 3733,
  "name": "Spodumene",
  "primary_element": "Li",
  "ore_notes": "Primary Li ore",
  "ima_formula": "LiAlSi<sub>2</sub>O<sub>6</sub>",
  "csystem": "Monoclinic",
  "spacegroup": 10,
  "a": 9.46,
  "b": 8.39,
  "c": 5.22,
  "alpha": 0,
  "beta": 110.17,
  "gamma": 0,
  "z": 4,
  "hmin": 6.5,
  "hmax": 7.0,
  "dmeas": 3.1,
  "dcalc": 3.184,
  "colour": "Colourless, yellow, light green, emerald-green, pink to violet...",
  "lustre": "Vitreous",
  "streak": "White",
  "tenacity": "brittle",
  "opticaltype": "Biaxial",
  "opticalsign": "+",
  "optical2vmeasured": 54,
  "opticalalpha": 1.648,
  "opticalbeta": 1.655,
  "opticalgamma": 1.662,
  "dana8ed1": 65,
  "dana8ed2": 1,
  "dana8ed3": 4,
  "dana8ed4": 1,
  "strunz10ed1": 9,
  "strunz10ed2": "D",
  "strunz10ed3": "A"
}
```

---

## Field Descriptions

### Geomaterials Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Mindat unique identifier |
| `name` | string | Mineral name |
| `ima_formula` | string | IMA-approved chemical formula (HTML formatted) |
| `ima_symbol` | string | IMA mineral symbol abbreviation |
| `ima_status` | array | IMA approval status (APPROVED, GRANDFATHERED, etc.) |
| `ima_year` | integer | Year of IMA approval |
| `discovery_year` | integer | Year mineral was first described |
| `mindat_formula` | string | Mindat chemical formula variant |
| `mindat_formula_note` | string | Notes on formula |
| `type_localities` | array | IDs of type localities |
| `type_specimen_store` | string | Location of type specimen |
| `description_short` | string | Brief description |
| `query_element` | string | Element used in query (added by loader) |
| `query_element_name` | string | Full element name (added by loader) |

### Localities Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Mindat locality ID |
| `txt` | string | Full locality name/path |
| `country` | string | Country name |
| `latitude` | float | GPS latitude (WGS84) |
| `longitude` | float | GPS longitude (WGS84) |
| `elements` | string | Elements found at locality (dash-separated) |
| `description_short` | string | Geological description |
| `discovery_year` | integer | Year discovered |
| `discovered_before` | integer | Known to exist before this year |
| `locality_type` | integer | Type code (mine, quarry, occurrence, etc.) |
| `loc_status` | integer | Status code (active, historic, etc.) |
| `loc_group` | integer | Locality group ID |
| `level` | integer | Hierarchical level |
| `parent` | integer | Parent locality ID |
| `wikipedia` | string | Wikipedia URL if available |
| `dateadd` | datetime | Date added to database |
| `datemodify` | datetime | Date last modified |
| `status_year` | integer | Year of status determination |

### Ore Minerals Physical Properties Fields

| Field | Type | Unit | Description |
|-------|------|------|-------------|
| `csystem` | string | - | Crystal system (Isometric, Hexagonal, etc.) |
| `spacegroup` | integer | - | Space group number |
| `a`, `b`, `c` | float | Å | Unit cell edge lengths |
| `alpha`, `beta`, `gamma` | float | degrees | Unit cell angles |
| `z` | integer | - | Formula units per unit cell |
| `hmin`, `hmax` | float | Mohs | Hardness range |
| `dmeas` | float | g/cm³ | Measured density |
| `dcalc` | float | g/cm³ | Calculated density |
| `colour` | string | - | Color description |
| `lustre` | string | - | Lustre type |
| `streak` | string | - | Streak color |
| `tenacity` | string | - | Tenacity (brittle, flexible, etc.) |
| `opticaltype` | string | - | Optical character (Isotropic, Uniaxial, Biaxial) |
| `opticalsign` | string | - | Optical sign (+/-) |
| `optical2vmeasured` | float | degrees | 2V angle (measured) |
| `opticalalpha`, `opticalbeta`, `opticalgamma` | float | - | Refractive indices |

### Classification Fields

| Field | Description |
|-------|-------------|
| `dana8ed1` - `dana8ed4` | Dana-8 classification hierarchy |
| `strunz10ed1` - `strunz10ed3` | Nickel-Strunz 10th edition classification |

---

## Usage with MindatLoader

The `MindatLoader` class in the `cmm_data` package provides convenient access to this data.

### Installation

```bash
pip install openmindat  # Required for API access
```

### Basic Usage

```python
from cmm_data import MindatLoader

# Initialize loader
loader = MindatLoader()

# Check what's available
print(loader.describe())
print(loader.list_cached_elements())
```

### Loading Mineral Data

```python
# Load minerals for a specific element as DataFrame
df_li = loader.load(element="Li")
print(f"Lithium minerals: {len(df_li)}")
print(df_li[['name', 'ima_formula']].head())

# Load all cached critical minerals
df_all = loader.load_all_critical_minerals()

# Get summary statistics
summary = loader.get_mineral_summary("Co")
print(f"Cobalt minerals: {summary['mineral_count']}")
```

### Loading Locality Data

```python
# Load localities as DataFrame
df_localities = loader.load_localities("element_Li")

# Filter by country
usa_li = df_localities[df_localities['country'] == 'USA']
print(f"US lithium localities: {len(usa_li)}")

# Get coordinates for mapping
coords = df_localities[['txt', 'latitude', 'longitude', 'country']]
```

### Loading Ore Mineral Properties

```python
import json

# Load ore minerals data
with open('ore_minerals/key_ore_minerals.json') as f:
    ore_minerals = json.load(f)

# Filter by element
li_ores = [m for m in ore_minerals if m['primary_element'] == 'Li']
for mineral in li_ores:
    print(f"{mineral['name']}: H={mineral.get('hmin')}-{mineral.get('hmax')}, "
          f"D={mineral.get('dmeas')} g/cm³")
```

### Fetching New Data (Requires API Key)

```python
import os
os.environ["MINDAT_API_KEY"] = "your_key_here"

loader = MindatLoader()

# Fetch minerals for a new element
sc_minerals = loader.fetch_minerals_by_element("Sc", ima_only=True, save=True)

# Fetch all critical minerals at once
all_data = loader.fetch_all_ima_and_filter_critical(save=True)

# Fetch locality data
localities = loader.fetch_localities_by_country("Australia", save=True)
```

### Querying with Filters

```python
# Query minerals with filters
df = loader.query(
    element="Li",
    crystal_system="Monoclinic"
)

# Using pandas for complex queries
df_li = loader.load(element="Li")
pegmatite_minerals = df_li[df_li['description_short'].str.contains('pegmatite', case=False, na=False)]
```

---

## Critical Elements Coverage

### DOE Critical Minerals List (2023)

The data covers all 50 elements designated as critical or relevant to critical mineral supply chains:

#### Battery Metals
| Element | Symbol | Minerals | Localities |
|---------|--------|----------|------------|
| Lithium | Li | 62 | 5,811 |
| Cobalt | Co | 28 | 8,798 |
| Nickel | Ni | 114 | 14,783 |
| Manganese | Mn | 145 | 28,632 |

#### Rare Earth Elements (REE)
| Element | Symbol | Minerals | Localities |
|---------|--------|----------|------------|
| Lanthanum | La | 33 | 1,889 |
| Cerium | Ce | 80 | 8,333 |
| Neodymium | Nd | 23 | 2,716 |
| Yttrium | Y | 68 | 7,480 |
| Scandium | Sc | 14 | - |
| (+ 12 more REE) | | | |

#### Technology Metals
| Element | Symbol | Minerals | Localities |
|---------|--------|----------|------------|
| Gallium | Ga | 3 | 203 |
| Germanium | Ge | 17 | 943 |
| Indium | In | 6 | 783 |
| Tellurium | Te | 62 | 7,717 |

#### Refractory Metals
| Element | Symbol | Minerals | Localities |
|---------|--------|----------|------------|
| Tungsten | W | 11 | 15,480 |
| Niobium | Nb | 106 | 8,374 |
| Tantalum | Ta | 37 | 4,179 |
| Titanium | Ti | 202 | 46,970 |

#### Platinum Group Metals (PGM)
| Element | Symbol | Minerals | Localities |
|---------|--------|----------|------------|
| Platinum | Pt | 23 | 3,451 |
| Palladium | Pd | 55 | 2,077 |
| Rhodium | Rh | 11 | - |
| Iridium | Ir | 10 | - |
| Ruthenium | Ru | 6 | - |
| Osmium | Os | 3 | - |

#### Other Critical Elements
| Element | Symbol | Minerals | Localities |
|---------|--------|----------|------------|
| Aluminum | Al | 833 | 101,015 |
| Chromium | Cr | 27 | 12,658 |
| Copper | Cu | - | 81,087 |
| Zinc | Zn | 216 | 52,978 |
| Tin | Sn | 47 | 13,891 |
| Antimony | Sb | 186 | 25,970 |
| Bismuth | Bi | 149 | - |
| Beryllium | Be | 89 | 12,504 |
| Zirconium | Zr | 85 | 19,653 |
| Vanadium | V | 57 | 9,076 |
| Fluorine | F | 342 | - |
| Barium | Ba | 136 | - |
| Arsenic | As | 187 | - |

---

## Key Ore Minerals

The following 64 minerals are the primary ore sources for critical elements:

### Lithium Ores
| Mineral | Formula | Hardness | Density | Crystal System |
|---------|---------|----------|---------|----------------|
| Spodumene | LiAlSi₂O₆ | 6.5-7.0 | 3.10 | Monoclinic |
| Lepidolite | K(Li,Al)₃(Si,Al)₄O₁₀(F,OH)₂ | 2.5-3.0 | 2.84 | Monoclinic |
| Petalite | LiAlSi₄O₁₀ | 6.5 | 2.42 | Monoclinic |
| Amblygonite | LiAlPO₄F | 5.5-6.0 | 3.02 | Triclinic |

### Cobalt Ores
| Mineral | Formula | Hardness | Density | Crystal System |
|---------|---------|----------|---------|----------------|
| Cobaltite | CoAsS | 5.5 | 6.33 | Orthorhombic |
| Skutterudite | CoAs₃ | 5.5-6.0 | 6.50 | Isometric |
| Carrollite | CuCo₂S₄ | 4.5-5.5 | 4.85 | Isometric |
| Erythrite | Co₃(AsO₄)₂·8H₂O | 1.5-2.5 | 3.18 | Monoclinic |

### Nickel Ores
| Mineral | Formula | Hardness | Density | Crystal System |
|---------|---------|----------|---------|----------------|
| Pentlandite | (Fe,Ni)₉S₈ | 3.5-4.0 | 4.90 | Isometric |
| Millerite | NiS | 3.0-3.5 | 5.37 | Trigonal |
| Nickeline | NiAs | 5.0-5.5 | 7.78 | Hexagonal |
| Garnierite | (Ni,Mg)₃Si₂O₅(OH)₄ | - | - | - |

### Rare Earth Ores
| Mineral | Formula | Hardness | Density | Crystal System |
|---------|---------|----------|---------|----------------|
| Bastnäsite-(Ce) | (Ce,La)(CO₃)F | 4.0-4.5 | 4.95 | Hexagonal |
| Monazite-(Ce) | (Ce,La,Nd,Th)PO₄ | 5.0-5.5 | 5.15 | Monoclinic |
| Xenotime-(Y) | YPO₄ | 4.0-5.0 | 4.75 | Tetragonal |

### Tungsten Ores
| Mineral | Formula | Hardness | Density | Crystal System |
|---------|---------|----------|---------|----------------|
| Wolframite | (Fe,Mn)WO₄ | 4.0-4.5 | 7.30 | Monoclinic |
| Scheelite | CaWO₄ | 4.5-5.0 | 6.01 | Tetragonal |
| Ferberite | FeWO₄ | 4.0-4.5 | 7.51 | Monoclinic |
| Hübnerite | MnWO₄ | 4.0-4.5 | 7.18 | Monoclinic |

*(See `ore_minerals/key_ore_minerals.json` for complete list with all 150 properties)*

---

## Data Statistics

### Summary Totals

| Dataset | Records | Size | Files |
|---------|---------|------|-------|
| Mineral Species (by element) | ~3,500 unique | 3 MB | 42 |
| All IMA Minerals | 6,190 | 5 MB | 1 |
| Localities | ~500,000 | 690 MB | 27 |
| Key Ore Minerals | 64 | 326 KB | 1 |
| **Total** | **~500,000** | **~700 MB** | **71** |

### Top Countries by Locality Count

| Rank | Country | Localities |
|------|---------|------------|
| 1 | USA | 29,941+ |
| 2 | China | 6,517+ |
| 3 | Australia | 5,756+ |
| 4 | Italy | 3,795+ |
| 5 | Norway | 3,548+ |
| 6 | Canada | 3,397+ |
| 7 | France | 3,383+ |
| 8 | Austria | 3,120+ |
| 9 | Germany | 3,092+ |
| 10 | Russia | 2,338+ |

---

## License and Attribution

### Data License

The data from Mindat.org is provided under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)**.

This means:
- **Attribution** - You must give appropriate credit to Mindat.org
- **NonCommercial** - You may not use the material for commercial purposes
- **ShareAlike** - If you remix or transform the material, you must distribute under the same license

### Required Attribution

When using this data, please cite:

> Ralph, J., Von Bargen, D., Martynov, P., Zhang, J., Que, X., Prabhu, A., Morrison, S. M., Li, W., Chen, W., & Ma, X. (2025). Mindat.org: The open access mineralogy database to accelerate data-intensive geoscience research. American Mineralogist, 110(6), 833-844. doi:10.2138/am-2024-9486

### OpenMindat Package

The data was retrieved using the OpenMindat Python package:

> Ma, X., Ralph, J., Zhang, J., Que, X., Prabhu, A., Morrison, S.M., Hazen, R.M., Wyborn, L., Lehnert, K., 2023. OpenMindat: Open and FAIR mineralogy data from the Mindat database. Geoscience Data Journal, doi:10.1002/gdj3.204

---

## References

### Primary Sources

1. **Mindat.org** - https://www.mindat.org
   - World's largest mineralogical database
   - Hudson Institute of Mineralogy

2. **OpenMindat API** - https://api.mindat.org/schema/redoc/
   - REST API documentation
   - Authentication and usage guidelines

3. **OpenMindat Python Package** - https://pypi.org/project/openmindat/
   - PyPI package page
   - Source: https://github.com/ChuBL/OpenMindat

### Related CMM Data Sources

This Mindat data complements other datasets in the CMM project:

| Source | Data Type | Location |
|--------|-----------|----------|
| USGS MCS | Production statistics | `../USGS_Data/` |
| USGS MRDS | Ore deposit geochemistry | `../USGS_Ore_Deposits/` |
| OECD | Trade and supply chain | `../OECD_Supply_Chain_Data/` |
| NETL | REE from coal | `../NETL_REE_Coal/` |
| SEC EDGAR | Company filings | `../Tools/` |

### Classification Systems

1. **Dana Classification** (8th Edition)
   - Systematic mineralogy based on chemical composition and crystal structure
   - Format: Class.Division.Family.Species (e.g., 65.1.4.1)

2. **Nickel-Strunz Classification** (10th Edition)
   - Chemical-structural classification system
   - Format: Class.Division.Subdivision (e.g., 9.D.A)

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-01-26 | 1.0.0 | Initial data collection |
| | | - 42 elements mineral species data |
| | | - 27 elements locality data |
| | | - 64 key ore minerals with detailed properties |

---

## Contact

For questions about this data collection or the CMM project:

- **Project Repository**: https://github.com/Redliana/cmm-data
- **Mindat Support**: https://www.mindat.org/contact.php

---

*This README was generated on January 26, 2026*
