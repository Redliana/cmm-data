# CMM Data Quick Start Guide

This guide will help you get started with the `cmm_data` package in under 5 minutes.

## Step 1: Install

```bash
# Navigate to the Globus_Sharing directory
cd /path/to/Globus_Sharing

# Create a virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate

# Install the package
pip install -e cmm_data

# Or with visualization support
pip install -e "cmm_data[viz]"
```

## Step 2: Verify

```bash
python cmm_data/scripts/verify_installation.py
```

You should see output like:
```
============================================================
 CMM Data Installation Verification
============================================================

1. Checking package import...
  [OK] cmm_data import: version 0.1.0

2. Checking configuration...
  [OK] Data root: /path/to/Globus_Sharing

3. Checking dataset availability...
  [OK] usgs_commodity: USGS Mineral Commodity Summaries
  [OK] usgs_ore: USGS Ore Deposits Database
  ...
```

## Step 3: Use

### Python Script

```python
import cmm_data

# See what's available
print(cmm_data.get_data_catalog())

# Load lithium data
df = cmm_data.load_usgs_commodity("lithi", "world")
print(df)

# Get top cobalt producers
loader = cmm_data.USGSCommodityLoader()
top = loader.get_top_producers("cobal", top_n=5)
print(top)
```

### Jupyter Notebook

```bash
# Install Jupyter if needed
pip install jupyter

# Open the tutorial notebook
jupyter notebook cmm_data/examples/cmm_data_tutorial.ipynb
```

## Step 4: Explore

### Available Commodity Codes

```python
import cmm_data

# All commodities
commodities = cmm_data.list_commodities()
print(commodities)
# ['abras', 'alumi', 'antim', 'arsen', ...]

# Critical minerals only
critical = cmm_data.list_critical_minerals()
print(critical)
# ['alumi', 'antim', 'arsen', 'barit', ...]
```

### Common Commodity Codes

| Code | Mineral |
|------|---------|
| `lithi` | Lithium |
| `cobal` | Cobalt |
| `nicke` | Nickel |
| `raree` | Rare Earths |
| `graph` | Graphite |
| `coppe` | Copper |
| `manga` | Manganese |
| `plati` | Platinum Group |

### Data Types

```python
# World production data
df = cmm_data.load_usgs_commodity("lithi", "world")

# US salient statistics (time series)
df = cmm_data.load_usgs_commodity("lithi", "salient")
```

## Step 5: Visualize

```python
import cmm_data
from cmm_data.visualizations.commodity import plot_world_production
import matplotlib.pyplot as plt

# Load data
df = cmm_data.load_usgs_commodity("lithi", "world")

# Create chart
fig = plot_world_production(df, "Lithium", top_n=8)
plt.show()

# Save to file
fig.savefig("lithium_production.png")
```

## Common Tasks

### Get Top Producers

```python
loader = cmm_data.USGSCommodityLoader()
top = loader.get_top_producers("lithi", top_n=10)
print(top[['Country', 'Prod_t_est_2022', 'Reserves_t']])
```

### Search Documents

```python
loader = cmm_data.PreprocessedCorpusLoader()
results = loader.search("lithium extraction")
print(results)
```

### Export to CSV

```python
df = cmm_data.load_usgs_commodity("lithi", "world")
df.to_csv("lithium_data.csv", index=False)
```

### Compare Critical Minerals

```python
loader = cmm_data.USGSCommodityLoader()

for code in ['lithi', 'cobal', 'nicke']:
    df = loader.load_salient_statistics(code)
    print(f"{loader.get_commodity_name(code)}: NIR = {df.iloc[-1]['NIR_pct']}")
```

## Getting Help

```python
import cmm_data

# Package documentation
help(cmm_data)

# Loader documentation
help(cmm_data.USGSCommodityLoader)

# List all functions
dir(cmm_data)
```

## Next Steps

1. **Run the examples**: `python cmm_data/examples/basic_usage.py`
2. **Open the tutorial notebook**: `examples/cmm_data_tutorial.ipynb`
3. **Read the full documentation**: `README.md`
4. **Explore visualization examples**: `examples/visualization_examples.py`
