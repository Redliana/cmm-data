# Vertex AI Batch Analysis Pipeline: OSTI Paper-to-Gold-QA Mapping

## What This Pipeline Does

This pipeline uses Google Gemini 2.5 Pro (via Vertex AI batch inference) to analyze 1,133 OSTI journal articles and determine which papers are best suited for creating 100 gold-standard Q&A evaluation pairs for a Critical Minerals and Materials (CMM) knowledge benchmark.

### The Problem

We have two things:

1. **1,133 categorized OSTI journal articles** (`document_catalog.json`) -- each tagged with a commodity category (e.g., HREE, Cobalt, Lithium) or a knowledge subdomain (e.g., Policy/Regulatory, Supply Chain Topology).

2. **A 100-cell Gold Q&A Allocation Matrix** (`CMM_Gold_QA_Allocation_Matrix.md`) -- defining exactly 100 gold-standard questions distributed across 10 commodities, 10 subdomains, and 4 complexity levels (L1 Factual through L4 Analytical).

The question: *Which of the 1,133 papers should be used as source material for drafting each of the 100 gold Q&A pairs?*

Doing this manually would require a domain expert to read every abstract and mentally cross-reference it against each relevant matrix cell. Instead, we ask Gemini to do this at scale using the Vertex AI batch API, which provides 50% discounted pricing with ~24-hour turnaround.

### The Output

