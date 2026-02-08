# UN Comtrade API Query Tool for Critical Minerals and Materials (CMM)

This directory contains Python scripts to query the UN Comtrade API for trade flow data related to critical minerals and materials, including rare earth elements, lithium, cobalt, graphite, gallium, and germanium.

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install directly:

```bash
pip install comtradeapicall pandas openpyxl
```

### 2. Get an API Key

Register for a free API key at the [UN Comtrade Developer Portal](https://comtradedeveloper.un.org/apis).

### 3. Set Your API Key

Option 1: Set as environment variable (recommended):

```bash
export UN_COMTRADE_API_KEY=your_api_key_here
```

Option 2: Pass it directly as a command-line argument (see usage below).

## Usage

### Command-Line Interface

#### Basic Query

Query trade data between two countries for a specific commodity:

```bash
python un_comtrade_query.py --reporter USA --partner CHN --commodity 2846 --year 2023
```

#### Using Commodity Names

Use predefined CMM commodity names instead of HS codes:

```bash
python un_comtrade_query.py --reporter USA --partner CHN --commodity-name REE_compounds --year 2023
```

#### Query Specific Trade Flow

Query only imports or exports:

```bash
python un_comtrade_query.py --reporter USA --partner CHN --commodity 2846 --year 2023 --flow import
```

#### Save Results to File

Save query results to CSV, JSON, or Excel:

```bash
python un_comtrade_query.py --reporter USA --partner CHN --commodity 2846 --year 2023 --output results.csv
```

#### Preview Mode (No API Key)

Test queries without an API key (limited to 500 records):

```bash
python un_comtrade_query.py --reporter USA --partner CHN --commodity 2846 --year 2023 --preview
```

#### List Available Commodities

See all available CMM commodity names and HS codes:

```bash
python un_comtrade_query.py --list-commodities
```

### Python API

You can also use the `ComtradeQuery` class directly in your Python scripts:

```python
from un_comtrade_query import ComtradeQuery

# Initialize with API key
query = ComtradeQuery(api_key='your_api_key')
# Or use environment variable
query = ComtradeQuery()  # Reads from UN_COMTRADE_API_KEY

# Query trade data
df = query.query_trade_data(
    reporter='USA',
    partner='CHN',
    commodity_code='2846',  # REE compounds
    year=2023,
    trade_flow='both'  # 'import', 'export', or 'both'
)

# Query using commodity name
df = query.query_cmm_commodity(
    commodity_name='REE_compounds',
    reporter='USA',
    partner='CHN',
    year=2023
)

# Save results
query.save_results(df, 'output.csv', format='csv')
```

See `example_usage.py` for more detailed examples.

## Available CMM Commodities

The script includes predefined HS codes for the following CMM commodities:

| Commodity Name | HS Code | Description |
|---------------|---------|-------------|
| `REE_compounds` | 2846 | Rare earth compounds |
| `REE_metals` | 280530 | Rare earth metals |
| `Lithium_ores` | 253090 | Lithium ores/carbonate |
| `Lithium_carbonate` | 283691 | Lithium carbonate |
| `Lithium_hydroxide` | 282520 | Lithium hydroxide |
| `Cobalt` | 8105 | Cobalt and articles |
| `Cobalt_oxides` | 282200 | Cobalt oxides |
| `Graphite_natural` | 250410 | Natural graphite |
| `Graphite_artificial` | 380110 | Artificial graphite |
| `Gallium_Germanium` | 811292 | Gallium and Germanium |

## API Rate Limits

- **With API key**: 500 calls/day; up to 100,000 records per call
- **Preview mode**: No API key needed, but limited to 500 records per call

## Parameters

### Required Parameters

- `reporter`: ISO 3-letter country code for the reporting country (e.g., 'USA', 'CHN')
- `partner`: ISO 3-letter country code for the partner country (e.g., 'USA', 'CHN', 'ALL' for all partners)
- `commodity_code` or `commodity_name`: HS commodity code or predefined commodity name
- `year`: Year of trade data (e.g., 2023)

### Optional Parameters

- `trade_flow`: 'import', 'export', or 'both' (default: 'both')
- `preview`: Use preview API mode (no key needed, 500 records max)

## Output Format

The query returns a pandas DataFrame with trade statistics including:
- Trade flow direction (import/export)
- Trade values and quantities
- Reporter and partner countries
- Commodity codes
- Year
- Additional metadata fields

## References

- UN Comtrade API Documentation: https://comtradeplus.un.org/
- UN Comtrade Developer Portal: https://comtradedeveloper.un.org/apis
- Python Package: https://pypi.org/project/comtradeapicall/

## Notes

- HS codes are based on UNCTAD mapping for CMM commodities
- Country codes should be ISO 3-letter codes (e.g., USA, CHN, DEU)
- Year parameter should be a 4-digit year (e.g., 2023)
- Use 'ALL' as partner to get data for all trading partners

