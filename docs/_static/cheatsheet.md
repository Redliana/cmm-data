# CMM Data Cheatsheet

## Installation
```bash
pip install cmm-data            # Basic
pip install "cmm-data[full]"    # All features
```

## Quick Start
```python
import cmm_data

# View datasets
cmm_data.get_data_catalog()
cmm_data.list_commodities()
cmm_data.list_critical_minerals()

# Load data
df = cmm_data.load_usgs_commodity("lithi", "world")
df = cmm_data.load_usgs_commodity("cobal", "salient")
```

## Commodity Codes
| Code | Mineral | Code | Mineral |
|------|---------|------|---------|
| lithi | Lithium | raree | Rare Earths |
| cobal | Cobalt | graph | Graphite |
| nicke | Nickel | manga | Manganese |
| coppe | Copper | tungs | Tungsten |

## Loaders
```python
# USGS Commodity
loader = cmm_data.USGSCommodityLoader()
loader.load_world_production("lithi")
loader.load_salient_statistics("lithi")
loader.get_top_producers("lithi", 10)

# Ore Deposits
loader = cmm_data.USGSOreDepositsLoader()
loader.get_ree_samples()

# Documents
loader = cmm_data.PreprocessedCorpusLoader()
loader.search("lithium")

# OECD
loader = cmm_data.OECDSupplyChainLoader()
loader.get_minerals_coverage()
```

## Visualizations
```python
from cmm_data.visualizations.commodity import *

plot_world_production(df, "Lithium")
plot_production_timeseries(df, "Cobalt")
plot_import_reliance(df, "Rare Earths")
```

## Configuration
```python
cmm_data.configure(data_root="/path/to/data")
config = cmm_data.get_config()
```

## Help
- Docs: README.md
- Tutorial: examples/cmm_data_tutorial.ipynb
- Issues: github.com/PNNL-CMM/cmm-data/issues
