# CMM Fine-Tuning Pipeline

A local fine-tuning pipeline for Microsoft's **Phi-4 (14B)** model on Critical Minerals and Materials (CMM) domain knowledge, optimized for **Apple Silicon** using [MLX](https://github.com/ml-explore/mlx) and [mlx-lm](https://github.com/ml-explore/mlx-examples/tree/main/llms/mlx_lm).

This pipeline converts raw UN Comtrade trade data and USGS Mineral Commodity Summaries into structured Q&A training pairs, fine-tunes Phi-4 with LoRA adapters, evaluates against a gold-standard question set, and provides an interactive chat interface for the fine-tuned model.

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Directory Structure](#directory-structure)
- [Pipeline Stages](#pipeline-stages)
  - [1. Data Preparation](#1-data-preparation)
  - [2. Training](#2-training)
  - [3. Evaluation](#3-evaluation)
  - [4. Interactive Chat](#4-interactive-chat)
- [Raw Data Sources](#raw-data-sources)
- [Q&A Generation Details](#qa-generation-details)
- [Training Configurations](#training-configurations)
- [Evaluation Methodology](#evaluation-methodology)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

---

## Overview

The pipeline has four stages, each with a dedicated CLI command:

| Stage | CLI Command | Description |
|-------|-------------|-------------|
| Data Preparation | `cmm-prepare` | Load CSVs, generate Q&A pairs, split into train/valid/test JSONL |
| Training | `cmm-train` | Fine-tune Phi-4 with LoRA via mlx_lm |
| Evaluation | `cmm-evaluate` | Score model answers against gold-standard Q&A pairs |
| Chat | `cmm-chat` | Interactive REPL with the fine-tuned model |

**Current dataset statistics** (generated from raw data):

- **Source records**: 720 trade + 75 salient + 363 world production = **1,158 total**
- **Generated Q&A pairs**: **3,175** across 8 commodities and 17 template types
- **Train/Valid/Test split**: 2,698 / 318 / 159 (85/10/5%)
- **Commodities covered**: Cobalt, Copper, Gallium, Graphite, Heavy REE, Light REE, Lithium, Nickel
- **Complexity levels**: L1 (direct lookup, 2,422), L2 (derived/comparison, 689), L3 (analytical, 64)

## Requirements

- **Hardware**: Apple Silicon Mac (M1/M2/M3/M4) with at least 32GB unified memory. The bf16 config targets the M4 Max (128GB) and uses ~50GB during training. The 4-bit config can run on 32GB machines.
- **Software**: Python 3.11+ and [uv](https://docs.astral.sh/uv/) package manager.
- **Operating system**: macOS (required for MLX).

## Installation

All commands should be run from the `fine_tuning/` directory.

```bash
cd fine_tuning/

# Create virtual environment and install all dependencies
uv venv
uv sync

# Also install dev dependencies (pytest, ruff) for testing
uv sync --extra dev

# Verify installation
.venv/bin/python -c "from cmm_fine_tune.constants import COMMODITY_CONFIG; print('OK')"
```

After installation, the four CLI commands (`cmm-prepare`, `cmm-train`, `cmm-evaluate`, `cmm-chat`) are available via `.venv/bin/` or after activating the venv:

```bash
source .venv/bin/activate
cmm-prepare --help
```

### Dependencies

| Package | Purpose |
|---------|---------|
| `mlx`, `mlx-lm` | Apple Silicon ML framework + LLM fine-tuning/inference |
| `pandas` | CSV loading and data manipulation |
| `pydantic` | Data validation and serialization |
| `pyyaml` | Training config parsing |
| `rouge-score` | ROUGE-L evaluation metric |
| `nltk` | NLP utilities for scoring |
| `scikit-learn` | Stratified data splitting |
| `rich` | Terminal formatting for chat REPL |
| `jinja2` | Template rendering |

## Directory Structure

```
fine_tuning/
    pyproject.toml                          # Project config, dependencies, CLI entry points
    README.md                               # This file
    .gitignore                              # Ignores data/*.jsonl, adapters/, __pycache__

    configs/
        phi4_lora.yaml                      # bf16 config (M4 Max, ~50GB VRAM)
        phi4_8bit_lora.yaml                 # 8-bit quantized (less memory, larger batch)
        phi4_4bit_lora.yaml                 # 4-bit quantized (most memory efficient)

    src/cmm_fine_tune/
        __init__.py
        constants.py                        # Paths, commodity configs, model IDs, system prompt
        models.py                           # Pydantic models for all pipeline stages

        data/
            csv_loader.py                   # Load + normalize heterogeneous CSVs
            qa_generator.py                 # Template-based Q&A generation (21 templates)
            jsonl_formatter.py              # Convert QAPairs to mlx-lm chat JSONL
            splitter.py                     # Stratified train/valid/test splitting
            prepare.py                      # CLI: cmm-prepare

        training/
            config.py                       # Pydantic training config model + YAML loader
            train.py                        # CLI: cmm-train (wraps mlx_lm.lora)

        evaluation/
            gold_qa_loader.py               # Load gold Q&A pairs from JSONL
            inference.py                    # Batch inference via mlx_lm.load/generate
            scorer.py                       # Criteria-based + ROUGE-L scoring
            report.py                       # Aggregate metrics, JSON + markdown reports
            evaluate.py                     # CLI: cmm-evaluate

        inference/
            chat.py                         # CLI: cmm-chat (interactive REPL)

    data/                                   # Generated JSONL files (gitignored)
        train.jsonl                         # Training examples (2,698 lines)
        valid.jsonl                         # Validation examples (318 lines)
        test.jsonl                          # Test examples (159 lines)
        preparation_summary.json            # Statistics from data preparation

    gold_qa/                                # Gold-standard Q&A evaluation set (to be populated)
    adapters/                               # Trained LoRA adapters (gitignored)
    results/                                # Evaluation reports (kept in git)

    tests/
        test_csv_loader.py                  # 20 tests for CSV loading + parsing
        test_qa_generator.py                # 11 tests for Q&A generation
        test_jsonl_formatter.py             # 4 tests for JSONL formatting
        test_scorer.py                      # 11 tests for evaluation scoring
```

---

## Pipeline Stages

### 1. Data Preparation

The `cmm-prepare` command loads raw CSV files from the repository, generates template-based Q&A pairs, formats them as chat JSONL for mlx-lm, and splits them into train/valid/test sets.

#### Basic Usage

```bash
# Generate training data with default settings
cmm-prepare --output-dir data/

# Preview statistics without writing files
cmm-prepare --dry-run

# Verbose output showing per-commodity generation counts
cmm-prepare --output-dir data/ -v

# Custom split ratios and seed
cmm-prepare --output-dir data/ --train-ratio 0.80 --valid-ratio 0.10 --test-ratio 0.10 --seed 123
```

#### Full Options

```
cmm-prepare [-h] [--output-dir OUTPUT_DIR] [--seed SEED]
             [--train-ratio TRAIN_RATIO] [--valid-ratio VALID_RATIO]
             [--test-ratio TEST_RATIO] [--dry-run] [-v]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--output-dir` | `data/` | Directory for train.jsonl, valid.jsonl, test.jsonl |
| `--seed` | `42` | Random seed for reproducible splitting |
| `--train-ratio` | `0.85` | Fraction of data for training |
| `--valid-ratio` | `0.10` | Fraction of data for validation |
| `--test-ratio` | `0.05` | Fraction of data for testing |
| `--dry-run` | off | Print statistics without writing files |
| `-v, --verbose` | off | Debug-level logging |

#### What It Does

1. **Loads raw data** from `API_Scripts/`:
   - 8 trade CSVs from `gold_qa_data/` (UN Comtrade, 720 records)
   - 16 salient CSVs from `usgs_mcs_data/cmm_extracted/{2023,2024}/` (USGS MCS, 75 records)
   - 16 world production CSVs from the same directories (363 records)

2. **Generates Q&A pairs** using 17 template types across three categories:
   - Trade flow templates (6 types): total value, bilateral, quantity, YoY change, trade balance, import concentration
   - Salient statistics templates (6 types): net import reliance, US production, prices, trade volumes, price trends, production-consumption gap
   - World production templates (5 types): country production (2 years), reserves, country share, top producers, reserves-to-production ratio, production concentration (HHI)

3. **Formats as chat JSONL** with system/user/assistant messages per mlx-lm convention.

4. **Splits stratified** on commodity + complexity_level so each set has proportional representation.

5. **Writes summary** to `preparation_summary.json` with counts by commodity, complexity, and template.

#### Output Format

Each line in the JSONL files is a self-contained training example:

```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are an expert analyst specializing in critical minerals and materials..."
    },
    {
      "role": "user",
      "content": "What was the total value of Cobalt imports by United States in 2023?"
    },
    {
      "role": "assistant",
      "content": "In 2023, United States's total Cobalt imports were valued at $355.11 million (USD), based on UN Comtrade data for HS code 8105."
    }
  ]
}
```

---

### 2. Training

The `cmm-train` command wraps `mlx_lm.lora` with configuration management and adapter directory setup.

#### Prerequisites

1. Data preparation must be completed first (`cmm-prepare`).
2. The model weights will be downloaded automatically on first run from Hugging Face.

#### Basic Usage

```bash
# Fine-tune with the primary bf16 config (requires ~50GB memory)
cmm-train --config configs/phi4_lora.yaml

# Fine-tune with 8-bit quantization (lower memory, larger batch)
cmm-train --config configs/phi4_8bit_lora.yaml

# Fine-tune with 4-bit quantization (most memory efficient, ~16GB)
cmm-train --config configs/phi4_4bit_lora.yaml

# Resume from a checkpoint
cmm-train --config configs/phi4_lora.yaml --resume adapters/phi4_lora/

# Verbose logging
cmm-train --config configs/phi4_lora.yaml -v
```

#### Full Options

```
cmm-train [-h] --config CONFIG [--resume RESUME] [-v]
```

| Option | Description |
|--------|-------------|
| `--config` | **Required.** Path to YAML config file |
| `--resume` | Path to adapter checkpoint directory to resume from |
| `-v, --verbose` | Debug-level logging |

#### What It Does

1. Loads and validates the YAML config into a Pydantic `TrainingConfig` model.
2. Creates the adapter output directory.
3. Writes a resolved config YAML to the adapter directory for reproducibility.
4. Launches `python -m mlx_lm.lora --config <resolved_config>`.
5. The adapter weights are saved periodically (every `save_every` steps) and at completion.

#### Quick Smoke Test

To verify training works before committing to a full run:

```bash
python -m mlx_lm.lora \
  --model mlx-community/phi-4-8bit \
  --data data \
  --iters 10 \
  --batch-size 2 \
  --lora-layers 4 \
  --adapter-path adapters/smoke_test
```

This should run in a few minutes, show decreasing loss, and save an adapter to `adapters/smoke_test/`.

---

### 3. Evaluation

The `cmm-evaluate` command scores model outputs against gold-standard Q&A pairs using a criteria-based rubric plus ROUGE-L.

#### Prerequisites

1. A gold Q&A file must exist in JSONL format (one `GoldQAPair` per line).
2. A model must be available (base or fine-tuned with adapter).

#### Basic Usage

```bash
# Evaluate base model (no adapter)
cmm-evaluate \
  --model mlx-community/phi-4-bf16 \
  --gold-qa gold_qa/gold_qa_pairs.jsonl \
  --output results/baseline/

# Evaluate fine-tuned model
cmm-evaluate \
  --model mlx-community/phi-4-bf16 \
  --adapter adapters/phi4_lora/ \
  --gold-qa gold_qa/gold_qa_pairs.jsonl \
  --output results/phi4_lora/

# With 8-bit model and custom settings
cmm-evaluate \
  --model mlx-community/phi-4-8bit \
  --adapter adapters/phi4_8bit_lora/ \
  --gold-qa gold_qa/gold_qa_pairs.jsonl \
  --output results/phi4_8bit/ \
  --max-tokens 512 \
  --temperature 0.1
```

#### Full Options

```
cmm-evaluate [-h] [--model MODEL] [--adapter ADAPTER]
              --gold-qa GOLD_QA [--output OUTPUT]
              [--max-tokens MAX_TOKENS] [--temperature TEMPERATURE] [-v]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--model` | `mlx-community/phi-4-bf16` | MLX model ID or local path |
| `--adapter` | None | LoRA adapter directory |
| `--gold-qa` | **Required** | Path to gold Q&A JSONL file |
| `--output` | `results/` | Directory for evaluation reports |
| `--max-tokens` | `512` | Maximum tokens to generate per answer |
| `--temperature` | `0.1` | Sampling temperature (low for factual tasks) |
| `-v, --verbose` | off | Debug-level logging |

#### Gold Q&A Format

Each line in the gold Q&A JSONL file must have this schema:

```json
{
  "id": "L1_trade_001",
  "question": "What was the total value of cobalt imports by the United States in 2022?",
  "reference_answer": "In 2022, US cobalt imports totaled $434.5 million according to UN Comtrade data.",
  "complexity_level": "L1",
  "subdomain": "trade_flow",
  "commodity": "cobalt",
  "temporal_stratum": "B",
  "required_elements": ["434.5", "million", "2022", "cobalt"],
  "disqualifying_errors": ["lithium", "2021"]
}
```

| Field | Description |
|-------|-------------|
| `id` | Unique identifier |
| `question` | The question posed to the model |
| `reference_answer` | The ideal human-written answer |
| `complexity_level` | `L1` (lookup), `L2` (derived), `L3` (analytical), `L4` (synthesis) |
| `subdomain` | Category: `trade_flow`, `production`, `reserves`, `prices`, `supply_chain`, etc. |
| `commodity` | One of the 8 commodities |
| `temporal_stratum` | `A` (historical) or `B` (recent) |
| `required_elements` | List of strings that must appear in a correct answer |
| `disqualifying_errors` | List of strings that, if present, result in an automatic score of 0.0 |

#### Scoring Rubric

| Score | Criteria |
|-------|----------|
| **1.0** | All required elements present, no disqualifying errors |
| **0.75** | Minor omission or imprecision (e.g., rounding); >= 70% elements present |
| **0.50** | Partially correct; >= 40% of required elements |
| **0.25** | Minimal relevant content; some required elements present |
| **0.0** | Disqualifying error found, or completely irrelevant answer |

ROUGE-L is computed as a supplementary metric. When no required elements are specified, ROUGE-L is used as the primary scoring proxy.

#### Output

Evaluation produces two report files:

- `evaluation_report.json` -- Full machine-readable results with individual scores
- `evaluation_report.md` -- Human-readable markdown with summary tables broken down by complexity level, commodity, and subdomain

---

### 4. Interactive Chat

The `cmm-chat` command launches an interactive REPL for conversing with the model using `rich` terminal formatting.

#### Basic Usage

```bash
# Chat with the base model
cmm-chat --model mlx-community/phi-4-bf16

# Chat with a fine-tuned model
cmm-chat --model mlx-community/phi-4-bf16 --adapter adapters/phi4_lora/

# Use the 8-bit model for faster loading
cmm-chat --model mlx-community/phi-4-8bit --adapter adapters/phi4_8bit_lora/

# Adjust generation settings
cmm-chat --model mlx-community/phi-4-8bit --max-tokens 1024 --temperature 0.3
```

#### Full Options

```
cmm-chat [-h] [--model MODEL] [--adapter ADAPTER]
          [--max-tokens MAX_TOKENS] [--temperature TEMPERATURE]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--model` | `mlx-community/phi-4-bf16` | MLX model ID |
| `--adapter` | None | LoRA adapter directory |
| `--max-tokens` | `512` | Maximum response length |
| `--temperature` | `0.7` | Sampling temperature (higher = more creative) |

#### In-Chat Commands

| Command | Action |
|---------|--------|
| `quit` or `exit` | End the session |
| `clear` | Reset conversation context (keeps model loaded) |
| Ctrl+C or Ctrl+D | End the session |

The chat maintains conversation context (multi-turn), so follow-up questions reference prior exchanges. Use `clear` to start a fresh conversation without reloading the model.

---

## Raw Data Sources

The pipeline reads from two data sources that already exist in the repository:

### UN Comtrade Trade Data

**Location**: `API_Scripts/gold_qa_data/`

Eight CSV files with international trade flows collected via the UN Comtrade API:

| File | Commodity | Records |
|------|-----------|---------|
| `cobalt_trade_data.csv` | Cobalt (HS 8105) | 86 |
| `copper_trade_data.csv` | Copper (HS 7402, 7403) | 75 |
| `gallium_trade_data.csv` | Gallium (HS 811292) | 40 |
| `graphite_trade_data.csv` | Graphite (HS 250410, 250490) | 80 |
| `heavy_ree_trade_data.csv` | Heavy REE (HS 284690) | 80 |
| `light_ree_trade_data.csv` | Light REE (HS 284610) | 80 |
| `lithium_trade_data.csv` | Lithium (HS 282520, 283691, 253090) | 175 |
| `nickel_trade_data.csv` | Nickel (HS 7501, 7502, 281122) | 104 |

Each CSV has 45+ columns. Key fields used: `reporterCode`, `reporterDesc`, `partnerCode`, `partnerDesc`, `flowCode` (M/X), `refYear`, `cmdCode`, `primaryValue` (USD), `netWgt` (kg), `qty`, `commodity_name`, `hs_code`.

### USGS Mineral Commodity Summaries

**Location**: `API_Scripts/usgs_mcs_data/cmm_extracted/{2023,2024}/`

Two types of CSV per commodity per year:

**Salient statistics** (`*_salient.csv`): US-focused annual data including production, imports, exports, consumption, prices, stocks, and net import reliance. Each commodity has a **different column schema** (10-20 columns), handled via a flexible `fields: dict` model. Example columns for cobalt: `USprod_Mine_t, USprod_Secondary_t, Imports_t, Exports_t, Consump_Estimated_t, Price_Spot_dlb, Price_LME_dlb, NIR_pct`.

**World production** (`*_world.csv`): Country-level mine production and reserves. Columns: `Source, Country, Type, Prod_t_<year1>, Prod_t_est_<year2>, Prod_notes, Reserves_t, Reserves_notes`.

#### Special Values in USGS Data

The loader handles these non-standard values:
- `"W"` -- Data withheld to avoid disclosing proprietary information (skipped in Q&A generation)
- `">25"`, `">50"` -- Greater-than thresholds for net import reliance (parsed as the numeric value)
- `"Less than 1/2 unit"` -- Treated as missing
- `""` (empty string) -- Treated as missing
- `"2019.0"` -- Year stored as float string in some CSVs (parsed via `int(float(...))`)

---

## Q&A Generation Details

All Q&A pairs are **template-based** (not LLM-generated), ensuring every answer is traceable to exact source data values. Each `QAPair` stores a `source_data` dict for full provenance.

### Template Types

#### Trade Flow Templates (6 types)

| ID | Level | Description | Example Question |
|----|-------|-------------|------------------|
| `trade_total_value` | L1 | Total import/export value for a country-year | "What was the total value of Cobalt imports by United States in 2023?" |
| `trade_bilateral` | L1 | Bilateral trade between two countries | "How much did China export in Lithium to Japan in 2022?" |
| `trade_quantity` | L1 | Weight/quantity of trade flow | "What was the quantity of Nickel imports by Germany in 2021?" |
| `trade_yoy_change` | L2 | Year-over-year value change (%) | "How did US Cobalt imports from China change between 2021 and 2022?" |
| `trade_balance` | L2 | Net trade balance (imports vs exports) | "What was Japan's trade balance in Graphite in 2023?" |
| `trade_import_concentration` | L3 | Top import sources with shares | "Which countries were the largest sources of Lithium imports for US in 2023?" |

#### Salient Statistics Templates (6 types)

| ID | Level | Description | Example Question |
|----|-------|-------------|------------------|
| `salient_nir` | L1 | Net import reliance percentage | "What was the US net import reliance for Gallium in 2022?" |
| `salient_us_production` | L1 | US domestic production by type | "What was US Mine production of Cobalt in 2022?" |
| `salient_price` | L1 | Commodity prices by type | "What was the Spot price of Cobalt in 2022?" |
| `salient_trade_volume` | L1 | US import/export volumes (metric tons) | "What were the US Lithium imports in 2021?" |
| `salient_price_trend` | L2 | Price change between consecutive years | "How did the LME price of Nickel change from 2021 to 2022?" |
| `salient_prod_consump_gap` | L2 | Gap between US production and consumption | "What was the gap between US production and consumption of Copper in 2022?" |

#### World Production Templates (5 types)

| ID | Level | Description | Example Question |
|----|-------|-------------|------------------|
| `world_country_production_y1/y2` | L1 | Country production for a given year | "How much Cobalt did Congo (Kinshasa) produce in 2022?" |
| `world_reserves` | L1 | Country mineral reserves | "What are Australia's known Lithium reserves?" |
| `world_total_production` | L1 | Global production total | "What was total world Graphite production in 2022?" |
| `world_country_share` | L2 | Country's share of global production | "What share of global Cobalt production did Congo account for in 2022?" |
| `world_top_producers` | L2 | Top 3 producing countries | "Which countries were the top producers of Nickel in 2022?" |
| `world_reserves_production_ratio` | L2 | Reserve life in years | "What is Chile's reserves-to-production ratio for Lithium?" |
| `world_production_concentration` | L3 | HHI-based concentration analysis | "How concentrated is global Cobalt production in 2022?" |

### Generation Statistics

| Commodity | Trade | Salient | World | Total |
|-----------|-------|---------|-------|-------|
| Heavy REE | 170 | 195 | 112 | 477 |
| Light REE | 170 | 195 | 112 | 477 |
| Copper | 158 | 144 | 146 | 448 |
| Lithium | 287 | 45 | 82 | 414 |
| Graphite | 169 | 95 | 143 | 407 |
| Nickel | 197 | 113 | 90 | 400 |
| Cobalt | 180 | 48 | 116 | 344 |
| Gallium | 102 | 74 | 32 | 208 |
| **Total** | **1,433** | **909** | **833** | **3,175** |

---

## Training Configurations

Three pre-built YAML configs are provided, targeting different memory budgets:

### Config Comparison

| Config | Model | Precision | Batch Size | Memory Estimate | Recommended Hardware |
|--------|-------|-----------|------------|-----------------|---------------------|
| `phi4_lora.yaml` | `phi-4-bf16` | bf16 | 4 | ~50GB | M4 Max 128GB |
| `phi4_8bit_lora.yaml` | `phi-4-8bit` | 8-bit | 8 | ~30GB | M2/M3 Pro 36GB+ |
| `phi4_4bit_lora.yaml` | `phi-4-4bit` | 4-bit | 16 | ~16GB | M1/M2 32GB |

### Shared Hyperparameters

All configs share:
- **LoRA rank**: 16, alpha: 32, dropout: 0.05
- **LoRA layers**: 16 (of Phi-4's 40 layers)
- **Iterations**: 1,000 (with 100-step warmup)
- **Learning rate**: 1e-5 with cosine decay to 1e-7
- **Gradient checkpointing**: enabled
- **Max sequence length**: 2,048 tokens
- **Validation**: every 100 steps, 25 batches
- **Checkpointing**: every 200 steps

### Customizing Configs

Copy an existing config and modify it:

```bash
cp configs/phi4_8bit_lora.yaml configs/my_experiment.yaml
# Edit as needed, then:
cmm-train --config configs/my_experiment.yaml
```

Key parameters to tune:
- `iters`: More iterations for larger datasets (monitor validation loss for overfitting)
- `lora_layers`: More layers = more capacity, but slower and more memory
- `lora_parameters.rank`: Higher rank = more parameters (try 8, 16, 32)
- `batch_size`: Larger = faster per iteration but more memory
- `learning_rate`: Start with 1e-5, reduce if training is unstable

---

## Evaluation Methodology

The evaluation pipeline implements a **criteria-based scoring rubric** designed for factual CMM questions:

1. **Disqualifying error check**: If the generated answer contains any string from `disqualifying_errors`, score is 0.0 immediately (e.g., confusing cobalt with lithium).

2. **Required elements coverage**: Count what fraction of `required_elements` appear in the answer (case-insensitive, with numeric tolerance for comma-formatted numbers).

3. **Rubric mapping**: Coverage percentage maps to the 5-point scale (0.0, 0.25, 0.50, 0.75, 1.0).

4. **ROUGE-L supplementary**: Computed for all answers; used as primary metric when no required elements are specified.

Reports aggregate scores by:
- **Complexity level** (L1 through L4) -- to measure performance degradation on harder questions
- **Commodity** (8 commodities) -- to identify domain gaps
- **Subdomain** (trade_flow, production, reserves, etc.) -- to identify task-type weaknesses

---

## Testing

The test suite covers all pipeline components except training and inference (which require model downloads).

```bash
# Run all tests (46 tests)
.venv/bin/python -m pytest tests/ -v

# Run a specific test file
.venv/bin/python -m pytest tests/test_csv_loader.py -v
.venv/bin/python -m pytest tests/test_qa_generator.py -v
.venv/bin/python -m pytest tests/test_jsonl_formatter.py -v
.venv/bin/python -m pytest tests/test_scorer.py -v

# Run with coverage (if pytest-cov is installed)
.venv/bin/python -m pytest tests/ --cov=cmm_fine_tune --cov-report=term-missing
```

### Test Coverage

| Test File | Tests | What's Covered |
|-----------|-------|----------------|
| `test_csv_loader.py` | 20 | Numeric parsing (W, >25, NaN, etc.), trade/salient/world loading |
| `test_qa_generator.py` | 11 | All three generator categories, template IDs, total count, provenance |
| `test_jsonl_formatter.py` | 4 | Chat conversion, JSON escaping, file write/read |
| `test_scorer.py` | 11 | Element matching, rubric scores, disqualifying errors, ROUGE-L fallback |

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'cmm_fine_tune'`

The package isn't installed. Run `uv sync` from the `fine_tuning/` directory.

### `ValueError: could not convert string to float: ''`

This was a known issue with empty trailing rows in some salient CSVs. It has been fixed in the loader (empty Year rows are skipped). If you encounter this with new data, ensure the CSV doesn't have blank rows at the bottom.

### Out of memory during training

Use a more quantized config:
```bash
# Try 8-bit instead of bf16
cmm-train --config configs/phi4_8bit_lora.yaml

# Or 4-bit for maximum memory savings
cmm-train --config configs/phi4_4bit_lora.yaml
```

You can also reduce `batch_size`, `max_seq_length`, or `lora_layers` in the config.

### Model download is slow or fails

MLX models are downloaded from Hugging Face on first use. You can pre-download:
```bash
python -c "from huggingface_hub import snapshot_download; snapshot_download('mlx-community/phi-4-8bit')"
```

### Training loss is not decreasing

- Verify data looks correct: `head -1 data/train.jsonl | python -m json.tool`
- Try a lower learning rate (e.g., `5e-6`)
- Ensure `max_seq_length` is long enough for your examples (check with `python -c "import json; lines=open('data/train.jsonl').readlines(); print(max(len(l) for l in lines))"` for a rough character count)

### Tests fail with "CSV not found"

The tests load data from the repository's `API_Scripts/` directory. The path resolution in `constants.py` assumes the standard repo structure (`LLM_Fine_Tuning/Exp_Design/fine_tuning/src/cmm_fine_tune/constants.py`). If you've moved the `fine_tuning/` directory, update `REPO_ROOT` in `constants.py`.
