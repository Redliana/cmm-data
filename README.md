# Critical Minerals and Materials LLM Fine-Tuning

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Data: USGS](https://img.shields.io/badge/Data-USGS%20Public%20Domain-blue.svg)](https://www.usgs.gov/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A comprehensive toolkit for fine-tuning Large Language Models (LLMs) on Critical Minerals and Materials (CMM) domain knowledge. This repository provides data preprocessing pipelines, fine-tuning workflows, and evaluation benchmarks for creating domain-specialized LLMs.

## Overview

Critical minerals are essential for modern technologies including clean energy, electronics, and defense applications. This project aims to:

1. **Preprocess** heterogeneous USGS mineral data into LLM-ready formats
2. **Fine-tune** foundation models on CMM domain knowledge
3. **Evaluate** model performance with domain-specific benchmarks
4. **Deploy** specialized models for mineral resource applications

## Repository Structure

```
CMM-LLM-FineTuning/
├── Data/                          # Data sources and preprocessing
│   ├── preprocessed/              # Processed JSONL corpus
│   ├── Mineral_Industry_Trends/   # MCS 2025 trends data
│   ├── Salient_Commodity_Data/    # Per-commodity statistics
│   ├── World_Data_Release/        # Global production data
│   └── USGS/                      # MRDS and additional sources
├── Claude/                        # Claude/Anthropic integrations
│   └── cmm_mcp_server/           # MCP server for CMM tools
├── scripts/                       # Utility scripts
├── notebooks/                     # Jupyter notebooks for exploration
├── models/                        # Fine-tuned model checkpoints
├── evaluation/                    # Benchmark datasets and metrics
└── docs/                          # Additional documentation
```

## Quick Start

### Prerequisites

- Python 3.8+
- No external dependencies for preprocessing (uses standard library)

### Data Preprocessing

```bash
cd Data/preprocessed

# Process each data source
python3 preprocess_mcs2025_trends.py
python3 preprocess_salient_commodities.py
python3 preprocess_world_production.py
python3 preprocess_mrds.py

# Consolidate into unified corpus
python3 consolidate_corpus.py

# Validate output
python3 validate_corpus.py
```

### Corpus Statistics

| Metric | Value |
|--------|-------|
| Total Documents | 3,298 |
| Total Characters | 897,290 |
| Data Sources | 4 |
| Commodities Covered | 85+ |
| Countries Covered | 153 |

## Data Sources

### USGS Mineral Commodity Summaries 2025
- Industry production, employment, and economic trends
- Salient statistics for 85 mineral commodities
- World production data by country
- Import reliance and trade statistics

### USGS Mineral Resources Data System (MRDS)
- Geological deposit records
- Location coordinates and geological context
- Commodity associations and ore mineralogy

## Documentation

- [Data Preprocessing Methodology](Data/preprocessed/METHODOLOGY.md)
- [Data Dictionary](Data/preprocessed/DATA_DICTIONARY.md)
- [Changelog](Data/preprocessed/CHANGELOG.md)

## Citation

If you use this work in your research, please cite:

```bibtex
@misc{cmm_llm_finetuning_2025,
  title={Critical Minerals and Materials LLM Fine-Tuning Toolkit},
  author={[Authors]},
  year={2025},
  publisher={GitHub},
  url={https://github.com/[username]/CMM-LLM-FineTuning}
}
```

Please also cite the original USGS data sources:

```bibtex
@techreport{usgs_mcs2025,
  title={Mineral Commodity Summaries 2025},
  author={{U.S. Geological Survey}},
  year={2025},
  institution={U.S. Geological Survey},
  doi={10.3133/mcs2025}
}
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

- **Code**: MIT License - see [LICENSE](LICENSE)
- **USGS Data**: Public Domain (U.S. Government Work)

## Acknowledgments

- U.S. Geological Survey National Minerals Information Center
- [Additional acknowledgments]

## Contact

[Contact information]
