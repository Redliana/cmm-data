Changelog
=========

All notable changes to the CMM Data package are documented here.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.1.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

.. contents:: Contents
   :local:
   :depth: 2

Unreleased
----------

**Planned:**

- Additional visualization types (heatmaps, Sankey diagrams)
- Data export to multiple formats (Parquet, HDF5)
- Integration with pymrio for ICIO table analysis
- Automated data updates from USGS APIs

Version 0.1.0 (2026-01-08)
--------------------------

Initial release of the CMM Data package.

Added
^^^^^

**Core Package:**

- Pip-installable package with ``pyproject.toml`` configuration
- Optional dependencies: ``[viz]``, ``[geo]``, ``[full]``
- Automatic data path detection from environment and directory structure
- Built-in memory and disk caching with configurable TTL
- Comprehensive error handling with custom exceptions

**Data Loaders:**

- **USGSCommodityLoader**: Access to 80+ mineral commodities from USGS MCS 2023
- **USGSOreDepositsLoader**: USGS National Geochemical Database access
- **OSTIDocumentsLoader**: DOE OSTI technical report retrieval
- **PreprocessedCorpusLoader**: LLM-ready document corpus
- **GAChronostratigraphicLoader**: Geoscience Australia 3D model
- **NETLREECoalLoader**: NETL REE/Coal geodatabase
- **OECDSupplyChainLoader**: OECD/IEA supply chain data

**Catalog Functions:**

- ``get_data_catalog()`` - DataFrame of all datasets with availability
- ``list_commodities()`` - All 80+ USGS commodity codes
- ``list_critical_minerals()`` - DOE critical minerals list (27 covered)

**Visualization Module:**

- ``plot_world_production()`` - Bar chart of top producers
- ``plot_production_timeseries()`` - Time series of production/trade
- ``plot_import_reliance()`` - U.S. net import reliance charts
- ``plot_deposit_locations()`` - Geospatial deposit maps
- ``plot_ree_distribution()`` - REE concentration patterns

**Utilities:**

- ``parse_numeric_value()`` - Handle USGS special codes
- ``parse_range()`` - Parse range values
- Caching infrastructure with memory and disk backends

**Configuration:**

- ``CMMDataConfig`` dataclass for settings
- ``configure()`` and ``get_config()`` functions
- Environment variable support (``CMM_DATA_PATH``)
- Auto-detection of Globus_Sharing directory

**Documentation:**

- Comprehensive README.md (1,200+ lines)
- Sphinx API documentation
- Jupyter notebook tutorial
- Example scripts

**Testing:**

- Unit tests for core functionality
- Comprehensive test runner script
- GitHub Actions CI workflow

Dependencies
^^^^^^^^^^^^

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

Version History
---------------

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Version
     - Date
     - Description
   * - 0.1.0
     - 2026-01-08
     - Initial release
