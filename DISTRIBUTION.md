# CMM Data Distribution Guide

This guide explains how to build and distribute the `cmm_data` package to collaborators.

## Building the Wheel Package

### Option 1: Using the Build Script (Recommended)

```bash
cd /path/to/Globus_Sharing/cmm_data

# Make script executable (first time only)
chmod +x scripts/build_wheel.sh

# Run the build
./scripts/build_wheel.sh

# Or use Python directly
python3 scripts/build_wheel.py
```

### Option 2: Manual Build

```bash
cd /path/to/Globus_Sharing/cmm_data

# Install build tools
pip install --upgrade pip build wheel

# Build the package
python -m build

# Output will be in dist/
ls dist/
# cmm_data-0.1.0-py3-none-any.whl
# cmm_data-0.1.0.tar.gz
```

## Distribution Files

After building, you'll have two files in `dist/`:

| File | Description | Use Case |
|------|-------------|----------|
| `cmm_data-0.1.0-py3-none-any.whl` | Wheel package | Fast installation |
| `cmm_data-0.1.0.tar.gz` | Source distribution | Fallback/verification |

## Sharing with Collaborators

### What to Send

1. **The wheel file**: `cmm_data-0.1.0-py3-none-any.whl`
2. **Data access**: Collaborators need access to `Globus_Sharing/` data directory

### Collaborator Setup Instructions

Send these instructions to collaborators:

```markdown
## CMM Data Setup

### 1. Get Data Access
Request access to the Globus_Sharing directory from the CMM team.

### 2. Install the Package
```bash
pip install cmm_data-0.1.0-py3-none-any.whl
```

### 3. Configure Data Path
```bash
# Set environment variable
export CMM_DATA_PATH=/path/to/Globus_Sharing

# Or configure in Python
python -c "import cmm_data; cmm_data.configure(data_root='/path/to/Globus_Sharing')"
```

### 4. Verify Installation
```python
import cmm_data
print(cmm_data.get_data_catalog())
```
```

## Installation Options for Collaborators

### Basic Installation

```bash
pip install cmm_data-0.1.0-py3-none-any.whl
```

### With Visualization Support

```bash
pip install cmm_data-0.1.0-py3-none-any.whl
pip install matplotlib plotly
```

### With Geospatial Support

```bash
pip install cmm_data-0.1.0-py3-none-any.whl
pip install geopandas rasterio fiona
```

### Full Installation

```bash
pip install cmm_data-0.1.0-py3-none-any.whl
pip install matplotlib plotly geopandas rasterio fiona
```

## Data Directory Structure

Collaborators need access to this directory structure:

```
Globus_Sharing/
├── USGS_Data/
│   ├── world/           # World production CSV files
│   └── salient/         # Salient statistics CSV files
├── USGS_Ore_Deposits/   # Ore deposits database
├── OSTI_retrieval/      # OSTI documents
├── Data/
│   └── preprocessed/    # LLM corpus (unified_corpus.jsonl)
├── GA_149923_Chronostratigraphic/  # GA 3D model
├── NETL_REE_Coal/       # NETL geodatabase
└── OECD_Supply_Chain_Data/  # OECD/IEA data
```

## Versioning

To release a new version:

1. Update version in `pyproject.toml`:
   ```toml
   version = "0.2.0"
   ```

2. Update version in `src/cmm_data/__init__.py`:
   ```python
   __version__ = "0.2.0"
   ```

3. Rebuild:
   ```bash
   python scripts/build_wheel.py
   ```

## Troubleshooting

### Build Fails

```bash
# Ensure build tools are installed
pip install --upgrade pip build wheel setuptools

# Clean and retry
rm -rf dist/ build/ *.egg-info src/*.egg-info
python -m build
```

### Import Fails After Installation

```bash
# Check installation
pip show cmm-data

# Reinstall
pip uninstall cmm-data
pip install cmm_data-0.1.0-py3-none-any.whl --force-reinstall
```

### Data Not Found

```python
import cmm_data

# Check current config
print(cmm_data.get_config().data_root)

# Reconfigure
cmm_data.configure(data_root="/correct/path/to/Globus_Sharing")

# Validate
print(cmm_data.get_config().validate())
```

## PyPI Publishing (Future)

To publish to PyPI (if desired):

```bash
# Install twine
pip install twine

# Upload to TestPyPI first
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

## Contact

For distribution questions, contact the CMM team at PNNL.
