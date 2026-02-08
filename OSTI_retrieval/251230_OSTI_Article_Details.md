  Successfully downloaded 1,112 DOE technical reports and journal preprints (6.2 GB) aligned with your CMM methodology.

  Results by Commodity Priority

  | Category               | PDFs | Size   | Methodology Weight |
  |------------------------|------|--------|--------------------|
  | HREE (Dy, Tb)          | 155  | 608 MB | 15%                |
  | LREE (Nd, Pr)          | 128  | 565 MB | 10%                |
  | Cobalt                 | 143  | 579 MB | 12%                |
  | Lithium                | 115  | 569 MB | 12%                |
  | Gallium                | 160  | 859 MB | 10%                |
  | Graphite               | 70   | 461 MB | 10%                |
  | Nickel                 | 29   | 265 MB | 8%                 |
  | Copper                 | 42   | 641 MB | 8%                 |
  | Germanium              | 29   | 92 MB  | 5%                 |
  | Other (Mn, Ti, PGM, W) | 51   | 383 MB | 10%                |

  Results by Sub-Domain

  | Sub-Domain                   | PDFs | Size   |
  |------------------------------|------|--------|
  | T-EC (Extraction Chemistry)  | 10   | 44 MB  |
  | T-PM (Processing Metallurgy) | 42   | 226 MB |
  | T-GO (Geological Occurrence) | 30   | 213 MB |
  | S-ST (Supply Chain Topology) | 57   | 214 MB |
  | G-PR (Policy/Regulatory)     | 51   | 523 MB |

  Output Files

  OSTI_retrieval/
  ├── pdfs/                    # 1,112 PDFs organized by category
  │   ├── HREE/               
  │   ├── CO/
  │   ├── LI/
  │   └── ...
  ├── document_catalog.json    # Full metadata catalog (1,133 entries)
  ├── downloaded_ids.txt       # Tracking file (prevents duplicates)
  └── retrieval_stats.json     # Execution statistics

  Notes

  - Some OSTI servers returned 503 errors (temporary unavailability) - the script can be re-run to retry failed downloads
  - Patent documents (USPTO links) were blocked - these are typically not full text preprints
  - Total queries executed: 72 across all commodities and sub-domains