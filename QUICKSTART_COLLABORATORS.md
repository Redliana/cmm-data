# CMM Data - Quick Start Guide for Collaborators

Welcome to the Critical Minerals Modeling (CMM) Data package! This guide will get you up and running in 5 minutes.

---

## What is CMM Data?

CMM Data provides unified Python access to critical minerals datasets:

| Dataset | What's in it |
|---------|--------------|
| **USGS Commodity** | Production, reserves, trade for 80+ minerals |
| **USGS Ore Deposits** | Geochemistry from ore deposits worldwide |
| **Document Corpus** | 3,298 documents for NLP/LLM applications |
| **OECD/IEA** | Trade data, export restrictions, outlooks |
| **Geoscience Australia** | 3D chronostratigraphic model |
| **NETL** | REE concentrations in coal |

---

## Installation

### Option 1: From Globus/OneDrive (Recommended)

If you have access to the shared `Globus_Sharing` directory:

```bash
# Navigate to the shared directory
cd /path/to/Globus_Sharing

# Install the package
pip install -e cmm_data

# Or with visualization support
pip install -e "cmm_data[viz]"
```

### Option 2: From PyPI

```bash
pip install cmm-data

# With all features
pip install "cmm-data[full]"
```

### Option 3: From GitHub

```bash
pip install git+https://github.com/PNNL-CMM/cmm-data.git
```

---

## Verify Installation

```python
import cmm_data
print(f"Version: {cmm_data.__version__}")
print(cmm_data.get_data_catalog())
```

Expected output:
```
Version: 0.1.0
     dataset                  name  available
0   usgs_commodity      USGS Commodity       True
1        usgs_ore   USGS Ore Deposits       True
...
```

---

## 5-Minute Tutorial

### 1. View Available Data

```python
import cmm_data

# See all datasets
catalog = cmm_data.get_data_catalog()
print(catalog)

# List all commodities (80+)
commodities = cmm_data.list_commodities()
print(f"Total: {len(commodities)} commodities")

# List critical minerals (27)
critical = cmm_data.list_critical_minerals()
print(f"Critical minerals: {critical}")
```

### 2. Load Lithium Data

```python
# World production data
lithium = cmm_data.load_usgs_commodity("lithi", "world")
print(lithium[['Country', 'Prod_t_est_2022', 'Reserves_t']])
```

Output:
```
        Country  Prod_t_est_2022   Reserves_t
0     Australia          61000.0   6200000.0
1         Chile          39000.0   9300000.0
2         China          19000.0   2000000.0
3     Argentina           6200.0   2700000.0
```

### 3. Load U.S. Trade Data

```python
# Salient statistics (U.S. time series)
cobalt = cmm_data.load_usgs_commodity("cobal", "salient")
print(cobalt[['Year', 'Imports_t', 'Exports_t', 'NIR_pct']])
```

### 4. Get Top Producers

```python
loader = cmm_data.USGSCommodityLoader()

# Top 5 rare earth producers
top_ree = loader.get_top_producers("raree", top_n=5)
print(top_ree[['Country', 'Prod_t_est_2022']])
```

### 5. Create a Chart

```python
from cmm_data.visualizations.commodity import plot_world_production

df = cmm_data.load_usgs_commodity("lithi", "world")
fig = plot_world_production(df, "Lithium", top_n=10)
fig.savefig("lithium_producers.png")
```

---

## Common Commodity Codes

| Code | Mineral | Critical? |
|------|---------|-----------|
| `lithi` | Lithium | Yes |
| `cobal` | Cobalt | Yes |
| `nicke` | Nickel | Yes |
| `raree` | Rare Earths | Yes |
| `graph` | Graphite | Yes |
| `manga` | Manganese | Yes |
| `coppe` | Copper | No |
| `gold` | Gold | No |
| `iron` | Iron Ore | No |

Full list: `cmm_data.list_commodities()`

---

## Data Loaders

### USGS Commodity Loader
```python
from cmm_data import USGSCommodityLoader

loader = USGSCommodityLoader()
loader.list_available()              # Available commodities
loader.load_world_production("lithi") # World production
loader.load_salient_statistics("lithi") # U.S. statistics
loader.get_top_producers("lithi", 10)   # Top 10 producers
loader.get_commodity_name("lithi")      # "Lithium"
```

### USGS Ore Deposits Loader
```python
from cmm_data import USGSOreDepositsLoader

loader = USGSOreDepositsLoader()
loader.load_geology()                # Deposit locations
loader.load_geochemistry()           # Element concentrations
loader.get_ree_samples()             # REE analyses
loader.get_element_statistics("La")  # Lanthanum stats
```

