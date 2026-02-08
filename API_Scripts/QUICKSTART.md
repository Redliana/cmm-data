# Quick Start Guide: UN Comtrade API Query Tool

## 1. Installation

```bash
pip install -r requirements.txt
```

Or install directly:

```bash
pip install comtradeapicall pandas openpyxl
```

## 2. Get API Key

1. Register at: https://comtradedeveloper.un.org/apis
2. Copy your API key
3. Set it as environment variable:

```bash
export UN_COMTRADE_API_KEY=your_api_key_here
```

## 3. Quick Test (No API Key Required)

Test with preview mode (limited to 500 records):

```bash
python3 un_comtrade_query.py --reporter USA --partner CHN --commodity 2846 --year 2023 --preview
```

## 4. Example Queries

### Query REE compounds trade between USA and China

```bash
python3 un_comtrade_query.py \
  --reporter USA \
  --partner CHN \
  --commodity-name REE_compounds \
  --year 2023 \
  --output usa_china_ree_2023.csv
```

### Query Lithium ores exports from Australia to China

```bash
python3 un_comtrade_query.py \
  --reporter AUS \
  --partner CHN \
  --commodity-name Lithium_ores \
  --year 2023 \
  --flow export \
  --output aus_china_lithium_2023.csv
```

### List all available CMM commodities

```bash
python3 un_comtrade_query.py --list-commodities
```

## 5. Python Script Usage

```python
from un_comtrade_query import ComtradeQuery

# Initialize (reads API key from environment variable)
query = ComtradeQuery()

# Query trade data
df = query.query_cmm_commodity(
    commodity_name='REE_compounds',
    reporter='USA',
    partner='CHN',
    year=2023,
    trade_flow='both'
)

# Save results
query.save_results(df, 'results.csv')
print(df.head())
```

## Common Parameters

- **Reporter/Partner**: ISO 3-letter country codes (USA, CHN, AUS, etc.)
- **Commodity**: Use `--commodity-name` for predefined CMM commodities or `--commodity` for HS codes
- **Year**: 4-digit year (e.g., 2023)
- **Flow**: `import`, `export`, or `both` (default)

## Need Help?

See `README.md` for detailed documentation and `example_usage.py` for more examples.

