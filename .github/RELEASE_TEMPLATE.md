# CMM Data v0.1.0

**Critical Minerals Modeling Data Access Library** - Initial Release

## Highlights

- Unified API for accessing 7 critical minerals datasets
- 80+ mineral commodities from USGS Mineral Commodity Summaries
- 3,298 preprocessed documents for LLM training
- Built-in visualizations for production charts
- Pip-installable with optional geo/viz dependencies

## Installation

```bash
pip install cmm-data

# With all features
pip install "cmm-data[full]"
```

## Quick Start

```python
import cmm_data

# View available datasets
print(cmm_data.get_data_catalog())

# Load lithium production data
df = cmm_data.load_usgs_commodity("lithi", "world")
print(df[['Country', 'Prod_t_est_2022', 'Reserves_t']])

# List critical minerals
print(cmm_data.list_critical_minerals())
```

## Data Loaders

| Loader | Dataset | Records |
|--------|---------|---------|
| `USGSCommodityLoader` | USGS MCS 2023 | 80+ commodities |
| `USGSOreDepositsLoader` | USGS NGDB | 356 fields |
| `PreprocessedCorpusLoader` | CMM Corpus | 3,298 documents |
| `OECDSupplyChainLoader` | OECD/IEA | Trade & policy data |
| `GAChronostratigraphicLoader` | Geoscience Australia | 9 surfaces |
| `NETLREECoalLoader` | NETL | REE in coal |
| `OSTIDocumentsLoader` | DOE OSTI | Technical reports |

## Requirements

- Python 3.9+
- pandas >= 2.0.0
- numpy >= 1.24.0

## Documentation

- [README](https://github.com/PNNL-CMM/cmm-data#readme)
- [API Reference](https://pnnl-cmm.github.io/cmm-data/)
- [Examples](https://github.com/PNNL-CMM/cmm-data/tree/main/examples)

## What's Changed

* Initial release of CMM Data package
* 7 data loaders for critical minerals datasets
* Visualization module with production charts
* Comprehensive documentation and examples
* GitHub Actions CI/CD workflows
* Pre-commit hooks for code quality

**Full Changelog**: https://github.com/PNNL-CMM/cmm-data/commits/v0.1.0

---

*Developed by Pacific Northwest National Laboratory (PNNL)*
