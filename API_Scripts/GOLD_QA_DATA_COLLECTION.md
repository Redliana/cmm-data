# Gold Q&A Data Collection Guide

This guide explains how to use the `pull_gold_qa_data.py` script to collect UN Comtrade trade flow data for the CMM Gold Q&A methodology.

## Purpose

The `pull_gold_qa_data.py` script systematically collects trade flow data from the UN Comtrade API based on the requirements specified in `CMM_LLM_Baseline_Gold_QA_Methodology.md`. Specifically, it focuses on:

- **Sub-Domain**: Trade Flows (Q-TF) - 10 questions total
- **Commodities**: All 10 priority commodity groups
- **Years**: 2020-2024 (covers both Stratum A and Stratum B temporal requirements)
- **Country Pairs**: Key bilateral relationships (USA-CHN, DRC-CHN, AUS-CHN, etc.)

## Methodology Alignment

Based on Section 4.2 of the methodology document, the following commodities have Trade Flow (Q-TF) questions:

| Commodity | Q-TF Questions | Key Countries | HS Codes |
|-----------|----------------|---------------|----------|
| Heavy REE | 1 | USA, CHN | 2846, 280530 |
| Cobalt | 2 | USA, CHN, COD (DRC) | 8105, 282200 |
| Lithium | 1 | USA, CHN, AUS | 253090, 283691, 282520 |
| Gallium | 1 | USA, CHN | 811292 |
| Graphite | 1 | USA, CHN | 250410, 380110 |
| Light REE | 1 | USA, CHN | 2846, 280530 |
| Nickel | 1 | USA, CHN, IDN | 7502, 7501 |
| Copper | 1 | USA, CHN | 7402, 7403 |
| Other | 1 | USA, CHN | (varies) |

## Prerequisites

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Get UN Comtrade API key**:
   - Register at: https://comtradedeveloper.un.org/apis
   - Set as environment variable:
     ```bash
     export UN_COMTRADE_API_KEY=your_api_key_here
     ```

## Usage

### Basic Usage

Collect all trade flow data for Gold Q&A requirements:

```bash
python3 pull_gold_qa_data.py --output-dir gold_qa_data
```

### With Custom API Key

```bash
python3 pull_gold_qa_data.py --api-key YOUR_KEY --output-dir gold_qa_data
```

### Preview Mode (Testing)

For testing without an API key (limited to 500 records per query):

```bash
# Note: Preview mode requires API modifications - use main query script instead
python3 un_comtrade_query.py --reporter USA --partner CHN --commodity 2846 --year 2023 --preview
```

## Output Structure

The script creates an output directory with:

```
gold_qa_data/
├── collection_summary.json          # Summary of all collections
├── heavy_ree_trade_data.csv         # Heavy REE trade data
├── cobalt_trade_data.csv            # Cobalt trade data
├── lithium_trade_data.csv           # Lithium trade data
├── gallium_trade_data.csv           # Gallium trade data
├── graphite_trade_data.csv          # Graphite trade data
├── light_ree_trade_data.csv         # Light REE trade data
├── nickel_trade_data.csv            # Nickel trade data
└── copper_trade_data.csv            # Copper trade data
```

### Collection Summary

The `collection_summary.json` file contains metadata about the collection:

```json
{
  "collection_date": "2025-12-28T...",
  "methodology_document": "CMM_LLM_Baseline_Gold_QA_Methodology.md",
  "focus": "Trade Flow questions (Q-TF sub-domain)",
  "years_queried": [2020, 2021, 2022, 2023, 2024],
  "commodities": [
    {
      "name": "Cobalt",
      "total_records": 1234,
      "filepath": "gold_qa_data/cobalt_trade_data.csv",
      "queries_executed": 45
    },
    ...
  ]
}
```

### Data Files

Each CSV file contains columns including:
- Standard UN Comtrade fields (trade values, quantities, etc.)
- `commodity_name`: Name of the commodity
- `hs_code`: HS code used for the query
- `query_year`: Year of the data

## Query Strategy

The script uses the following strategy:

1. **Commodity Coverage**: Iterates through all commodities with Q-TF questions
2. **HS Code Coverage**: Queries all relevant HS codes for each commodity
3. **Country Pairs**: Queries key bilateral relationships:
   - USA ↔ CHN (bidirectional)
   - Producer → CHN (e.g., AUS → CHN for lithium, COD → CHN for cobalt)
   - USA → ALL (USA imports from all partners)
   - CHN → ALL (China exports to all partners)
4. **Time Coverage**: Queries all years 2020-2024
5. **Trade Flow**: Queries both imports and exports ('both')

## Rate Limiting

The UN Comtrade API has rate limits:
- **With API key**: 500 calls/day; up to 100,000 records/call
- **Preview mode**: No key needed, but limited to 500 records/call

The script includes:
- 0.5 second delay between queries
- Duplicate query prevention
- Query logging

## Expected Runtime

For a full collection:
- **Commodities**: ~8 commodities (those with Q-TF questions)
- **HS codes per commodity**: 1-3 codes
- **Country pairs per commodity**: 3-5 pairs
- **Years**: 5 years (2020-2024)
- **Trade flows**: 2 (import + export)

**Total queries**: ~8 commodities × 2 HS codes × 4 pairs × 5 years × 2 flows ≈ **640 queries**

At 0.5 seconds per query: **~5-6 minutes** (excluding API processing time)

**Note**: With 500 calls/day limit, this may require multiple days or a premium API key.

## Troubleshooting

### No Data Returned

- Check that HS codes are correct for the commodity
- Verify country codes (use ISO 3-letter codes)
- Some country pairs may have no trade data for certain commodities

### API Rate Limit Errors

- The script respects rate limits with delays
- If you hit daily limits, run over multiple days
- Consider obtaining a premium API key for higher limits

### Import Errors

- Ensure `un_comtrade_query.py` is in the same directory
- Verify all dependencies are installed: `pip install -r requirements.txt`

## Next Steps

After collecting the data:

1. **Review collection summary**: Check `collection_summary.json` for completeness
2. **Validate data**: Review sample records from each commodity file
3. **Use for Q&A construction**: Reference the methodology document for question requirements
4. **Cross-reference with other sources**: Combine with USGS MCS data for comprehensive coverage

## Related Files

- `un_comtrade_query.py`: Core query functionality
- `example_usage.py`: Examples of using the query tools
- `CMM_LLM_Baseline_Gold_QA_Methodology.md`: Full methodology specification
- `CMM_API_MCP_Analysis.md`: API and data source analysis

## References

- UN Comtrade API: https://comtradeplus.un.org/
- UN Comtrade Developer Portal: https://comtradedeveloper.un.org/apis
- Methodology Document: `CMM_LLM_Baseline_Gold_QA_Methodology.md`