### Document Corpus Loader
```python
from cmm_data import PreprocessedCorpusLoader

loader = PreprocessedCorpusLoader()
loader.get_corpus_stats()            # Corpus statistics
loader.search("lithium extraction")  # Search documents
loader.iter_documents()              # Iterate all docs
```

### OECD Supply Chain Loader
```python
from cmm_data import OECDSupplyChainLoader

loader = OECDSupplyChainLoader()
loader.get_minerals_coverage()       # Coverage info
loader.get_download_urls()           # Download URLs
loader.get_export_restrictions_reports()  # PDF paths
```

---

## Configuration

### Set Data Path

```python
import cmm_data

# Check current configuration
config = cmm_data.get_config()
print(f"Data root: {config.data_root}")

# Set custom path
cmm_data.configure(data_root="/path/to/Globus_Sharing")
```

### Environment Variable

```bash
export CMM_DATA_PATH=/path/to/Globus_Sharing
```

---

## Example Workflows

### Workflow 1: Compare Critical Minerals

```python
import cmm_data
import pandas as pd

loader = cmm_data.USGSCommodityLoader()
minerals = ['lithi', 'cobal', 'nicke', 'raree', 'graph']

comparison = []
for code in minerals:
    df = loader.load_salient_statistics(code)
    latest = df.iloc[-1]
    comparison.append({
        'Mineral': loader.get_commodity_name(code),
        'Year': latest['Year'],
        'NIR_pct': latest.get('NIR_pct', 'N/A')
    })

result = pd.DataFrame(comparison)
print(result)
```

### Workflow 2: Export Data to Excel

```python
import cmm_data

# Load multiple commodities
minerals = ['lithi', 'cobal', 'nicke']

with pd.ExcelWriter('critical_minerals.xlsx') as writer:
    for code in minerals:
        df = cmm_data.load_usgs_commodity(code, 'world')
        name = cmm_data.USGSCommodityLoader().get_commodity_name(code)
        df.to_excel(writer, sheet_name=name, index=False)

print("Saved to critical_minerals.xlsx")
```

### Workflow 3: Search Documents

```python
from cmm_data import PreprocessedCorpusLoader

loader = PreprocessedCorpusLoader()

# Search for lithium extraction documents
results = loader.search("lithium extraction", limit=10)
for _, doc in results.iterrows():
    print(f"- {doc.get('title', 'No title')[:60]}")
```

---

## Troubleshooting

### "Data not found" error

```python
import cmm_data

# Check if data path is configured
config = cmm_data.get_config()
print(f"Data root: {config.data_root}")

# Validate which datasets are available
status = config.validate()
for dataset, available in status.items():
    print(f"{'✓' if available else '✗'} {dataset}")

# Reconfigure if needed
cmm_data.configure(data_root="/correct/path/to/Globus_Sharing")
```

### Import error

```bash
# Reinstall
pip uninstall cmm-data
pip install -e /path/to/cmm_data
```

### Missing visualization

```bash
# Install viz dependencies
pip install matplotlib plotly
# Or
pip install -e "cmm_data[viz]"
```

---

## Getting Help

- **Documentation:** See `README.md` for full documentation
- **Examples:** Check `examples/` directory
- **Jupyter Tutorial:** `examples/cmm_data_tutorial.ipynb`
- **Issues:** https://github.com/PNNL-CMM/cmm-data/issues
- **Email:** cmm@pnnl.gov

---

## Quick Reference Card

```python
import cmm_data

# --- CATALOG ---
cmm_data.get_data_catalog()          # All datasets
cmm_data.list_commodities()          # All commodity codes
cmm_data.list_critical_minerals()    # Critical minerals only

# --- LOAD DATA ---
cmm_data.load_usgs_commodity("lithi", "world")    # World production
cmm_data.load_usgs_commodity("lithi", "salient")  # U.S. statistics

# --- LOADERS ---
cmm_data.USGSCommodityLoader()       # USGS commodity data
cmm_data.USGSOreDepositsLoader()     # Ore deposits database
cmm_data.PreprocessedCorpusLoader()  # Document corpus
cmm_data.OECDSupplyChainLoader()     # OECD/IEA data

# --- CONFIG ---
cmm_data.get_config()                # Current configuration
cmm_data.configure(data_root="...")  # Set data path

# --- VISUALIZATIONS ---
from cmm_data.visualizations.commodity import (
    plot_world_production,
    plot_production_timeseries,
    plot_import_reliance
)
```

---

*CMM Data v0.1.0 - Pacific Northwest National Laboratory*
