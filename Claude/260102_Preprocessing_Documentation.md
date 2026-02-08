Data Analysis for LLM Fine-Tuning

  Overview

  | Category                      | Files | Total Size | Format             |
  |-------------------------------|-------|------------|--------------------|
  | MCS 2025 Industry Trends      | 14    | ~200KB     | CSV, XML           |
  | Salient Commodity Data        | 170   | ~1.5MB     | CSV (85), XML (85) |
  | World Data Release            | 2     | ~150KB     | CSV, XML           |
  | USGS Mineral Resource Data    | 5     | ~17MB      | GeoJSON, TXT, XLSX |
  | USGS Materials Commodity PDFs | 10    | ~63MB      | PDF                |
  | Documentation/Code            | 3     | ~300KB     | MD, TXT            |

  ---
  Dataset Details & Preprocessing Required

  1. MCS 2025 Industry Trends (Mineral_Industry_Trends_And_Statistics_MCS_2025/)

  - Content: Critical minerals statistics, import reliance, state rankings, economic trends
  - Format: Well-structured CSV with headers
  - Preprocessing:
    - Handle special values: W (withheld), NA, E (net exporter)
    - Parse numeric ranges like "<100,000" and ">75"
    - Convert to JSONL with semantic descriptions (e.g., "Cobalt has 76% net import reliance from Norway")

  2. Salient Commodity Data (Salient_Commodity_Data_Release_Grouped_MCS_2025/)

  - Content: 85 commodities with salient statistics + metadata
  - Format: CSV pairs with XML metadata per commodity
  - Preprocessing:
    - Merge CSV data with XML metadata (abstracts, keywords, descriptions)
    - Extract commodity-specific facts: production, imports, reserves
    - Create Q&A pairs from the structured data

  3. World Production Data (World_Data_Release_MCS_2025/)

  - Content: Global production by country, commodity, year
  - Format: CSV with 5,000+ rows covering all commodities
  - Preprocessing:
    - Pivot data for country-commodity comparisons
    - Generate narrative statements about production rankings
    - Handle notes columns and estimate flags

  4. USGS Mineral Resource Database (MRDS) (USGS/Mineral_Resource_Data/)

  - Content: 2,500+ REE mineral deposit records with geology, location, production history
  - Format: Tab-delimited TXT (1.1MB), GeoJSON (16MB), XLSX
  - Preprocessing:
    - Parse 50+ columns including: deposit type, ore minerals, gangue, geology, references
    - Clean long reference strings and geological descriptions
    - Extract structured facts about mineral occurrences
    - Convert coordinates to location descriptions

  5. USGS Materials Commodity Supply PDFs (USGS/Materials_Commodity_Supply/)

  - Content: Annual Mineral Commodity Summaries 2020-2024 (full reports + appendixes)
  - Format: PDF (~63MB total, 10 files)
  - Preprocessing:
    - OCR extraction using Mistral OCR (same pipeline as OSTI documents)
    - Extract commodity chapters individually
    - Parse tables for production/import/export data
    - Extract narrative descriptions and analysis

  ---
  Recommended Preprocessing Pipeline

  1. CSV/Structured Data → JSONL
     - Parse and clean tabular data
     - Generate natural language statements
     - Create Q&A training pairs

  2. XML Metadata → Context enrichment
     - Extract abstracts, keywords, citations
     - Merge with corresponding data files

  3. GeoJSON/MRDS → Geological knowledge base
     - Convert deposit records to text descriptions
     - Create location-based queries

  4. PDFs → OCR + Text extraction
     - Use existing Mistral OCR pipeline
     - Extract by commodity section
     - Analyze charts/figures

  ---
  Estimated Effort

  | Task                            | Complexity | Notes                                  |
  |---------------------------------|------------|----------------------------------------|
  | CSV parsing & JSONL conversion  | Low        | Standard pandas workflow               |
  | XML metadata extraction         | Low        | ElementTree parsing                    |
  | MRDS geological data cleaning   | Medium     | Many columns, reference cleanup        |
  | PDF OCR extraction              | Medium     | ~63MB, 10 files, use existing pipeline |
  | Q&A pair generation             | Medium     | Requires template design               |
  | Data validation & deduplication | Low        | Cross-check sources                    |

  Would you like me to start implementing the preprocessing pipeline for any of these datasets?

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
> Yes, start with the CSV data preprocessing                                                                                                         ↵ send
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  ⏵⏵ accept edits on (shift+tab to cycle)                                                                              Context left until auto-compact: 3%

