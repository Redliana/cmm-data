# Changelog

All notable changes to the CMM Data package will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Additional visualization types (heatmaps, Sankey diagrams)
- Data export to multiple formats (Parquet, HDF5)
- Integration with pymrio for ICIO table analysis
- Automated data updates from USGS APIs

---

## [0.1.0] - 2026-01-08

### Added

#### Core Package
- Initial release of `cmm_data` package
- Pip-installable package with `pyproject.toml` configuration
- Optional dependencies: `[viz]`, `[geo]`, `[full]`
- Automatic data path detection from environment and directory structure
- Built-in memory and disk caching with configurable TTL
- Comprehensive error handling with custom exceptions

#### Data Loaders
- **USGSCommodityLoader**: Access to 80+ mineral commodities from USGS MCS 2023
  - `load_world_production()`: Country-level production and reserves
  - `load_salient_statistics()`: U.S. time series data
  - `get_top_producers()`: Ranked producer lists
  - Automatic parsing of special codes (W, NA, ranges)

- **USGSOreDepositsLoader**: USGS National Geochemical Database access
  - `load_geology()`: Deposit locations and geological context
  - `load_geochemistry()`: Element concentration data
  - `get_ree_samples()`: Rare earth element analyses
  - `get_element_statistics()`: Statistical summaries
  - Support for 356 database fields

- **OSTIDocumentsLoader**: DOE OSTI technical report retrieval
  - `search_documents()`: Full-text search
  - `get_document_metadata()`: Document information
  - Integration with existing OSTI retrieval infrastructure

- **PreprocessedCorpusLoader**: LLM-ready document corpus
  - `iter_documents()`: Memory-efficient iteration
  - `get_corpus_stats()`: Corpus statistics
  - `search()`: Text search across 3,298 documents
  - `filter_by_source()`: Source-based filtering

- **GAChronostratigraphicLoader**: Geoscience Australia 3D model
  - Support for 9 chronostratigraphic surfaces
  - Multiple formats: GeoTIFF, XYZ, ZMAP
  - `get_surface_extent()`: Spatial bounds
  - `get_model_info()`: Model metadata

- **NETLREECoalLoader**: NETL REE/Coal geodatabase
  - `get_ree_samples()`: Coal REE concentrations
  - `get_ree_statistics()`: Element statistics
  - GeoPandas integration for spatial analysis

- **OECDSupplyChainLoader**: OECD/IEA supply chain data
  - `get_export_restrictions_reports()`: Policy PDFs
  - `get_iea_minerals_reports()`: IEA outlook reports
  - `get_minerals_coverage()`: Coverage information
  - `get_download_urls()`: Manual download links

#### Catalog Functions
- `get_data_catalog()`: DataFrame of all datasets with availability status
- `list_commodities()`: All 80+ USGS commodity codes
- `list_critical_minerals()`: DOE critical minerals list (27 covered)

#### Visualization Module
- `plot_world_production()`: Bar chart of top producers
- `plot_production_timeseries()`: Time series of production/trade
- `plot_import_reliance()`: U.S. net import reliance charts
- `plot_deposit_locations()`: Geospatial deposit maps (requires geo extras)
- `plot_ree_distribution()`: REE concentration patterns

#### Utilities
- `parse_numeric_value()`: Handle USGS special codes (W, NA, --, etc.)
- `parse_range()`: Parse range values (>50, <100, 100-200)
- Caching infrastructure with memory and disk backends

#### Configuration
- `CMMDataConfig` dataclass for settings
- `configure()`: Runtime configuration
- `get_config()`: Access current settings
- Environment variable support (`CMM_DATA_PATH`)
- Auto-detection of Globus_Sharing directory

#### Documentation
- Comprehensive README.md (1,200+ lines)
- QUICKSTART.md for rapid onboarding
- DISTRIBUTION.md for wheel building and sharing
- CONTRIBUTING.md for development guidelines
- API reference with method tables
- Code examples for all loaders

#### Examples
- `basic_usage.py`: Core API demonstrations
- `visualization_examples.py`: Chart generation
- `data_export.py`: Export to CSV/Excel
- `cmm_data_tutorial.ipynb`: Jupyter notebook tutorial

#### Testing
- `tests/test_basic.py`: Unit tests for core functionality
- `scripts/run_all_tests.py`: Comprehensive test runner
- `scripts/verify_installation.py`: Installation verification
- GitHub Actions CI workflow

#### Build & Distribution
- `pyproject.toml`: Modern Python packaging
- `setup.py`: Backward compatibility
- `MANIFEST.in`: Source distribution configuration
- `scripts/build_wheel.py`: Cross-platform build script
- `.gitignore`: Git configuration

### Data Coverage

| Dataset | Records | Format |
|---------|---------|--------|
| USGS Commodity | 80+ commodities | CSV |
| USGS Ore Deposits | 356 fields | CSV |
| Preprocessed Corpus | 3,298 documents | JSONL |
| GA Chronostratigraphic | 9 surfaces | GeoTIFF/XYZ |
| OECD Supply Chain | Multiple | PDF/CSV |
| NETL REE/Coal | Variable | Geodatabase |
| OSTI Documents | Variable | JSON |

### Critical Minerals Covered

27 of 50 DOE critical minerals with USGS data:
- Aluminum, Antimony, Arsenic, Barite, Beryllium, Bismuth
- Chromium, Cobalt, Fluorspar, Gallium, Germanium, Graphite
- Indium, Lithium, Manganese, Nickel, Niobium, Platinum Group
- Rare Earths, Tantalum, Tellurium, Tin, Titanium, Tungsten
- Vanadium, Zinc, Zirconium/Hafnium

### Dependencies

**Required:**
- Python >= 3.9
- pandas >= 2.0.0
- numpy >= 1.24.0

**Optional (viz):**
- matplotlib >= 3.7.0
- plotly >= 5.15.0

**Optional (geo):**
- geopandas >= 0.14.0
- rasterio >= 1.3.0
- fiona >= 1.9.0

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 0.1.0 | 2026-01-08 | Initial release |

---

## Upgrade Guide

### Installing v0.1.0

```bash
# From source
pip install -e /path/to/cmm_data

# From wheel
pip install cmm_data-0.1.0-py3-none-any.whl

# With all optional dependencies
pip install -e "/path/to/cmm_data[full]"
```

### Verifying Installation

```python
import cmm_data
print(f"Version: {cmm_data.__version__}")
print(cmm_data.get_data_catalog())
```

---

## Links

- **Repository**: https://github.com/PNNL-CMM/cmm-data
- **Issues**: https://github.com/PNNL-CMM/cmm-data/issues
- **Documentation**: See README.md

---

*CMM Data - Critical Minerals Modeling Data Access Library*
*Pacific Northwest National Laboratory*
