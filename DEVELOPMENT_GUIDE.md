# CMM Data Package - Development Guide

**A Complete Record of Building the Critical Minerals Modeling Data Access Library**

**Date:** January 8-9, 2026
**Author:** CMM Team @ PNNL with Claude Opus 4.5
**Repository:** https://github.com/Redliana/cmm-data

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Package Architecture](#2-package-architecture)
3. [Implementation Details](#3-implementation-details)
4. [Files Created](#4-files-created)
5. [Setup Instructions](#5-setup-instructions)
6. [Testing](#6-testing)
7. [Documentation](#7-documentation)
8. [CI/CD Pipeline](#8-cicd-pipeline)
9. [Publishing](#9-publishing)
10. [Usage Examples](#10-usage-examples)
11. [Troubleshooting](#11-troubleshooting)
12. [Future Development](#12-future-development)

---

## 1. Project Overview

### Objective

Create a pip-installable Python package that provides unified access to critical minerals datasets for the CMM (Critical Minerals Modeling) project at Pacific Northwest National Laboratory.

### Problem Solved

Researchers working on critical minerals supply chain modeling need to access data from multiple heterogeneous sources:
- USGS Mineral Commodity Summaries
- USGS Ore Deposits Database
- DOE OSTI Technical Reports
- OECD/IEA Trade and Policy Data
- Geoscience Australia 3D Models
- NETL REE/Coal Database

Previously, each dataset required custom code to load and parse. The `cmm_data` package provides a unified API with:
- Consistent data structures (pandas DataFrames)
- Automatic handling of special codes (W, NA, ranges)
- Built-in caching for performance
- Visualization utilities

### Key Deliverables

| Deliverable | Description |
|-------------|-------------|
| Python Package | 62 files, pip-installable |
| 7 Data Loaders | USGS, OECD, OSTI, GA, NETL |
| Visualizations | Production charts, time series, maps |
| Documentation | README, Sphinx docs, examples |
| CI/CD | GitHub Actions for tests, docs, PyPI |
| GitHub Release | v0.1.0 with wheel attached |

---

## 2. Package Architecture

### Directory Structure

```
cmm_data/
├── pyproject.toml              # Package configuration (PEP 621)
├── setup.py                    # Backward compatibility
├── MANIFEST.in                 # Source distribution rules
├── LICENSE                     # MIT License
├── .gitignore                  # Git ignore patterns
├── .pre-commit-config.yaml     # Code quality hooks
│
├── README.md                   # Main documentation (1,300+ lines)
├── QUICKSTART.md               # Quick start guide
├── QUICKSTART_COLLABORATORS.md # 5-minute collaborator guide
├── CONTRIBUTING.md             # Contribution guidelines
├── CHANGELOG.md                # Version history
├── RELEASE_NOTES.md            # v0.1.0 release notes
│
├── src/cmm_data/               # Source code
│   ├── __init__.py             # Package entry point
│   ├── config.py               # Configuration management
│   ├── catalog.py              # Data catalog functions
│   ├── exceptions.py           # Custom exceptions
│   ├── loaders/                # Data loader classes
│   ├── utils/                  # Utility functions
│   └── visualizations/         # Plotting functions
│
├── docs/                       # Sphinx documentation
├── examples/                   # Usage examples
├── scripts/                    # Build and test scripts
├── tests/                      # Unit tests
└── .github/                    # GitHub Actions workflows
```

### Module Design

```
cmm_data
├── __init__.py          # Exports convenience functions
├── config.py            # CMMDataConfig dataclass
├── catalog.py           # get_data_catalog(), list_commodities()
├── exceptions.py        # CMMDataError, DataNotFoundError
│
├── loaders/
│   ├── base.py          # Abstract BaseLoader class
│   ├── usgs_commodity.py
│   ├── usgs_ore.py
│   ├── osti_docs.py
│   ├── preprocessed.py
│   ├── ga_chronostrat.py
│   ├── netl_ree.py
│   └── oecd_supply.py
│
├── utils/
│   └── parsing.py       # parse_numeric_value(), parse_range()
│
└── visualizations/
    ├── commodity.py     # plot_world_production(), etc.
    ├── geospatial.py    # plot_deposit_locations()
    └── timeseries.py    # plot_critical_minerals_comparison()
```

### Design Patterns Used

1. **Abstract Base Class**: `BaseLoader` defines the interface for all data loaders
2. **Factory Pattern**: `load_usgs_commodity()` convenience function creates loaders
3. **Singleton Pattern**: Global `_config` instance for configuration
4. **Lazy Loading**: Loaders only read data when methods are called
5. **Caching**: Memory and disk caching with configurable TTL

---

## 3. Implementation Details

### 3.1 Package Configuration (pyproject.toml)

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "cmm-data"
version = "0.1.0"
description = "Critical Minerals Modeling data access library"
requires-python = ">=3.9"
dependencies = [
    "pandas>=2.0.0",
    "numpy>=1.24.0",
]

[project.optional-dependencies]
geo = ["geopandas>=0.14.0", "rasterio>=1.3.0", "fiona>=1.9.0"]
viz = ["matplotlib>=3.7.0", "plotly>=5.15.0"]
dev = ["pytest>=7.0.0", "ruff>=0.1.0", "pre-commit>=3.0.0"]
full = ["cmm-data[geo,viz,dev]"]
```

### 3.2 Configuration System (config.py)

The configuration system automatically detects data paths:

```python
def _find_data_root() -> Path:
    # 1. Check CMM_DATA_PATH environment variable
    env_path = os.environ.get("CMM_DATA_PATH")
    if env_path and Path(env_path).exists():
        return Path(env_path)

    # 2. Search parent directories for Globus_Sharing
    current = Path(__file__).resolve()
    for _ in range(10):
        current = current.parent
        if current.name == "Globus_Sharing":
            return current

    # 3. Check common paths
    common_paths = [
        Path.home() / "Globus_Sharing",
        Path("/data/cmm/Globus_Sharing"),
    ]
    for path in common_paths:
        if path.exists():
            return path

    return None
```

### 3.3 Base Loader Class (loaders/base.py)

```python
from abc import ABC, abstractmethod

class BaseLoader(ABC):
    dataset_name: str = "base"

    def __init__(self, config=None):
        self.config = config or get_config()
        self._cache = {}

    @abstractmethod
    def load(self, **kwargs) -> pd.DataFrame:
        """Load data and return DataFrame."""
        pass

    @abstractmethod
    def list_available(self) -> List[str]:
        """List available data items."""
        pass

    def describe(self) -> Dict[str, Any]:
        """Return dataset metadata."""
        return {
            "name": self.dataset_name,
            "available": self.list_available(),
        }
```

### 3.4 USGS Commodity Loader (loaders/usgs_commodity.py)

Key features:
- Loads world production and salient statistics
- Parses special USGS codes (W, NA, ranges)
- Provides commodity name lookup
- Gets top producers by production

```python
class USGSCommodityLoader(BaseLoader):
    dataset_name = "usgs_commodity"

    def load_world_production(self, commodity: str) -> pd.DataFrame:
        path = self.config.get_path("usgs") / "world" / f"mcs2023-{commodity}_world.csv"
        df = pd.read_csv(path)
        # Parse numeric columns
        for col in ['Prod_t_2021', 'Prod_t_est_2022', 'Reserves_t']:
            df[f'{col}_clean'] = df[col].apply(parse_numeric_value)
        return df

    def get_top_producers(self, commodity: str, top_n: int = 10) -> pd.DataFrame:
        df = self.load_world_production(commodity)
        df = df[~df['Country'].str.contains('World|total', case=False)]
        return df.nlargest(top_n, 'Prod_t_est_2022_clean')
```

### 3.5 Value Parsing Utilities (utils/parsing.py)

Handles USGS special codes:

```python
def parse_numeric_value(value) -> float:
    """Parse USGS values, handling special codes."""
    if pd.isna(value):
        return np.nan

    if isinstance(value, (int, float)):
        return float(value)

    value_str = str(value).strip()

    # Handle special codes
    if value_str.upper() in ('W', 'NA', 'N/A', '--', '—', ''):
        return np.nan

    # Handle ranges like ">50" or "<100"
    if value_str.startswith('>'):
        return float(value_str[1:].replace(',', ''))
    if value_str.startswith('<'):
        return float(value_str[1:].replace(',', ''))

    # Remove commas and convert
    return float(value_str.replace(',', ''))
```

### 3.6 Visualization Functions (visualizations/commodity.py)

```python
def plot_world_production(
    df: pd.DataFrame,
    commodity_name: str,
    top_n: int = 10,
    figsize: tuple = (12, 6),
    ax=None
):
    """Create bar chart of top producing countries."""
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    # Filter and sort data
    plot_df = df[~df['Country'].str.contains('World|total', case=False)]
    plot_df = plot_df.nlargest(top_n, 'Prod_t_est_2022_clean')

    # Create bar chart
    ax.barh(plot_df['Country'], plot_df['Prod_t_est_2022_clean'])
    ax.set_xlabel('Production (metric tons)')
    ax.set_title(f'{commodity_name} World Production (2022 est.)')

    return ax.figure
```

---

## 4. Files Created

### Source Code (19 files)

| File | Lines | Description |
|------|-------|-------------|
| `src/cmm_data/__init__.py` | ~150 | Package entry point, exports |
| `src/cmm_data/config.py` | ~180 | Configuration management |
| `src/cmm_data/catalog.py` | ~100 | Data catalog functions |
| `src/cmm_data/exceptions.py` | ~30 | Custom exception classes |
| `src/cmm_data/loaders/__init__.py` | ~20 | Loader exports |
| `src/cmm_data/loaders/base.py` | ~100 | Abstract base loader |
| `src/cmm_data/loaders/usgs_commodity.py` | ~250 | USGS commodity loader |
| `src/cmm_data/loaders/usgs_ore.py` | ~200 | USGS ore deposits loader |
| `src/cmm_data/loaders/osti_docs.py` | ~150 | OSTI documents loader |
| `src/cmm_data/loaders/preprocessed.py` | ~180 | Corpus loader |
| `src/cmm_data/loaders/ga_chronostrat.py` | ~150 | GA 3D model loader |
| `src/cmm_data/loaders/netl_ree.py` | ~120 | NETL REE loader |
| `src/cmm_data/loaders/oecd_supply.py` | ~200 | OECD supply chain loader |
| `src/cmm_data/utils/__init__.py` | ~10 | Utility exports |
| `src/cmm_data/utils/parsing.py` | ~80 | Value parsing functions |
| `src/cmm_data/visualizations/__init__.py` | ~20 | Visualization exports |
| `src/cmm_data/visualizations/commodity.py` | ~150 | Commodity charts |
| `src/cmm_data/visualizations/geospatial.py` | ~100 | Map visualizations |
| `src/cmm_data/visualizations/timeseries.py` | ~120 | Time series plots |

### Documentation (17 files)

| File | Description |
|------|-------------|
| `README.md` | Comprehensive documentation (1,300+ lines) |
| `QUICKSTART.md` | Quick start guide |
| `QUICKSTART_COLLABORATORS.md` | 5-minute collaborator guide |
| `CONTRIBUTING.md` | Contribution guidelines |
| `CHANGELOG.md` | Version history |
| `RELEASE_NOTES.md` | v0.1.0 release notes |
| `DISTRIBUTION.md` | Wheel building guide |
| `SESSION_LOG.md` | Development session log |
| `docs/conf.py` | Sphinx configuration |
| `docs/index.rst` | Sphinx main page |
| `docs/installation.rst` | Installation guide |
| `docs/quickstart.rst` | Quick start (RST) |
| `docs/configuration.rst` | Configuration guide |
| `docs/datasets.rst` | Dataset descriptions |
| `docs/api/modules.rst` | API reference |
| `docs/api/loaders.rst` | Loader API |
| `docs/api/visualizations.rst` | Visualization API |

### Scripts (9 files)

| File | Description |
|------|-------------|
| `scripts/run_all_tests.py` | Comprehensive test runner |
| `scripts/verify_installation.py` | Installation verification |
| `scripts/setup_complete.sh` | Full setup automation |
| `scripts/build_wheel.py` | Cross-platform wheel builder |
| `scripts/publish_pypi.sh` | PyPI publishing script |
| `scripts/demo_recording.py` | GIF demo recording script |
| `scripts/demo.tape` | VHS tape for GIF generation |
| `scripts/quickstart.py` | Quick start demo |

### CI/CD (3 workflows)

| File | Triggers | Actions |
|------|----------|---------|
| `.github/workflows/test.yml` | Push, PR | Tests, lint, docs build |
| `.github/workflows/docs.yml` | Push to main | Deploy to GitHub Pages |
| `.github/workflows/publish.yml` | Release | Publish to PyPI |

---

## 5. Setup Instructions

### 5.1 Development Setup

```bash
# Clone repository
git clone https://github.com/Redliana/cmm-data.git
cd cmm-data

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install with all dependencies
pip install -e ".[full]"

# Install pre-commit hooks
pip install pre-commit
pre-commit install
```

### 5.2 Quick Install (Users)

```bash
# From PyPI
pip install cmm-data

# With visualization support
pip install "cmm-data[viz]"

# From GitHub
pip install git+https://github.com/Redliana/cmm-data.git
```

### 5.3 Configuration

```python
import cmm_data

# Auto-detection (usually works)
config = cmm_data.get_config()

# Manual configuration
cmm_data.configure(data_root="/path/to/Globus_Sharing")

# Or via environment variable
export CMM_DATA_PATH=/path/to/Globus_Sharing
```

---

## 6. Testing

### 6.1 Test Structure

```
tests/
├── __init__.py
└── test_basic.py      # Unit tests for core functionality
```

### 6.2 Running Tests

```bash
# Run comprehensive test suite
python scripts/run_all_tests.py

# Run with pytest
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=cmm_data --cov-report=html
```

### 6.3 Test Categories

The test suite covers 8 categories:

1. **Import Tests** - Package imports correctly
2. **Configuration Tests** - Config loads and validates
3. **Catalog Tests** - Data catalog functions work
4. **Loader Initialization** - All 7 loaders initialize
5. **Data Loading** - Data loads correctly from files
6. **Utility Tests** - Parsing functions work
7. **OECD Tests** - OECD-specific functionality
8. **Visualization Tests** - Viz imports work

### 6.4 Expected Output

```
============================================================
 CMM Data Package Test Suite
============================================================

1. Import Tests
  [PASS] Import cmm_data
  [PASS] Version is 0.1.0
  [PASS] All exports available

... (25 tests total)

============================================================
 Test Summary: 25/25 passed
============================================================
```

---

## 7. Documentation

### 7.1 Documentation Structure

```
docs/
├── conf.py              # Sphinx configuration
├── index.rst            # Main page
├── Makefile             # Build automation
├── requirements.txt     # Doc dependencies
├── installation.rst
├── quickstart.rst
├── configuration.rst
├── datasets.rst
├── contributing.rst
├── changelog.rst
└── api/
    ├── modules.rst
    ├── loaders.rst
    ├── visualizations.rst
    └── utilities.rst
```

### 7.2 Building Documentation

```bash
# Install doc dependencies
pip install -r docs/requirements.txt

# Build HTML
cd docs
make html

# View
open _build/html/index.html
```

### 7.3 Sphinx Configuration

Key features:
- **Theme**: sphinx_rtd_theme (Read the Docs)
- **Extensions**: autodoc, napoleon, intersphinx, viewcode
- **Docstring Style**: Google/NumPy (via napoleon)
- **Markdown Support**: myst_parser

---

## 8. CI/CD Pipeline

### 8.1 Test Workflow (.github/workflows/test.yml)

Triggers on push/PR to main:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11', '3.12']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install -e ".[viz]"
      - run: pytest tests/ -v

  lint:
    runs-on: ubuntu-latest
    steps:
      - run: ruff check src/

  docs:
    runs-on: ubuntu-latest
    steps:
      - run: make html
```

### 8.2 Documentation Deployment (.github/workflows/docs.yml)

Deploys to GitHub Pages on push to main:

```yaml
jobs:
  build:
    steps:
      - run: make html
      - uses: actions/upload-pages-artifact@v3

  deploy:
    uses: actions/deploy-pages@v4
```

### 8.3 PyPI Publishing (.github/workflows/publish.yml)

Publishes on GitHub release:

```yaml
jobs:
  build:
    steps:
      - run: python -m build
      - run: twine check dist/*

  publish:
    steps:
      - uses: pypa/gh-action-pypi-publish@release/v1
```

### 8.4 Pre-commit Hooks

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    hooks:
      - id: ruff          # Linting
      - id: ruff-format   # Formatting

  - repo: https://github.com/pre-commit/mirrors-mypy
    hooks:
      - id: mypy          # Type checking

  - repo: https://github.com/PyCQA/bandit
    hooks:
      - id: bandit        # Security checks
```

---

## 9. Publishing

### 9.1 Building the Wheel

```bash
# Install build tool
pip install build

# Build wheel and source distribution
python -m build

# Output:
# dist/cmm_data-0.1.0-py3-none-any.whl
# dist/cmm_data-0.1.0.tar.gz
```

### 9.2 Publishing to PyPI

```bash
# Install twine
pip install twine

# Check package
twine check dist/*

# Upload to PyPI
twine upload dist/*

# Username: __token__
# Password: pypi-YOUR-TOKEN
```

### 9.3 Creating GitHub Release

```bash
# Create tag
git tag -a v0.1.0 -m "CMM Data v0.1.0 - Initial Release"
git push origin v0.1.0

# Create release with assets
gh release create v0.1.0 \
  --title "CMM Data v0.1.0 - Initial Release" \
  --notes-file .github/RELEASE_TEMPLATE.md \
  dist/cmm_data-0.1.0-py3-none-any.whl \
  dist/cmm_data-0.1.0.tar.gz
```

---

## 10. Usage Examples

### 10.1 Basic Usage

```python
import cmm_data

# View available datasets
catalog = cmm_data.get_data_catalog()
print(catalog)

# List commodities
commodities = cmm_data.list_commodities()
critical = cmm_data.list_critical_minerals()

# Load data
df = cmm_data.load_usgs_commodity("lithi", "world")
print(df[['Country', 'Prod_t_est_2022', 'Reserves_t']])
```

### 10.2 Using Loaders

```python
from cmm_data import USGSCommodityLoader, USGSOreDepositsLoader

# USGS Commodity
loader = USGSCommodityLoader()
top_producers = loader.get_top_producers("lithi", top_n=10)
commodity_name = loader.get_commodity_name("lithi")  # "Lithium"

# Ore Deposits
ore_loader = USGSOreDepositsLoader()
ree_samples = ore_loader.get_ree_samples()
la_stats = ore_loader.get_element_statistics("La")
```

### 10.3 Visualizations

```python
import cmm_data
from cmm_data.visualizations.commodity import (
    plot_world_production,
    plot_production_timeseries,
    plot_import_reliance
)

# Load data
df = cmm_data.load_usgs_commodity("lithi", "world")

# Create chart
fig = plot_world_production(df, "Lithium", top_n=10)
fig.savefig("lithium_producers.png")
```

### 10.4 Document Corpus

```python
from cmm_data import PreprocessedCorpusLoader

loader = PreprocessedCorpusLoader()

# Get statistics
stats = loader.get_corpus_stats()
print(f"Documents: {stats['total_documents']}")

# Search
results = loader.search("lithium extraction", limit=10)

# Iterate
for doc in loader.iter_documents():
    print(doc['title'])
```

---

## 11. Troubleshooting

### Common Issues

**Issue: "Data not found" error**

```python
import cmm_data
cmm_data.configure(data_root="/correct/path/to/Globus_Sharing")
```

**Issue: pyproject.toml error during install**

Fixed by correcting the `[project.optional-dependencies]` section syntax.

**Issue: GitHub workflow permission denied**

```bash
gh auth login --scopes workflow
```

**Issue: Permission denied running scripts**

```bash
chmod +x scripts/setup_complete.sh
```

---

## 12. Future Development

### Planned for v0.2.0

- [ ] Integration with pymrio for ICIO table analysis
- [ ] Additional visualization types (heatmaps, Sankey diagrams)
- [ ] Data export to Parquet and HDF5 formats
- [ ] Automated data updates from USGS APIs
- [ ] Additional loaders for new data sources

### Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Make changes and add tests
4. Run tests: `pytest tests/`
5. Run linter: `ruff check src/`
6. Commit: `git commit -m "Add feature"`
7. Push: `git push origin feature/my-feature`
8. Open Pull Request

---

## Summary

This development session created a complete, production-ready Python package for accessing critical minerals data. The package includes:

- **7 data loaders** covering major data sources
- **80+ mineral commodities** with production and reserves data
- **Visualization module** for quick data exploration
- **Comprehensive documentation** for users and developers
- **CI/CD pipeline** for automated testing and deployment
- **Published to PyPI** for easy installation

**Repository:** https://github.com/Redliana/cmm-data
**PyPI:** https://pypi.org/project/cmm-data/
**Install:** `pip install cmm-data`

---

*CMM Data v0.1.0 - Pacific Northwest National Laboratory*