---

Preprocessing Complete

  All data preprocessing tasks have been completed. Here's the summary:

  Unified Corpus Statistics

  | Metric           | Value   |
  |------------------|---------|
  | Total Documents  | 3,298   |
  | Total Characters | 897,290 |
  | Corpus Size      | 3.9 MB  |

  Data Sources Processed

  | Source                       | Documents | Description                                                  |
  |------------------------------|-----------|--------------------------------------------------------------|
  | MCS 2025 Industry Trends     | 470       | Production, employment, import reliance, prices, consumption |
  | MCS 2025 Salient Commodities | 425       | 85 commodities x 5 years (2020-2024)                         |
  | MCS 2025 World Production    | 1,016     | 76 commodities, 153 countries                                |
  | USGS MRDS REE Deposits       | 1,387     | Mineral deposit records from 38 countries                    |

  Output Files

  All files in /Users/wash198/Documents/Projects/Science_Projects/MPII_CMM/LLM_Fine_Tuning/Data/preprocessed/:

  - unified_corpus.jsonl - Combined corpus (3.9 MB)
  - corpus_summary.json - Full statistics and metadata
  - Individual JSONL files per data source with summaries

  Content Types

  - Mineral deposit records: 1,387
  - World production data: 1,016
  - Commodity salient statistics: 425
  - Consumption changes: 152
  - Import reliance: 64
  - Critical minerals end use: 50
  - State production: 50
    - 9 other types

  Pending for Future Processing

  - USGS MCS PDFs (2020-2024): 10 files, ~63MB - available for OCR when needed

  The corpus is ready for the next phase when you've finished gathering additional data sources.

---

Documentation Complete

  I've created comprehensive documentation for scientific publication and GitHub release:

  Documentation Files

  | File               | Size   | Purpose                                               |
  |--------------------|--------|-------------------------------------------------------|
  | README.md          | 4.7 KB | Quick start guide, data source overview, usage        |
  | METHODOLOGY.md     | 8.5 KB | Detailed preprocessing methodology for publications   |
  | DATA_DICTIONARY.md | 11 KB  | Field-level documentation for all output files        |
  | CHANGELOG.md       | 2.9 KB | Version history tracking                              |
  | LICENSE            | 1.5 KB | MIT for code, public domain attribution for USGS data |
  | requirements.txt   | 447 B  | Dependencies (standard library only)                  |
  | validate_corpus.py | 2.4 KB | Integrity validation script                           |

  Key Documentation Features

  For Scientific Publications (METHODOLOGY.md):
  - Abstract and introduction
  - Data source descriptions with DOIs
  - Pipeline architecture diagram
  - Special value handling table
  - Quality assurance methodology
  - Reproducibility instructions
  - Limitations section
  - BibTeX citations

  For GitHub Release (README.md):
  - Quick start usage
  - Data source summary table
  - Document schema definition
  - Citation templates

  For Developers (DATA_DICTIONARY.md):
  - Complete field-level documentation
  - Content type taxonomy
  - Parsed value object specifications
  - Enumerated value lists

  Validation Results

  All validations passed!
  - 6,596 documents validated (including unified corpus)
  - 0 invalid documents
  - 0 duplicate IDs

  Next Steps for GitHub Release

  1. Update author/institution in LICENSE and citations
  2. Add your GitHub repository URL to README.md
  3. Consider adding example Jupyter notebooks for data exploration
  4. Add CI/CD workflow (.github/workflows/) for automated validation

