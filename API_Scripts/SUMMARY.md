# UN Comtrade API Query Tools - Summary

This directory contains a complete toolkit for querying UN Comtrade API data for Critical Minerals and Materials (CMM) trade flows, specifically designed to support the Gold Q&A methodology framework.

## Files Created

### Core Scripts

1. **`un_comtrade_query.py`** (13 KB)
   - Main query class: `ComtradeQuery`
   - Command-line interface for ad-hoc queries
   - Includes all CMM HS codes (REE, Lithium, Cobalt, Graphite, Gallium, Germanium, Nickel, Copper)
   - Supports preview mode (no API key needed)
   - Export to CSV, JSON, Excel

2. **`pull_gold_qa_data.py`** (15 KB)
   - Systematic data collection for Gold Q&A methodology
   - Aligned with `CMM_LLM_Baseline_Gold_QA_Methodology.md` requirements
   - Focuses on Trade Flow (Q-TF) sub-domain questions
   - Collects data for 2020-2024 across all relevant commodities
   - Generates collection summaries

3. **`example_usage.py`** (5.8 KB)
   - Comprehensive examples of using the query tools
   - Shows various query patterns and use cases

### Documentation

4. **`README.md`** (4.7 KB)
   - Complete documentation for the query tools
   - Setup instructions, usage examples
   - API reference

5. **`GOLD_QA_DATA_COLLECTION.md`** (6.2 KB)
   - Detailed guide for collecting Gold Q&A data
   - Methodology alignment
   - Query strategy and output structure

6. **`QUICKSTART.md`** (1.9 KB)
   - Quick reference guide
   - Essential commands and examples

7. **`requirements.txt`**
   - Python package dependencies

## Key Features

### Commodity Coverage

All 10 priority commodities from the methodology:
- Heavy REE (Dy, Tb)
- Cobalt
- Lithium
- Gallium
- Graphite
- Light REE (Nd, Pr)
- Nickel
- Copper
- Germanium
- Other (Mn, Ti, PGM, W)

### Methodology Alignment

The `pull_gold_qa_data.py` script specifically implements:

- **Trade Flow (Q-TF) questions**: 10 questions across commodities
- **Years**: 2020-2024 (Stratum A and Stratum B coverage)
- **Key country pairs**: USA-CHN, DRC-CHN, AUS-CHN, etc.
- **HS code mapping**: All relevant codes per commodity

### Query Capabilities

- Bidirectional trade flows (imports and exports)
- Multiple HS codes per commodity
- Multiple country pairs
- Multi-year queries
- Rate limiting and error handling
- Data export and summarization

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Get API key**: Register at https://comtradedeveloper.un.org/apis

3. **Set environment variable**:
   ```bash
   export UN_COMTRADE_API_KEY=your_key_here
   ```

4. **Run data collection**:
   ```bash
   python3 pull_gold_qa_data.py --output-dir gold_qa_data
   ```

## Next Steps

1. **Review methodology document**: `CMM_LLM_Baseline_Gold_QA_Methodology.md`
2. **Run data collection**: Use `pull_gold_qa_data.py` to collect trade flow data
3. **Validate data**: Review collected data against methodology requirements
4. **Construct Q&A pairs**: Use collected data to answer Trade Flow questions

## Integration with Methodology

The tools support the methodology's requirements:

- **Section 4.2**: Commodity × Sub-Domain allocation (Q-TF column)
- **Section 3.3**: Temporal stratification (2020-2024 coverage)
- **Section 6.2**: Example Trade Flow questions (Q-TF sub-domain)
- **Section 7.1**: Source validation (UN Comtrade as Tier 2 source)

## Support

For questions or issues:
- Review documentation files
- Check UN Comtrade API documentation
- Refer to methodology document for requirements

