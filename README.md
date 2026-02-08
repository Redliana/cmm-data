# Critical Minerals and Materials LLM Fine-Tuning

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Data: USGS](https://img.shields.io/badge/Data-USGS%20Public%20Domain-blue.svg)](https://www.usgs.gov/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

A comprehensive toolkit for fine-tuning Large Language Models (LLMs) on Critical Minerals and Materials (CMM) domain knowledge. This repository provides data collection pipelines, a local fine-tuning workflow for Phi-4 on Apple Silicon, a gold-standard evaluation framework, and tooling for mapping scientific literature to structured evaluation benchmarks.

## Overview

Critical minerals are essential for modern technologies including clean energy, electronics, and defense applications. This project aims to:

1. **Collect** trade flow data (UN Comtrade) and mineral statistics (USGS MCS) for 8 critical commodities
2. **Generate** template-based Q&A training pairs (3,175 pairs) with full data provenance
3. **Fine-tune** Microsoft Phi-4 (14B) with LoRA adapters on Apple Silicon via MLX
4. **Evaluate** model performance against a 100-question gold-standard benchmark spanning 10 commodities, 10 knowledge subdomains, and 4 complexity levels
5. **Curate** the gold-standard evaluation set by mapping 1,133 OSTI journal articles to the 100-cell evaluation matrix using Vertex AI batch inference

## Repository Structure

```
LLM_Fine_Tuning/
├── Exp_Design/                        # Experiment design and core pipelines
│   ├── fine_tuning/                   #   Phi-4 LoRA fine-tuning pipeline (see its README)
│   │   ├── src/cmm_fine_tune/         #     Python package: data prep, training, eval, chat
│   │   ├── configs/                   #     LoRA YAML configs (bf16, 8-bit, 4-bit)
│   │   ├── tests/                     #     46 unit tests
│   │   └── README.md                  #     Full pipeline documentation
│   ├── batch_analysis/                #   Vertex AI batch analysis pipeline (see its README)
│   │   ├── config.py                  #     GCP config, paths, category mappings
│   │   ├── matrix_parser.py           #     Parse allocation matrix into 100 cells
│   │   ├── prepare_batch.py           #     Generate 1,133-line JSONL batch input
│   │   ├── submit_batch.py            #     Upload to GCS + submit Vertex AI job
│   │   ├── parse_results.py           #     Parse batch output + salvage truncated JSON
│   │   ├── generate_report.py         #     Markdown recommendation report
│   │   └── README.md                  #     Full pipeline documentation
│   ├── CMM_Gold_QA_Allocation_Matrix.md   # 100-cell evaluation matrix definition
│   └── CMM_LLM_Baseline_Gold_QA_Methodology.md  # Evaluation methodology
│
├── API_Scripts/                       # Data collection scripts
│   ├── un_comtrade_query.py           #   UN Comtrade API query tool
│   ├── gold_qa_data/                  #   8 trade CSVs (720 records, 8 commodities)
│   ├── usgs_mcs_data/                 #   USGS Mineral Commodity Summaries
│   │   └── cmm_extracted/{2023,2024}/ #     Salient + world production CSVs
│   └── README.md                      #   API tools documentation
│
├── OSTI_retrieval/                    # Scientific literature retrieval
│   ├── document_catalog.json          #   1,133 categorized OSTI journal articles
│   ├── osti_retrieval.py              #   OSTI search + download pipeline
│   └── pdfs/                          #   Downloaded PDFs (gitignored, ~6 GB)
│
├── OSTI_OCR_Extracted/                # OCR-processed article text (gitignored, ~315 MB)
│   ├── batch_output/                  #   106 JSON files with extracted text
│   └── search_index.db               #   TF-IDF search index
│
├── Claude/                            # Anthropic Claude integrations
│   └── cmm_mcp_server/               #   MCP server for CMM domain tools
│
├── Fine_Tuning_Corpus/                # Consolidated fine-tuning datasets (placeholder)
│
├── Aurora/                            # Google Aurora fine-tuning reference docs
├── Mindat/                            # Mindat.org API integration docs
├── OCR_Tests/                         # OCR validation test files
├── PNNL_Compute_Examples/             # HPC fine-tuning reference notebooks
│
├── .gitignore                         # Excludes PDFs, OCR data, venvs, model weights
├── CONTRIBUTING.md
├── LICENSE                            # MIT
└── README.md                          # This file
```

## Key Components

### Fine-Tuning Pipeline (`Exp_Design/fine_tuning/`)

A local fine-tuning pipeline for **Phi-4 (14B)** optimized for Apple Silicon using [MLX](https://github.com/ml-explore/mlx). Four CLI commands cover the full workflow:

| Stage | Command | Description |
|-------|---------|-------------|
| Data Preparation | `cmm-prepare` | Load CSVs, generate 3,175 Q&A pairs, split train/valid/test |
| Training | `cmm-train` | Fine-tune Phi-4 with LoRA via mlx-lm |
| Evaluation | `cmm-evaluate` | Score answers against gold-standard Q&A pairs |
| Chat | `cmm-chat` | Interactive REPL with the fine-tuned model |

**Current dataset**: 720 trade + 75 salient + 363 world production records = **3,175 Q&A pairs** across 8 commodities (Cobalt, Copper, Gallium, Graphite, Heavy REE, Light REE, Lithium, Nickel) at 3 complexity levels.

See [`Exp_Design/fine_tuning/README.md`](Exp_Design/fine_tuning/README.md) for installation, usage, training configs, and evaluation methodology.

### Gold Q&A Evaluation Framework (`Exp_Design/`)

A structured 100-question benchmark defined in [`CMM_Gold_QA_Allocation_Matrix.md`](Exp_Design/CMM_Gold_QA_Allocation_Matrix.md), distributed across:

- **10 commodities**: HREE, LREE, Cobalt, Lithium, Gallium, Graphite, Nickel, Copper, Germanium, Other (PGMs, Manganese, Tungsten)
- **10 knowledge subdomains**: Extraction Chemistry, Processing Metallurgy, Geological Occurrence, Production Statistics, Trade Flows, Economic Parameters, Policy/Regulatory, Bilateral/Multilateral, Cross-Commodity, Supply Chain Topology
- **4 complexity levels**: L1 (Factual), L2 (Relational), L3 (Inferential), L4 (Analytical)

The evaluation methodology is documented in [`CMM_LLM_Baseline_Gold_QA_Methodology.md`](Exp_Design/CMM_LLM_Baseline_Gold_QA_Methodology.md).

### Batch Analysis Pipeline (`Exp_Design/batch_analysis/`)

Uses **Gemini 2.5 Pro** via Vertex AI batch inference to analyze 1,133 OSTI journal articles and determine which papers are best suited as source material for each of the 100 gold Q&A evaluation pairs.

**Results** (2026-02-07 batch run):
- 1,106 / 1,133 papers successfully evaluated (97.6%)
- 387 papers recommended for gold Q&A creation
- 92 / 100 matrix cells covered (best score >= 3)
- 8 gap cells identified needing external source material

See [`Exp_Design/batch_analysis/README.md`](Exp_Design/batch_analysis/README.md) for the full pipeline documentation, design decisions, and results.

### Data Collection (`API_Scripts/`)

Scripts for querying the UN Comtrade API and downloading USGS Mineral Commodity Summaries. Collected data is stored in `gold_qa_data/` (trade flows) and `usgs_mcs_data/` (salient statistics, world production).

See [`API_Scripts/README.md`](API_Scripts/README.md) for setup and usage.

### Literature Retrieval (`OSTI_retrieval/`)

Pipeline for searching, downloading, and cataloging CMM-relevant journal articles from the DOE's OSTI database. The `document_catalog.json` file contains metadata for 1,133 papers categorized by commodity and knowledge subdomain.

## Quick Start

### Fine-Tuning Pipeline

```bash
cd Exp_Design/fine_tuning/

# Create venv and install dependencies
uv venv && uv sync

# Generate training data from raw CSVs
cmm-prepare --output-dir data/

# Fine-tune Phi-4 with LoRA (requires Apple Silicon, 32+ GB RAM)
cmm-train --config configs/phi4_4bit_lora.yaml

# Evaluate against gold Q&A set
cmm-evaluate --gold-qa gold_qa/gold_qa_pairs.jsonl --adapter adapters/phi4_4bit_lora/

# Interactive chat
cmm-chat --adapter adapters/phi4_4bit_lora/
```

### Batch Analysis Pipeline

```bash
cd Exp_Design/batch_analysis/

# Create venv and install dependencies
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Generate batch input, submit, parse, report
python prepare_batch.py
python submit_batch.py --monitor
python parse_results.py
python generate_report.py
```

Requires GCP authentication (`gcloud auth application-default login`) with access to project `rcgenai`.

## Commodities Covered

| Commodity | Code | Trade Data | Salient Stats | World Production | OSTI Papers |
|-----------|------|:----------:|:-------------:|:----------------:|:-----------:|
| Heavy REE | HREE | 80 records | Yes | Yes | 176 |
| Light REE | LREE | 80 records | Yes | Yes | 128 |
| Cobalt | CO | 86 records | Yes | Yes | 143 |
| Lithium | LI | 175 records | Yes | Yes | 115 |
| Gallium | GA | 40 records | Yes | Yes | 160 |
| Graphite | GR | 80 records | Yes | Yes | 70 |
| Nickel | NI | 104 records | Yes | Yes | 29 |
| Copper | CU | 75 records | Yes | Yes | 42 |
| Germanium | GE | -- | -- | -- | 29 |
| Other | OTH | -- | -- | -- | 51 |

## Data Sources

- **[UN Comtrade](https://comtradeplus.un.org/)**: International trade flows by HS commodity code, reporter, partner, and year
- **[USGS Mineral Commodity Summaries](https://www.usgs.gov/centers/national-minerals-information-center/mineral-commodity-summaries)**: US salient statistics (production, imports, exports, prices, net import reliance) and world mine production/reserves by country
- **[DOE OSTI](https://www.osti.gov/)**: Scientific and technical journal articles on critical minerals topics

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

Please also cite the original data sources:

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

- **Code**: MIT License -- see [LICENSE](LICENSE)
- **USGS Data**: Public Domain (U.S. Government Work)
- **UN Comtrade Data**: Subject to [UN Comtrade terms of use](https://comtradeplus.un.org/LegalAgreement)

## Acknowledgments

- U.S. Geological Survey National Minerals Information Center
- U.S. Department of Energy Office of Scientific and Technical Information (OSTI)
- United Nations Statistics Division (UN Comtrade)
- Pacific Northwest National Laboratory (PNNL)
