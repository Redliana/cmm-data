# USGS Mineral Commodity Summaries Data Download Guide

This guide explains how to download USGS MCS data for CMM-relevant commodities for years 2020-2024.

## Overview

The `download_usgs_mcs.py` script downloads and extracts USGS Mineral Commodity Summaries data from the ScienceBase catalog for CMM-relevant commodities.

## CMM Commodities Included

Based on the Gold Q&A methodology, the script extracts data for:

- **Heavy REE** (Dysprosium, Terbium)
- **Light REE** (Neodymium, Praseodymium)  
- **Cobalt**
- **Lithium**
- **Gallium**
- **Graphite**
- **Nickel**
- **Copper**
- **Germanium**
- **Manganese**
- **Titanium**
- **Platinum Group Metals** (Platinum, Palladium, Rhodium, etc.)
- **Tungsten**

## ScienceBase Catalog Item IDs

You need the ScienceBase catalog item ID for each year. Currently known:

- **2024**: `65a6e45fd34e5af967a46749` ✓ (provided)
- **2023**: Need to find
- **2022**: Need to find
- **2021**: Need to find
- **2020**: Need to find

### Finding Catalog Item IDs

1. Visit: https://www.sciencebase.gov/catalog/
2. Search for: "Mineral Commodity Summaries [YEAR]"
3. Click on the data release item
4. The item ID is in the URL: `https://www.sciencebase.gov/catalog/item/{ITEM_ID}`

Alternatively, visit the USGS data release page:
- https://www.usgs.gov/data/us-geological-survey-mineral-commodity-summaries-2025-data-release
- Look for links to previous years' data releases

## Usage

### Download Single Year

```bash
python3 download_usgs_mcs.py --year 2024 --item-id 65a6e45fd34e5af967a46749
```

### Download All Years (once you have all item IDs)

First, update the `SCIENCEBASE_ITEMS` dictionary in the script with all item IDs, then:

```bash
python3 download_usgs_mcs.py --output-dir usgs_mcs_data
```

### Custom Output Directory

```bash
python3 download_usgs_mcs.py --year 2024 --item-id 65a6e45fd34e5af967a46749 --output-dir my_data
```

## Output Structure

```
usgs_mcs_data/
├── 2024/
│   ├── salient.zip (downloaded)
│   ├── world.zip (downloaded)
│   ├── salient/ (extracted)
│   └── world/ (extracted)
├── cmm_extracted/
│   └── 2024/
│       ├── heavy_ree_mcs2024-raree_salient.csv
│       ├── lithium_mcs2024-lithium_salient.csv
│       └── ... (other CMM commodities)
└── download_summary.json
```

## Data Files

Each commodity has two types of files:
- **Salient files**: U.S. statistics (production, imports, exports, consumption, prices)
- **World files**: World production statistics by country

## Data Structure

The salient CSV files contain columns like:
- `DataSource`: MCS year (e.g., "MCS2024")
- `Commodity`: Commodity name
- `Year`: Year (2020-2024)
- `USprod_t`: U.S. production (tonnes)
- `Imports_t`: Imports (tonnes)
- `Exports_t`: Exports (tonnes)
- `Consump_t`: Consumption (tonnes)
- `Price_dt`: Price (dollars per tonne)
- `Employment_num`: Employment numbers
- `NIR_pct`: Net Import Reliance (percentage)

## Notes

- The script automatically extracts CMM-relevant commodities from all downloaded files
- Files are organized by year and commodity category
- The download summary JSON file tracks what was downloaded
- If a year's catalog item ID is not found, you'll need to manually download from the USGS website

## References

- USGS MCS 2024: https://www.sciencebase.gov/catalog/item/65a6e45fd34e5af967a46749
- USGS MCS Main Page: https://www.usgs.gov/centers/national-minerals-information-center/mineral-commodity-summaries
- ScienceBase Catalog: https://www.sciencebase.gov/catalog/