For each of the 100 matrix cells, a ranked list of the best-matching OSTI papers with:
- A relevance score (1-5)
- A justification explaining why the paper fits (or doesn't)
- A suggested question angle the paper could support
- Whether the paper has enough depth for L3/L4 (inferential/analytical) questions

This is compiled into a markdown recommendation report with coverage tables, per-cell rankings, and a gap analysis identifying cells that need additional source material.

---

## Directory Structure

```
batch_analysis/
    README.md               # This file
    config.py               # GCP config, paths, commodity/subdomain mappings
    matrix_parser.py        # Parse allocation matrix MD into data structures
    prepare_batch.py        # Generate JSONL batch input (1,133 requests)
    submit_batch.py         # Upload to GCS + submit Vertex AI batch job
    parse_results.py        # Download + parse batch output into recommendations
    generate_report.py      # Create markdown report mapping papers to Q&A cells
    requirements.txt        # google-genai, google-cloud-storage
    .gitignore              # Ignores output/, .venv/, __pycache__/
    .venv/                  # Python virtual environment (not committed)
    output/                 # Generated artifacts (not committed)
        batch_input.jsonl       # 1,133-line JSONL of Vertex AI requests
        job_metadata.json       # Submitted job name, URIs, timestamps
        batch_output_raw.jsonl  # Raw Vertex AI responses (after job completes)
        paper_evaluations.json  # Parsed per-paper evaluations
        recommendation_matrix.json  # Cell -> ranked papers mapping
        parse_stats.json        # Success/failure counts
        recommendation_report.md    # Final human-readable report
```

---

## How to Run the Pipeline

### Prerequisites

1. **GCP authentication**: You must have run `gcloud auth application-default login` with access to project `rcgenai`.

2. **Python virtual environment**: The pipeline uses a local venv to avoid polluting your system Python.

```bash
cd batch_analysis
source .venv/bin/activate    # activate the existing venv (already created)
```

If the venv doesn't exist yet:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Step-by-Step Execution

#### Step 1: Generate Batch Input

```bash
python prepare_batch.py              # generates output/batch_input.jsonl
python prepare_batch.py --dry-run    # preview stats without writing
```

This reads `document_catalog.json` and the allocation matrix, then generates one JSONL line per paper. Each line is a complete Vertex AI `GenerateContentRequest` asking Gemini to evaluate that paper against its relevant matrix cells.

#### Step 2: Submit Batch Job

```bash
python submit_batch.py               # upload to GCS + submit
python submit_batch.py --monitor     # submit + poll every 60s until done
```

This uploads `batch_input.jsonl` to `gs://fine_tuning_osti_docs/batch_analysis/input/` and submits a batch prediction job. Job metadata (name, URIs, timestamps) is saved to `output/job_metadata.json`.

To check status of a running job:
```bash
python submit_batch.py --status "projects/47868259239/locations/us-central1/batchPredictionJobs/YOUR_JOB_ID"
```

#### Step 3: Parse Results (after job completes)

```bash
python parse_results.py              # download from GCS + parse
python parse_results.py --local output/batch_output_raw.jsonl  # parse local file
```

This downloads the batch output JSONL from GCS, parses each response, and produces:
- `output/paper_evaluations.json` -- all 1,133 parsed evaluations
- `output/recommendation_matrix.json` -- cell_id -> ranked papers
- `output/parse_stats.json` -- success/failure/recommendation counts

#### Step 4: Generate Report

```bash
python generate_report.py
```

Produces `output/recommendation_report.md` containing:
- Executive summary (papers evaluated, cells covered, gap count)
- Coverage tables by commodity and by subdomain
- 100 cell-level sections each showing the top 5 papers with scores, justifications, and suggested question angles
- Gap analysis identifying cells with no high-relevance papers

---

## Design Decisions in Detail

### Why One Request Per Paper (Not Per Cell)

The naive approach would send one request per (paper, cell) pair. Since each paper is evaluated against 4-16 cells, that would be ~12,000 requests instead of 1,133. The one-per-paper approach:

- Cuts API calls by ~10x and reduces total token usage (the system instruction and paper metadata are sent once, not repeated per cell)
- Gives Gemini the full context of all relevant cells at once, allowing it to compare and rank cells for a given paper more consistently

**Trade-off: MAX_TOKENS truncation.** With `maxOutputTokens=4096`, papers evaluated against many cells (especially HREE with 16 cells) can produce responses that exceed the token budget. In the actual batch run, 289 of 1,133 responses (25.5%) were truncated. The parser includes a salvage mechanism (see below) that recovered 262 of those, but this means some cell evaluations near the end of long responses were lost. A higher `maxOutputTokens` (e.g., 8192) would reduce truncation at the cost of slightly higher output token spend.

### Why Structured JSON Output (responseMimeType + responseSchema)

Every request includes `"responseMimeType": "application/json"` and a full `responseSchema`. This tells Gemini to produce JSON that conforms exactly to our schema -- no freeform text, no missing fields, no hallucinated keys. This is critical because:

- We're parsing 1,133 responses programmatically. Even a 1% malformation rate would mean 11 unparseable responses.
- The schema enforces that every cell evaluation includes all required fields (`cell_id`, `relevance_score`, `justification`, `suggested_question_angle`, `supports_l3_l4`).
- Vertex AI validates the output against the schema server-side before returning it.

### Why Abstract-Only (Not Full Text)

Using only title, abstract, authors, subjects, and publication date (not the full paper text):

- **Sufficient for relevance assessment**: An abstract tells you what a paper is *about* and its key contributions. That's all we need to determine whether it maps to a matrix cell -- we don't need the full paper to know if it discusses "DRC cobalt production volume" (Q32).
- **Token efficiency**: Average prompt is ~1,500 tokens per paper. Using full text would be ~10,000-50,000 tokens per paper, blowing up costs from ~$3-7 to ~$50-300.
- **Speed**: Batch jobs complete faster with shorter prompts.

### Why OCR Fallback for Empty Abstracts

82 of the 1,133 papers have empty `description` fields in the OSTI catalog. We have 106 OCR-extracted files from a prior Mistral-OCR pipeline (`OSTI_OCR_Extracted/batch_output/`). Of those, 12 overlap with the empty-abstract papers.

The OCR files have `abstract` and `text` fields. In practice, the `abstract` fields are often empty too (the OCR pipeline didn't extract abstracts separately), so we fall back to using the first ~500 characters of the OCR `text` field, truncated at a sentence boundary. This recovers enough context for a meaningful relevance assessment.

The remaining 70 papers with no abstract and no OCR text are marked with `limited_metadata` and scored conservatively.

### Why the google-genai SDK (Not Legacy aiplatform)

The `google-genai` package (>= 1.0.0) is the current recommended SDK for interacting with the Vertex AI Gemini API. It replaced the older `google-cloud-aiplatform` approach. The batch API is accessed through `client.batches.create()` with `vertexai=True`, which handles the Vertex AI endpoint routing automatically.

### Why Lazy GCP Imports

The `submit_batch.py` and `parse_results.py` files import `google.cloud.storage` and `google.genai` inside their functions rather than at module level. This allows the core logic modules (`config.py`, `matrix_parser.py`, `prepare_batch.py`, `generate_report.py`) to be imported and tested on any machine without GCP dependencies installed. Only the two scripts that actually talk to GCP need the dependencies at runtime.

### Truncated JSON Salvage (parse_results.py)

Gemini's structured output mode guarantees valid JSON *when the response completes*, but with `maxOutputTokens=4096`, 289 of 1,133 responses hit the token limit and were cut off mid-JSON (`finishReason: MAX_TOKENS`). Rather than discarding these entirely, `parse_results.py` includes a `_salvage_truncated_json()` function that uses regex to extract:

1. Top-level fields (`osti_id`, `overall_cmm_relevance`, `depth_assessment`) from the partial JSON
2. All **complete** `cell_evaluation` objects -- i.e., objects where all 5 required fields (`cell_id`, `relevance_score`, `justification`, `suggested_question_angle`, `supports_l3_l4`) and the closing `}` were written before truncation
3. Reconstructs `best_matching_cells` and `recommended_for_gold_qa` from the recovered cell evaluations

This recovered 262 of the 289 truncated responses, yielding 2,114 additional cell evaluations that would otherwise have been lost. The 27 unrecoverable responses were truncated so early (before the first complete cell evaluation) that no useful data could be extracted.

The salvage approach is conservative: it only includes cell evaluations where *all five fields* were fully written. If a response was cut off mid-`justification` for the 8th cell, cells 1-7 are recovered and cell 8 is discarded.

---

## How the Cell Routing Works

Each paper in the document catalog has a `commodity_category` field. This field determines which matrix cells the paper is evaluated against:

### Commodity Papers (943 papers)

Papers tagged with a specific commodity (e.g., `HREE`, `CO`, `LI`, `GA`, `GR`, `LREE`, `NI`, `CU`, `GE`, `OTH`) are evaluated against **all cells for that commodity across all 10 subdomains**.

For example, an `HREE` paper is evaluated against 16 cells:
- T-EC/L1, T-EC/L2, T-EC/L3, T-EC/L4 (extraction chemistry)
- T-PM/L2, T-PM/L4 (processing metallurgy)
- T-GO/L1, T-GO/L3 (geological occurrence)
- Q-PS/L1 (production statistics)
- Q-TF/L2 (trade flows)
- Q-EP/L3 (economic parameters)
- G-PR/L2, G-PR/L4 (policy/regulatory)
- G-BM/L2 (bilateral/multilateral)
- S-CC/L3 (cross-commodity)
- S-ST/L1 (supply chain topology)

The number of cells varies by commodity because some commodities appear in more matrix cells than others (HREE=16, CO=12, GE=4, etc.).

### Subdomain Papers (190 papers)

Papers tagged with a subdomain (e.g., `subdomain_G-PR`, `subdomain_S-ST`, `subdomain_T-PM`) are evaluated against **all 10 commodity cells within that subdomain**.

For example, a `subdomain_G-PR` paper is evaluated against 10 cells:
- GA/L1, GE/L1, HREE/L2, GA/L2, GR/L2, CO/L3, LI/L3, LREE/L3, HREE/L4, NI/L4

This ensures every paper is evaluated only against cells it could plausibly be relevant to, avoiding the waste of evaluating a pure-geology paper against trade flow cells.

### Category Distribution

| Category | Papers | Cells Per Paper | Total Evaluations |
|----------|--------|-----------------|-------------------|
| HREE | 176 | 16 | 2,816 |
| GA | 160 | 10 | 1,600 |
| CO | 143 | 12 | 1,716 |
| LREE | 128 | 10 | 1,280 |
| LI | 115 | 12 | 1,380 |
| GR | 70 | 11 | 770 |
| subdomain_S-ST | 57 | 10 | 570 |
| subdomain_G-PR | 51 | 10 | 510 |
| OTH | 51 | 10 | 510 |
| CU | 42 | 7 | 294 |
| subdomain_T-PM | 42 | 10 | 420 |
| subdomain_T-GO | 30 | 10 | 300 |
| NI | 29 | 8 | 232 |
| GE | 29 | 4 | 116 |
| subdomain_T-EC | 10 | 10 | 100 |
| **Total** | **1,133** | -- | **~12,614** |

---

## Prompt and Response Schema

### System Instruction

Each request includes a system instruction that establishes the evaluator persona:

> You are an expert analyst specializing in critical minerals and materials (CMM) supply chains, with deep knowledge of extraction chemistry, processing metallurgy, geology, trade flows, economic parameters, policy/regulatory frameworks, and supply chain topology.

It also provides the scoring rubric (1-5 scale) and guidelines for when to set `supports_l3_l4=true`.

### User Prompt (Per Paper)

Each user prompt contains:

1. **Paper metadata**: OSTI ID, title, authors (up to 5), publication date, category, subjects
2. **Abstract**: The paper's description from the catalog, or OCR-recovered text, or a "limited metadata" notice
3. **Matrix cells**: A numbered list of the 4-16 relevant cells, each showing cell ID, subdomain name, complexity level, and topic focus

### Structured Response Schema

Gemini is constrained to produce JSON matching this schema:

```json
{
  "osti_id": "string",
  "overall_cmm_relevance": 1-5,
  "depth_assessment": "string",
  "cell_evaluations": [
    {
      "cell_id": "CMM-HREE-TEC-L1-001",
      "relevance_score": 1-5,
      "justification": "Why this score...",
      "suggested_question_angle": "A specific Q&A angle...",
      "supports_l3_l4": true/false
    }
  ],
  "best_matching_cells": ["CMM-HREE-TEC-L1-001", ...],
  "recommended_for_gold_qa": true/false
}
```

---

## Cost Estimate

| Component | Estimate |
|-----------|----------|
| Input tokens | ~1.7M |
| Output tokens | ~0.9M |
| Input cost (batch, $0.625/1M) | ~$1.06 |
| Output cost (batch, $2.50/1M) | ~$2.27 |
| **Total estimated cost** | **~$3.33** |

Batch inference pricing is 50% off standard Gemini 2.5 Pro rates. Actual cost depends on response lengths.

---

## Input Data Sources

### document_catalog.json

- **Location**: `../OSTI_retrieval/document_catalog.json`
- **Records**: 1,133 OSTI documents
- **Fields used**: `osti_id`, `title`, `authors`, `publication_date`, `description`, `subjects`, `commodity_category`
- **Created by**: Prior OSTI retrieval pipeline that searched for CMM-relevant papers and categorized them

### CMM_Gold_QA_Allocation_Matrix.md

- **Location**: `../CMM_Gold_QA_Allocation_Matrix.md`
- **Structure**: Markdown tables defining 100 questions across 10 subdomains and 4 complexity levels
- **Each row**: `| Q# | CMM-COMMODITY-SUBDOMAIN-LEVEL-### | COMMODITY | L# | A/B | Topic Focus |`
- **Distribution**: 10 commodities (HREE:16, CO:12, LI:12, GA:10, GR:11, LREE:10, NI:8, CU:7, GE:4, OTH:10)
- **Companion to**: `CMM_LLM_Baseline_Gold_QA_Methodology.md`

### OSTI_OCR_Extracted/batch_output/

- **Location**: `../OSTI_OCR_Extracted/batch_output/`
- **Records**: 106 JSON files (one per OCR-processed OSTI document)
- **Fields used**: `abstract` (usually empty), `text` (OCR full text, used as fallback)
- **Created by**: Prior Mistral-OCR pipeline

---

## Module Reference

### config.py

Central configuration. All other modules import from here. Contains:

- **Paths**: `DOCUMENT_CATALOG`, `OCR_DIR`, `ALLOCATION_MATRIX_MD`, `OUTPUT_DIR`
- **GCP settings**: `GCP_PROJECT` ("rcgenai"), `GCP_REGION` ("us-central1"), `GCS_BUCKET` ("fine_tuning_osti_docs"), input/output prefixes
- **Model config**: `GEMINI_MODEL` ("gemini-2.5-pro"), `TEMPERATURE` (0.2), `MAX_OUTPUT_TOKENS` (4096)
- **Category lists**: `COMMODITY_CATEGORIES` (10 codes), `SUBDOMAIN_CATEGORIES` (10 codes)
- **Display mappings**: `COMMODITY_DISPLAY`, `SUBDOMAIN_DISPLAY`, `DOMAIN_GROUPS`, `COMPLEXITY_LEVELS`

### matrix_parser.py

Parses `CMM_Gold_QA_Allocation_Matrix.md` into structured data.

- **`MatrixCell` dataclass**: `question_number`, `cell_id`, `commodity`, `subdomain`, `complexity_level`, `stratum`, `topic_focus`
- **`parse_matrix()`**: Regex-parses markdown table rows, returns list of 100 `MatrixCell` objects
- **`get_relevant_cells(matrix, commodity_category)`**: Routes commodity papers to their commodity's cells and subdomain papers to their subdomain's cells
- **CLI mode** (`python matrix_parser.py`): Prints distribution stats for verification

The regex `_ROW_RE` matches lines like:
```
| 1 | CMM-HREE-TEC-L1-001 | HREE | L1 | A | Primary REE separation method |
```

Subdomain extraction from cell IDs (e.g., "TEC" -> "T-EC") uses the `_ID_SUBDOMAIN_MAP` dictionary, scanning from the 3rd segment onward to handle variable ID formats.

### prepare_batch.py

Generates the JSONL file of Vertex AI batch requests.

- **`RESPONSE_SCHEMA`**: The structured output JSON schema included in every request's `generationConfig`
- **`SYSTEM_INSTRUCTION`**: The expert evaluator persona and scoring rubric
- **`build_user_prompt(doc, cells)`**: Formats paper metadata + relevant cells into a prompt. Returns `(prompt_text, limited_metadata_flag)`
- **`_try_ocr_abstract(osti_id)`**: Checks `OSTI_OCR_Extracted/batch_output/{osti_id}.json` for abstract or text fallback
- **`build_request(doc, cells)`**: Wraps the prompt into the Vertex AI camelCase JSONL format
- **`prepare_batch(dry_run=False)`**: Main orchestrator. Loads catalog + matrix, builds all requests, writes JSONL, prints stats

### submit_batch.py

Handles GCS upload and Vertex AI job submission.

- **`upload_to_gcs(local_path, gcs_prefix)`**: Uploads a file to `gs://fine_tuning_osti_docs/{prefix}/{filename}`
- **`submit_batch_job(input_uri, monitor)`**: Creates a batch job via `client.batches.create()`, saves metadata to `output/job_metadata.json`
- **`poll_job(client, job_name)`**: Polls job state every 60 seconds until terminal state. Updates metadata with `final_state` and `completed_at`
- **CLI flags**: `--monitor` (poll after submit), `--status JOB_NAME` (check existing job), `--input PATH` (custom input file)

### parse_results.py

Downloads and parses batch output, including salvage of truncated responses.

- **`CellScore` dataclass**: One paper's evaluation against one matrix cell
- **`PaperEvaluation` dataclass**: One paper's full evaluation (overall relevance + all cell scores)
- **`download_batch_output()`**: Lists JSONL blobs under the GCS output prefix, downloads and concatenates them
- **`_salvage_truncated_json(text)`**: Regex-based recovery of partial JSON from `MAX_TOKENS` truncated responses. Extracts top-level fields and all complete `cell_evaluation` objects. Returns a reconstructed dict or `None` if too little was written
- **`parse_response_line(line)`**: Extracts JSON from `response.candidates[0].content.parts[0].text`, builds `PaperEvaluation`. Returns `(evaluation, was_salvaged)` tuple. Falls back to `_salvage_truncated_json()` on `json.JSONDecodeError`
- **`build_recommendation_matrix(evaluations)`**: Inverts the paper->cells structure into cells->papers, sorted by score descending
- **`save_results()`**: Writes `paper_evaluations.json`, `recommendation_matrix.json`, `parse_stats.json`
- **CLI flag**: `--local PATH` to parse a local file without downloading from GCS

### generate_report.py

Produces the final markdown report.

- **Executive summary**: Total papers, recommended papers, cells covered, gap count
- **Coverage by Commodity table**: Papers evaluated, cell count, cells covered (>=3), average top score
- **Coverage by Subdomain table**: Same metrics by subdomain
- **Cell-Level Recommendations**: 100 sections (organized by domain -> subdomain), each showing top 5 papers with rank, OSTI ID, score, title, and suggested question angle
- **Gap Analysis**: Table of cells with no paper scoring >= 3, grouped by commodity
- **Reads from**: `paper_evaluations.json`, `recommendation_matrix.json`, `parse_stats.json`, `document_catalog.json` (for titles)

---

## Batch Run Results (2026-02-07)

### Job Details

| Field | Value |
|-------|-------|
| Job name | `projects/47868259239/locations/us-central1/batchPredictionJobs/8367605008627138560` |
| Model | gemini-2.5-pro |
| Input | `gs://fine_tuning_osti_docs/batch_analysis/input/batch_input.jsonl` |
| Output | `gs://fine_tuning_osti_docs/batch_analysis/output` |
| Submitted | 2026-02-07T20:26:07Z |
| Final state | **JOB_STATE_SUCCEEDED** |

**Console note**: Jobs submitted via the `google-genai` SDK appear under **Vertex AI > Generative AI > Batch predictions** in the GCP console (`console.cloud.google.com/vertex-ai/generative/batch`), not under the classic Vertex AI Batch Predictions page.

### Parse Statistics

| Metric | Count |
|--------|-------|
| Total responses | 1,133 |
| Parsed OK | **1,106** (97.6%) |
| -- Complete (valid JSON) | 844 |
| -- Salvaged (truncated JSON) | 262 (2,114 cells recovered) |
| Parse failures (unrecoverable) | 27 |
| Papers recommended (any cell >= 4) | 387 |
| High overall CMM relevance (>= 4) | 349 |

289 responses (25.5%) were truncated by `MAX_TOKENS` (4096). The `_salvage_truncated_json()` regex parser recovered 262 of these by extracting all complete cell evaluation objects before the truncation point, yielding 2,114 additional cell evaluations. The remaining 27 were truncated before the first complete cell evaluation could be written.

### Coverage Results

| Metric | Value |
|--------|-------|
| Matrix cells covered (best score >= 3) | **92 / 100** |
| Strongly covered (best score >= 4) | **83 / 100** |
| Gap cells (no paper with score >= 3) | **8** |

#### Coverage by Commodity

| Commodity | Papers | Cells | Covered (>=3) | Avg Top Score |
|-----------|--------|-------|---------------|---------------|
| HREE | 342 | 16 | 15 | 4.5 |
| CO | 319 | 12 | 12 | 4.6 |
| LI | 304 | 12 | 12 | 4.8 |
| GA | 319 | 10 | 10 | 4.6 |
| GR | 218 | 11 | 10 | 4.5 |
| LREE | 275 | 10 | 10 | 4.6 |
| NI | 148 | 8 | 8 | 4.9 |
| CU | 126 | 7 | 5 | 3.1 |
| GE | 107 | 4 | 4 | 4.2 |
| OTH | 107 | 10 | 6 | 3.5 |

#### Coverage by Subdomain

| Subdomain | Cells | Covered (>=3) | Avg Top Score |
|-----------|-------|---------------|---------------|
| Extraction Chemistry (T-EC) | 10 | 10 | 4.8 |
| Processing Metallurgy (T-PM) | 10 | 9 | 4.6 |
| Geological Occurrence (T-GO) | 10 | 10 | 4.5 |
| Production Statistics (Q-PS) | 10 | 9 | 4.3 |
| Trade Flows (Q-TF) | 10 | 9 | 4.4 |
| Economic Parameters (Q-EP) | 10 | 9 | 4.1 |
| Policy/Regulatory (G-PR) | 10 | 10 | 4.8 |
| Bilateral/Multilateral (G-BM) | 10 | 7 | 3.3 |
| Cross-Commodity (S-CC) | 10 | 9 | 4.4 |
| Supply Chain Topology (S-ST) | 10 | 10 | 4.7 |

### Gap Cells (8)

These cells had no paper scoring >= 3 and will need external source material or additional OSTI papers:

| Q# | Cell ID | Commodity | Subdomain | Level | Topic | Best |
|----|---------|-----------|-----------|-------|-------|------|
| Q11 | CMM-GR-TPM-L1-001 | GR | T-PM | L1 | Spheroidization process definition | 2/5 |
| Q40 | CMM-OTH-QPS-L4-001 | OTH | Q-PS | L4 | PGM production concentration (SA/Russia) | 2/5 |
| Q49 | CMM-CU-QTF-L4-001 | CU | Q-TF | L4 | Copper concentrate vs. refined trade | 2/5 |
| Q60 | CMM-OTH-QEP-L4-001 | OTH | Q-EP | L4 | Manganese pricing and steel demand | 2/5 |
| Q73 | CMM-HREE-GBM-L2-001 | HREE | G-BM | L2 | Australia-U.S. REE cooperation | 2/5 |
| Q75 | CMM-CU-GBM-L2-001 | CU | G-BM | L2 | Chile-China copper relationship | 1/5 |
| Q80 | CMM-OTH-GBM-L4-003 | OTH | G-BM | L4 | WTO and critical minerals trade rules | 2/5 |
| Q90 | CMM-OTH-SCC-L4-001 | OTH | S-CC | L4 | Tungsten-molybdenum substitution | 2/5 |

Gap distribution: OTH has 4 gaps (PGMs, manganese, tungsten-molybdenum topics absent from OSTI corpus), CU has 2 gaps (bilateral trade topics), HREE and GR have 1 gap each.

### Rerunning the Pipeline

To re-submit and re-parse (e.g., after adjusting `maxOutputTokens`):
```bash
source .venv/bin/activate
python prepare_batch.py          # regenerate JSONL if config changed
python submit_batch.py --monitor # resubmit + wait
python parse_results.py          # download + parse new output
python generate_report.py        # regenerate report
```

---

## Verification Checklist

- [x] `matrix_parser.py` parses exactly 100 cells, 10 per subdomain
- [x] `prepare_batch.py --dry-run` generates 1,133 requests with correct routing
- [x] All 1,133 JSONL lines are valid JSON with correct Vertex AI structure
- [x] `responseMimeType` and `responseSchema` present in every request's `generationConfig`
- [x] OCR fallback recovers 12 of 82 empty-abstract papers
- [x] End-to-end test (synthetic output -> parse -> report) passes
- [x] All 6 Python files pass syntax check and import successfully
- [x] Full batch job completes successfully (JOB_STATE_SUCCEEDED)
- [x] 1,106 / 1,133 responses parsed (844 complete + 262 salvaged)
- [x] All 100 matrix cells have at least 1 paper recommendation
- [x] 92 / 100 cells have a paper scoring >= 3
- [x] Gap analysis identifies 8 cells needing external sources (mostly OTH and CU bilateral topics)
