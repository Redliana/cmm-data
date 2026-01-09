# Release Notes

## v0.1.0 - Initial Release

**Release Date:** January 8, 2026

We are excited to announce the first public release of **CMM Data** - the Critical Minerals Modeling Data Access Library developed by Pacific Northwest National Laboratory (PNNL).

---

### Highlights

- **Unified API** for accessing 7 different critical minerals datasets
- **80+ mineral commodities** from USGS Mineral Commodity Summaries
- **3,298 preprocessed documents** ready for LLM training
- **Built-in visualizations** for production charts and time series
- **Pip-installable** with optional dependencies for geo/viz features

---

### New Features

#### Data Loaders

| Loader | Dataset | Description |
|--------|---------|-------------|
| `USGSCommodityLoader` | USGS MCS 2023 | World production, reserves, U.S. statistics for 80+ commodities |
| `USGSOreDepositsLoader` | USGS NGDB | Geochemistry data with 356 fields, REE analyses |
| `OSTIDocumentsLoader` | DOE OSTI | Technical reports and publications |
| `PreprocessedCorpusLoader` | CMM Corpus | 3,298 documents for NLP/LLM applications |
| `GAChronostratigraphicLoader` | Geoscience Australia | 3D chronostratigraphic model (9 surfaces) |
| `NETLREECoalLoader` | NETL | REE concentrations in coal samples |
| `OECDSupplyChainLoader` | OECD/IEA | Trade data, export restrictions, critical minerals outlook |

#### Convenience Functions

```python
import cmm_data

# View all datasets
cmm_data.get_data_catalog()

# List available commodities
cmm_data.list_commodities()        # 80+ commodities
cmm_data.list_critical_minerals()  # 27 DOE critical minerals

# Quick data loading
cmm_data.load_usgs_commodity("lithi", "world")
cmm_data.load_usgs_commodity("cobal", "salient")
```

#### Visualizations

```python
from cmm_data.visualizations.commodity import (
    plot_world_production,
    plot_production_timeseries,
    plot_import_reliance
)

# Create charts
fig = plot_world_production(df, "Lithium", top_n=10)
fig = plot_production_timeseries(df, "Cobalt")
fig = plot_import_reliance(df, "Rare Earths")
```

#### Configuration

```python
import cmm_data

# Auto-detects data path from environment or directory structure
config = cmm_data.get_config()

# Manual configuration
cmm_data.configure(
    data_root="/path/to/Globus_Sharing",
    cache_enabled=True,
    cache_ttl_seconds=3600
)
```

#### Utilities

- `parse_numeric_value()` - Handle USGS special codes (W, NA, --, ranges)
- `parse_range()` - Parse range values like ">50", "<100", "100-200"
- Built-in memory and disk caching with configurable TTL

---

### Critical Minerals Coverage

27 of the 50 DOE Critical Minerals are covered with USGS data:

| | | | |
|---|---|---|---|
| Aluminum | Antimony | Arsenic | Barite |
| Beryllium | Bismuth | Chromium | Cobalt |
| Fluorspar | Gallium | Germanium | Graphite |
| Indium | Lithium | Manganese | Nickel |
| Niobium | Platinum Group | Rare Earths | Tantalum |
| Tellurium | Tin | Titanium | Tungsten |
| Vanadium | Zinc | Zirconium/Hafnium | |

---

### Installation

```bash
# Basic installation
pip install cmm-data

# With visualization support
pip install "cmm-data[viz]"

# With geospatial support
pip install "cmm-data[geo]"

# Full installation
pip install "cmm-data[full]"
```

---

### Requirements

**Python:** 3.9, 3.10, 3.11, 3.12

**Required Dependencies:**
- pandas >= 2.0.0
- numpy >= 1.24.0

**Optional Dependencies:**
- matplotlib >= 3.7.0 (viz)
- plotly >= 5.15.0 (viz)
- geopandas >= 0.14.0 (geo)
- rasterio >= 1.3.0 (geo)
- fiona >= 1.9.0 (geo)

---

### Documentation

- **README:** Comprehensive documentation with examples
- **Sphinx Docs:** Full API reference at `docs/`
- **Examples:** Jupyter notebook tutorial and Python scripts
- **CONTRIBUTING:** Development setup and guidelines

---

### Package Contents

```
cmm_data/
├── 62 files total
├── 19 source files (loaders, visualizations, utilities)
├── 17 documentation files (Sphinx + markdown)
├── 5 example files (notebook + scripts)
├── 5 script files (tests, build, demo)
├── 3 GitHub workflow files (CI/CD)
└── Configuration, license, and setup files
```

---

### Known Limitations

1. **OECD bulk data** requires manual download due to Cloudflare protection
2. **NETL geodatabase** requires geopandas/fiona installation
3. **GA GeoTIFF files** require rasterio for full functionality
4. **Shell commands** in documentation assume Unix-like environment

---

### Acknowledgments

This work was supported by the U.S. Department of Energy. Data sources include:

- U.S. Geological Survey (USGS)
- Office of Scientific and Technical Information (OSTI)
- Organisation for Economic Co-operation and Development (OECD)
- International Energy Agency (IEA)
- Geoscience Australia
- National Energy Technology Laboratory (NETL)

---

### What's Next (Planned for v0.2.0)

- [ ] Integration with pymrio for ICIO table analysis
- [ ] Additional visualization types (heatmaps, Sankey diagrams)
- [ ] Data export to Parquet and HDF5 formats
- [ ] Automated data updates from USGS APIs
- [ ] Additional loaders for new data sources

---

### Links

- **GitHub:** https://github.com/PNNL-CMM/cmm-data
- **Documentation:** https://pnnl-cmm.github.io/cmm-data/
- **Issues:** https://github.com/PNNL-CMM/cmm-data/issues
- **PyPI:** https://pypi.org/project/cmm-data/

---

### Contributors

- CMM Team @ Pacific Northwest National Laboratory
- Claude (AI Assistant) - Code generation and documentation

---

**Full Changelog:** https://github.com/PNNL-CMM/cmm-data/commits/v0.1.0

---

*CMM Data v0.1.0 - Critical Minerals Modeling Data Access Library*
*Pacific Northwest National Laboratory*