---

> Set up the GitHub repo structure 

⏺ Bash(ls -la /Users/wash198/Documents/Projects/Science_Projects/MPII_CMM/LLM_Fine_Tuning/)
  ⎿  total 40                                            
     drwxr-xr-x  12 wash198  staff    384 Dec 31 12:24 .
     drwxr-xr-x  40 wash198  staff   1280 Dec 28 14:53 ..
     … +10 lines (ctrl+o to expand)

⏺ Write(~/Documents/Projects/Science_Projects/MPII_CMM/LLM_Fine_Tuning/README.md)
  ⎿  Wrote 134 lines to ../../../../../../../../../../Documents/Projects/Science_Projects/MPII_CMM/LLM_Fine_Tuning/README.md                         
      1 # Critical Minerals and Materials LLM Fine-Tuning
      2 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
      3 [![Data: USGS](https://img.shields.io/badge/Data-USGS%20Public%20Domain-blue.svg)](https://www.usgs.gov/)
      4 [![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
      5 A comprehensive toolkit for fine-tuning Large Language Models (LLMs) on Critical Minerals and Materials (CMM) domain knowledge. This reposito
        ry provides data preprocessing pipelines, fine-tuning workflows, and evaluation benchmarks for creating domain-specialized LLMs.
      6 ## Overview
     … +124 lines (ctrl+o to expand)

⏺ Write(~/Documents/Projects/Science_Projects/MPII_CMM/LLM_Fine_Tuning/.gitignore)
  ⎿  Wrote 131 lines to ../../../../../../../../../../Documents/Projects/Science_Projects/MPII_CMM/LLM_Fine_Tuning/.gitignore
      1 # Byte-compiled / optimized / DLL files
      2 __pycache__/
      3 *.py[cod]
      4 *$py.class
      5 # C extensions
      6 *.so
      7 # Distribution / packaging
      8 .Python
     … +121 lines (ctrl+o to expand)

⏺ Write(~/Documents/Projects/Science_Projects/MPII_CMM/LLM_Fine_Tuning/LICENSE)
  ⎿  Wrote 38 lines to ../../../../../../../../../../Documents/Projects/Science_Projects/MPII_CMM/LLM_Fine_Tuning/LICENSE
      1 MIT License
      2 Copyright (c) 2025 [Author/Institution]
      3 Permission is hereby granted, free of charge, to any person obtaining a copy
      4 of this software and associated documentation files (the "Software"), to deal
      5 in the Software without restriction, including without limitation the rights
      6 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
      7 copies of the Software, and to permit persons to whom the Software is
      8 furnished to do so, subject to the following conditions:
     … +28 lines (ctrl+o to expand)

⏺ Write(~/Documents/Projects/Science_Projects/MPII_CMM/LLM_Fine_Tuning/CONTRIBUTING.md)
  ⎿  Wrote 210 lines to ../../../../../../../../../../Documents/Projects/Science_Projects/MPII_CMM/LLM_Fine_Tuning/CONTRIBUTING.md                   
      1 # Contributing to CMM LLM Fine-Tuning
      2 Thank you for your interest in contributing to the Critical Minerals and Materials LLM Fine-Tuning project! This document provides guidelines
         for contributing.
      3 ## Table of Contents
      4 - [Code of Conduct](#code-of-conduct)
      5 - [How to Contribute](#how-to-contribute)
      6 - [Development Setup](#development-setup)
      7 - [Pull Request Process](#pull-request-process)
     … +200 lines (ctrl+o to expand)

⏺ Bash(mkdir -p /Users/wash198/Documents/Projects/Science_Projects/MPII_CMM/LLM_Fine_Tuning/.github/workflows
      /Users/wash198/Documents/Projects/Science_Projects/MPII_C…)
  ⎿  (No content)

⏺ Write(~/Documents/Projects/Science_Projects/MPII_CMM/LLM_Fine_Tuning/.github/workflows/validate.yml)
  ⎿  Wrote 57 lines to ../../../../../../../../../../Documents/Projects/Science_Projects/MPII_CMM/LLM_Fine_Tuning/.github/workflows/validate.yml
      1 name: Validate Corpus
      2 on:
      3   push:
      4     branches: [ main, develop ]
      5     paths:
      6       - 'Data/preprocessed/**'
      7   pull_request:
      8     branches: [ main ]
      9     paths:
     … +47 lines (ctrl+o to expand)

⏺ Write(~/Documents/Projects/Science_Projects/MPII_CMM/LLM_Fine_Tuning/.github/workflows/preprocess.yml)
  ⎿  Wrote 73 lines to ../../../../../../../../../../Documents/Projects/Science_Projects/MPII_CMM/LLM_Fine_Tuning/.github/workflows/preprocess.yml
      1 name: Preprocess Data
      2 on:
      3   workflow_dispatch:
      4     inputs:
      5       source:
      6         description: 'Data source to preprocess'
      7         required: true
      8         default: 'all'
      9         type: choice
     … +63 lines (ctrl+o to expand)

⏺ Write(~/Documents/Projects/Science_Projects/MPII_CMM/LLM_Fine_Tuning/.github/ISSUE_TEMPLATE/bug_report.md)
  ⎿  Wrote 43 lines to ../../../../../../../../../../Documents/Projects/Science_Projects/MPII_CMM/LLM_Fine_Tuning/.github/ISSUE_TEMPLATE/bug_report.md
      1 ---
      2 name: Bug Report
      3 about: Report a bug in the preprocessing pipeline or data
      4 title: '[BUG] '
      5 labels: bug
      6 assignees: ''
      7 ---
      8 ## Bug Description
      9 A clear and concise description of what the bug is.
     … +33 lines (ctrl+o to expand)

⏺ Write(~/Documents/Projects/Science_Projects/MPII_CMM/LLM_Fine_Tuning/.github/ISSUE_TEMPLATE/feature_request.md)
  ⎿  Wrote 32 lines to                                                                                                                                 
     ../../../../../../../../../../Documents/Projects/Science_Projects/MPII_CMM/LLM_Fine_Tuning/.github/ISSUE_TEMPLATE/feature_request.md
      1 ---
      2 name: Feature Request
      3 about: Suggest a new feature or enhancement
      4 title: '[FEATURE] '
      5 labels: enhancement
      6 assignees: ''
      7 ---
      8 ## Feature Description
      9 A clear and concise description of the feature you'd like.
     … +22 lines (ctrl+o to expand)

⏺ Write(~/Documents/Projects/Science_Projects/MPII_CMM/LLM_Fine_Tuning/.github/ISSUE_TEMPLATE/data_source_request.md)
  ⎿  Wrote 65 lines to                                                                                                                       
     ../../../../../../../../../../Documents/Projects/Science_Projects/MPII_CMM/LLM_Fine_Tuning/.github/ISSUE_TEMPLATE/data_source_request.md
      1 ---
      2 name: New Data Source Request
      3 about: Suggest a new data source for inclusion
      4 title: '[DATA] '
      5 labels: data-source
      6 assignees: ''
      7 ---
      8 ## Data Source Information
     … +55 lines (ctrl+o to expand)

⏺ Write(~/Documents/Projects/Science_Projects/MPII_CMM/LLM_Fine_Tuning/.github/PULL_REQUEST_TEMPLATE.md)
  ⎿  Wrote 38 lines to ../../../../../../../../../../Documents/Projects/Science_Projects/MPII_CMM/LLM_Fine_Tuning/.github/PULL_REQUEST_TEMPLATE.md
      1 ## Description
      2 Brief description of the changes in this PR.
      3 ## Type of Change
      4 - [ ] Bug fix (non-breaking change that fixes an issue)
      5 - [ ] New feature (non-breaking change that adds functionality)
      6 - [ ] New data source (adds preprocessing for new data)
      7 - [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
      8 - [ ] Documentation update
      9 - [ ] Refactoring (no functional changes)
