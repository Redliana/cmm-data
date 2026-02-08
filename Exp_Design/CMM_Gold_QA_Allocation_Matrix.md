# CMM Gold Q&A Allocation Matrix: Detailed Cell Assignments

**Companion to:** CMM_LLM_Baseline_Gold_QA_Methodology.md  
**Purpose:** Operational worksheet for question drafting

---

## Master Allocation Grid (100 Questions)

### Full Matrix: Sub-Domain × Complexity × Commodity

This matrix shows the target number of questions in each cell, with commodity assignments.

```
                    L1 (Factual)    L2 (Relational)   L3 (Inferential)   L4 (Analytical)
                    ─────────────   ───────────────   ────────────────   ───────────────
T-EC (Extraction)       2               3                  3                  2         = 10
                    HREE, GA        HREE, LI, LREE     HREE, LI, GA       HREE, LREE
                    
T-PM (Processing)       2               3                  3                  2         = 10  
                    GR, LI          HREE, GR, NI       CO, GR, GA         HREE, GR
                    
T-GO (Geological)       3               3                  2                  2         = 10
                    HREE, CO, LI    CO, LI, LREE       HREE, NI           CU, GE
                    
Q-PS (Production)       3               3                  2                  2         = 10
                    HREE, CO, LI    GA, GR, LREE       NI, CU             CO, OTH
                    
Q-TF (Trade)            2               3                  3                  2         = 10
                    CO, LREE        HREE, LI, GR       CO, GA, NI         CU, OTH
                    
Q-EP (Economic)         2               2                  3                  3         = 10
                    GA, GE          CO, NI             HREE, LI, LREE     GR, CU, OTH
                    
G-PR (Policy)           2               3                  3                  2         = 10
                    GA, GE          HREE, GA, GR       CO, LI, LREE       HREE, NI
                    
G-BM (Bilateral)        2               3                  2                  3         = 10
                    CO, LREE        HREE, NI, CU       LI, OTH            OTH×3
                    
S-CC (Cross-Comm)       2               2                  3                  3         = 10
                    GA, GE          CO, LREE           HREE, GR, NI       LI, CU, OTH
                    
S-ST (Topology)         2               3                  3                  2         = 10
                    HREE, GA        LI, GR, CU         CO, LREE, OTH      GR, OTH
                    ─────────────   ───────────────   ────────────────   ───────────────
COLUMN TOTALS:         22              28                 27                 23         = 100
```

---

## Commodity Distribution Verification

### Questions per Commodity (Target vs. Allocated)

| Commodity | Target | Allocated | Variance | Status |
|-----------|--------|-----------|----------|--------|
| Heavy REE (HREE) | 15 | 15 | 0 | ✓ |
| Cobalt (CO) | 12 | 12 | 0 | ✓ |
| Lithium (LI) | 12 | 12 | 0 | ✓ |
| Gallium (GA) | 10 | 10 | 0 | ✓ |
| Graphite (GR) | 10 | 10 | 0 | ✓ |
| Light REE (LREE) | 10 | 10 | 0 | ✓ |
| Nickel (NI) | 8 | 8 | 0 | ✓ |
| Copper (CU) | 8 | 8 | 0 | ✓ |
| Germanium (GE) | 5 | 5 | 0 | ✓ |
| Other (OTH) | 10 | 10 | 0 | ✓ |
| **TOTAL** | **100** | **100** | **0** | **✓** |

### Commodity × Sub-Domain Coverage Matrix

Minimum requirement: Each commodity appears in ≥4 sub-domains

| Commodity | T-EC | T-PM | T-GO | Q-PS | Q-TF | Q-EP | G-PR | G-BM | S-CC | S-ST | Count |
|-----------|------|------|------|------|------|------|------|------|------|------|-------|
| HREE | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 10 ✓ |
| CO | - | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 9 ✓ |
| LI | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 10 ✓ |
| GA | ✓ | ✓ | - | ✓ | ✓ | ✓ | ✓ | - | ✓ | ✓ | 8 ✓ |
| GR | - | ✓ | - | ✓ | ✓ | ✓ | ✓ | - | ✓ | ✓ | 7 ✓ |
| LREE | ✓ | - | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 9 ✓ |
| NI | - | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - | 8 ✓ |
| CU | - | - | ✓ | ✓ | ✓ | ✓ | - | ✓ | ✓ | ✓ | 7 ✓ |
| GE | - | ✓ | ✓ | - | - | ✓ | ✓ | - | ✓ | - | 5 ✓ |
| OTH | - | - | - | ✓ | ✓ | ✓ | - | ✓ | ✓ | ✓ | 6 ✓ |

All commodities meet minimum coverage requirement (≥4 sub-domains).

---

## Temporal Stratum Allocation

### Target Distribution
- Stratum A (Time-Invariant): 60% = 60 questions
- Stratum B (Time-Sensitive): 40% = 40 questions

### Stratum Assignment by Sub-Domain

| Sub-Domain | Stratum A | Stratum B | Rationale |
|------------|-----------|-----------|-----------|
| T-EC | 10 | 0 | Extraction chemistry is foundational; rarely changes |
| T-PM | 8 | 2 | Processing routes stable; new technologies occasionally |
| T-GO | 9 | 1 | Geology invariant; reserve estimates update annually |
| Q-PS | 3 | 7 | Production statistics highly time-sensitive |
| Q-TF | 3 | 7 | Trade flows change annually |
| Q-EP | 4 | 6 | Prices volatile; cost structures more stable |
| G-PR | 3 | 7 | Policy developments highly time-sensitive |
| G-BM | 4 | 6 | Agreements evolve; some historical context stable |
| S-CC | 8 | 2 | Substitution relationships relatively stable |
| S-ST | 8 | 2 | Topology changes slowly; chokepoints persistent |
| **TOTAL** | **60** | **40** | |

### Stratum B Temporal Tags Required

For each Stratum B question, assign one of:
- `pre-2023`: Accessible to all models
- `2023-H1`: Accessible to all models (likely)
- `2023-Q3`: Llama-3/Mixtral cutoff boundary
- `2023-Q4`: May exceed Llama-3/Mixtral cutoff
- `2024-H1`: Phi-4 only
- `2024-H2`: May exceed all model cutoffs (flag for future evaluation)

---

## Detailed Cell Assignments

### Block 1: Technical Domain (30 questions)

#### T-EC: Extraction Chemistry (10 questions)

| Q# | ID | Commodity | Level | Stratum | Topic Focus |
|----|-----|-----------|-------|---------|-------------|
| 1 | CMM-HREE-TEC-L1-001 | HREE | L1 | A | Primary REE separation method |
| 2 | CMM-GA-TEC-L1-001 | GA | L1 | A | Gallium extraction from Bayer liquor |
| 3 | CMM-HREE-TEC-L2-001 | HREE | L2 | A | Separation factors and stage requirements |
| 4 | CMM-LI-TEC-L2-001 | LI | L2 | A | Brine vs. hard rock extraction trade-offs |
| 5 | CMM-LREE-TEC-L2-001 | LREE | L2 | A | NdPr co-extraction considerations |
| 6 | CMM-HREE-TEC-L3-001 | HREE | L3 | A | Cascade design implications |
| 7 | CMM-LI-TEC-L3-001 | LI | L3 | A | DLE technology impact on extraction economics |
| 8 | CMM-GA-TEC-L3-001 | GA | L3 | A | Byproduct recovery constraints |
| 9 | CMM-HREE-TEC-L4-001 | HREE | L4 | A | Heavy/light REE balance problem |
| 10 | CMM-LREE-TEC-L4-001 | LREE | L4 | A | Separation purity vs. throughput optimization |

#### T-PM: Processing Metallurgy (10 questions)

| Q# | ID | Commodity | Level | Stratum | Topic Focus |
|----|-----|-----------|-------|---------|-------------|
| 11 | CMM-GR-TPM-L1-001 | GR | L1 | A | Spheroidization process definition |
| 12 | CMM-LI-TPM-L1-001 | LI | L1 | A | Battery-grade conversion pathways |
| 13 | CMM-HREE-TPM-L2-001 | HREE | L2 | A | Oxide to metal reduction methods |
| 14 | CMM-GR-TPM-L2-001 | GR | L2 | A | Natural vs. synthetic graphite processing |
| 15 | CMM-NI-TPM-L2-001 | NI | L2 | A | Class 1 vs. Class 2 nickel processing |
| 16 | CMM-CO-TPM-L3-001 | CO | L3 | A | Hydromet vs. pyromet cobalt refining |
| 17 | CMM-GR-TPM-L3-001 | GR | L3 | A | Purification chemistry (HF) constraints |
| 18 | CMM-GA-TPM-L3-001 | GA | L3 | B | Semiconductor-grade purification requirements |
| 19 | CMM-HREE-TPM-L4-001 | HREE | L4 | A | Magnet alloy production integration |
| 20 | CMM-GR-TPM-L4-001 | GR | L4 | B | Anode coating technology evolution |

#### T-GO: Geological Occurrence (10 questions)

| Q# | ID | Commodity | Level | Stratum | Topic Focus |
|----|-----|-----------|-------|---------|-------------|
| 21 | CMM-HREE-TGO-L1-001 | HREE | L1 | A | Ion-adsorption clay characteristics |
| 22 | CMM-CO-TGO-L1-001 | CO | L1 | A | Sediment-hosted vs. magmatic deposits |
| 23 | CMM-LI-TGO-L1-001 | LI | L1 | A | Pegmatite vs. brine deposit types |
| 24 | CMM-CO-TGO-L2-001 | CO | L2 | A | DRC Copperbelt geology and cobalt association |
| 25 | CMM-LI-TGO-L2-001 | LI | L2 | A | Lithium Triangle geology |
| 26 | CMM-LREE-TGO-L2-001 | LREE | L2 | A | Carbonatite-hosted REE deposits |
| 27 | CMM-HREE-TGO-L3-001 | HREE | L3 | A | Heavy REE enrichment mechanisms |
| 28 | CMM-NI-TGO-L3-001 | NI | L3 | A | Laterite vs. sulfide implications |
| 29 | CMM-CU-TGO-L4-001 | CU | L4 | A | Porphyry copper and byproduct recovery |
| 30 | CMM-GE-TGO-L4-001 | GE | L4 | A | Germanium occurrence and recovery pathways |

---

### Block 2: Quantitative Domain (30 questions)

#### Q-PS: Production Statistics (10 questions)

| Q# | ID | Commodity | Level | Stratum | Topic Focus |
|----|-----|-----------|-------|---------|-------------|
| 31 | CMM-HREE-QPS-L1-001 | HREE | L1 | B | China's share of REE production |
| 32 | CMM-CO-QPS-L1-001 | CO | L1 | B | DRC cobalt production volume |
| 33 | CMM-LI-QPS-L1-001 | LI | L1 | B | Global lithium production leaders |
| 34 | CMM-GA-QPS-L2-001 | GA | L2 | B | Gallium production concentration |
| 35 | CMM-GR-QPS-L2-001 | GR | L2 | B | Graphite production geography |
| 36 | CMM-LREE-QPS-L2-001 | LREE | L2 | A | NdPr production relative to total REE |
| 37 | CMM-NI-QPS-L3-001 | NI | L3 | B | Indonesian nickel production growth |
| 38 | CMM-CU-QPS-L3-001 | CU | L3 | B | Copper production-demand balance |
| 39 | CMM-CO-QPS-L4-001 | CO | L4 | B | ASM contribution and tracking challenges |
| 40 | CMM-OTH-QPS-L4-001 | OTH | L4 | B | PGM production concentration (SA/Russia) |

#### Q-TF: Trade Flows (10 questions)

| Q# | ID | Commodity | Level | Stratum | Topic Focus |
|----|-----|-----------|-------|---------|-------------|
| 41 | CMM-CO-QTF-L1-001 | CO | L1 | A | U.S. cobalt import sources |
| 42 | CMM-LREE-QTF-L1-001 | LREE | L1 | A | REE import dependency |
| 43 | CMM-HREE-QTF-L2-001 | HREE | L2 | A | Myanmar-China REE transit route |
| 44 | CMM-LI-QTF-L2-001 | LI | L2 | B | Chile-China lithium trade relationship |
| 45 | CMM-GR-QTF-L2-001 | GR | L2 | A | Graphite processing bottleneck |
| 46 | CMM-CO-QTF-L3-001 | CO | L3 | A | DRC-China refining dependency |
| 47 | CMM-GA-QTF-L3-001 | GA | L3 | B | Gallium trade post-export controls |
| 48 | CMM-NI-QTF-L3-001 | NI | L3 | B | Indonesian nickel export evolution |
| 49 | CMM-CU-QTF-L4-001 | CU | L4 | A | Copper concentrate vs. refined trade |
| 50 | CMM-OTH-QTF-L4-001 | OTH | L4 | B | Titanium sponge trade patterns |

#### Q-EP: Economic Parameters (10 questions)

| Q# | ID | Commodity | Level | Stratum | Topic Focus |
|----|-----|-----------|-------|---------|-------------|
| 51 | CMM-GA-QEP-L1-001 | GA | L1 | A | Gallium pricing mechanism |
| 52 | CMM-GE-QEP-L1-001 | GE | L1 | A | Germanium market structure |
| 53 | CMM-CO-QEP-L2-001 | CO | L2 | B | Cobalt price volatility factors |
| 54 | CMM-NI-QEP-L2-001 | NI | L2 | B | Class 1 nickel premium dynamics |
| 55 | CMM-HREE-QEP-L3-001 | HREE | L3 | A | REE pricing opacity |
| 56 | CMM-LI-QEP-L3-001 | LI | L3 | B | Lithium pricing evolution (spot vs. contract) |
| 57 | CMM-LREE-QEP-L3-001 | LREE | L3 | A | Magnet pricing and REE cost pass-through |
| 58 | CMM-GR-QEP-L4-001 | GR | L4 | A | Graphite economics (natural vs. synthetic) |
| 59 | CMM-CU-QEP-L4-001 | CU | L4 | B | Copper demand elasticity |
| 60 | CMM-OTH-QEP-L4-001 | OTH | L4 | B | Manganese pricing and steel demand |

---

### Block 3: Geopolitical Domain (20 questions)

#### G-PR: Policy/Regulatory (10 questions)

| Q# | ID | Commodity | Level | Stratum | Topic Focus |
|----|-----|-----------|-------|---------|-------------|
| 61 | CMM-GA-GPR-L1-001 | GA | L1 | B | China gallium export control date |
| 62 | CMM-GE-GPR-L1-001 | GE | L1 | B | China germanium export control |
| 63 | CMM-HREE-GPR-L2-001 | HREE | L2 | B | REE export licensing requirements |
| 64 | CMM-GA-GPR-L2-001 | GA | L2 | B | Gallium export control stated justification |
| 65 | CMM-GR-GPR-L2-001 | GR | L2 | B | IRA graphite sourcing requirements |
| 66 | CMM-CO-GPR-L3-001 | CO | L3 | A | DRC mining code evolution |
| 67 | CMM-LI-GPR-L3-001 | LI | L3 | B | IRA battery minerals requirements |
| 68 | CMM-LREE-GPR-L3-001 | LREE | L3 | B | Defense Production Act critical minerals |
| 69 | CMM-HREE-GPR-L4-001 | HREE | L4 | A | U.S. rare earth policy effectiveness |
| 70 | CMM-NI-GPR-L4-001 | NI | L4 | B | Indonesian nickel export ban implications |

#### G-BM: Bilateral/Multilateral (10 questions)

| Q# | ID | Commodity | Level | Stratum | Topic Focus |
|----|-----|-----------|-------|---------|-------------|
| 71 | CMM-CO-GBM-L1-001 | CO | L1 | A | U.S.-DRC critical minerals MOU |
| 72 | CMM-LREE-GBM-L1-001 | LREE | L1 | B | Minerals Security Partnership |
| 73 | CMM-HREE-GBM-L2-001 | HREE | L2 | B | Australia-U.S. REE cooperation |
| 74 | CMM-NI-GBM-L2-001 | NI | L2 | B | U.S.-Indonesia minerals framework |
| 75 | CMM-CU-GBM-L2-001 | CU | L2 | A | Chile-China copper relationship |
| 76 | CMM-LI-GBM-L3-001 | LI | L3 | B | Argentina lithium nationalism |
| 77 | CMM-OTH-GBM-L3-001 | OTH | L3 | A | Russia PGM and sanctions |
| 78 | CMM-OTH-GBM-L4-001 | OTH | L4 | B | Critical minerals alliance architecture |
| 79 | CMM-OTH-GBM-L4-002 | OTH | L4 | B | Friend-shoring effectiveness |
| 80 | CMM-OTH-GBM-L4-003 | OTH | L4 | A | WTO and critical minerals trade rules |

---

### Block 4: Systemic Domain (20 questions)

#### S-CC: Cross-Commodity (10 questions)

| Q# | ID | Commodity | Level | Stratum | Topic Focus |
|----|-----|-----------|-------|---------|-------------|
| 81 | CMM-GA-SCC-L1-001 | GA | L1 | A | Gallium-aluminum relationship |
| 82 | CMM-GE-SCC-L1-001 | GE | L1 | A | Germanium-zinc co-production |
| 83 | CMM-CO-SCC-L2-001 | CO | L2 | A | Cobalt-copper co-production |
| 84 | CMM-LREE-SCC-L2-001 | LREE | L2 | A | REE balance problem |
| 85 | CMM-HREE-SCC-L3-001 | HREE | L3 | A | Dy-Nd substitution constraints |
| 86 | CMM-GR-SCC-L3-001 | GR | L3 | A | Graphite-silicon anode evolution |
| 87 | CMM-NI-SCC-L3-001 | NI | L3 | A | Ni-Co-Mn cathode chemistry dependencies |
| 88 | CMM-LI-SCC-L4-001 | LI | L4 | A | Battery chemistry evolution impacts |
| 89 | CMM-CU-SCC-L4-001 | CU | L4 | A | Copper-aluminum substitution in EVs |
| 90 | CMM-OTH-SCC-L4-001 | OTH | L4 | A | Tungsten-molybdenum substitution |

#### S-ST: Supply Chain Topology (10 questions)

| Q# | ID | Commodity | Level | Stratum | Topic Focus |
|----|-----|-----------|-------|---------|-------------|
| 91 | CMM-HREE-SST-L1-001 | HREE | L1 | A | REE processing chokepoint location |
| 92 | CMM-GA-SST-L1-001 | GA | L1 | A | Gallium supply chain structure |
| 93 | CMM-LI-SST-L2-001 | LI | L2 | A | Lithium mine-to-cell topology |
| 94 | CMM-GR-SST-L2-001 | GR | L2 | A | Graphite processing dependency |
| 95 | CMM-CU-SST-L2-001 | CU | L2 | A | Copper smelting concentration |
| 96 | CMM-CO-SST-L3-001 | CO | L3 | A | Cobalt refining network structure |
| 97 | CMM-LREE-SST-L3-001 | LREE | L3 | A | Permanent magnet value chain |
| 98 | CMM-OTH-SST-L3-001 | OTH | L3 | A | Titanium sponge production topology |
| 99 | CMM-GR-SST-L4-001 | GR | L4 | A | Graphite diversification false security |
| 100 | CMM-OTH-SST-L4-001 | OTH | L4 | A | Multi-commodity chokepoint analysis |

---

## Summary Statistics

### By Complexity Level
| Level | Count | Percentage |
|-------|-------|------------|
| L1 (Factual) | 22 | 22% |
| L2 (Relational) | 28 | 28% |
| L3 (Inferential) | 27 | 27% |
| L4 (Analytical) | 23 | 23% |

### By Temporal Stratum
| Stratum | Count | Percentage |
|---------|-------|------------|
| A (Time-Invariant) | 60 | 60% |
| B (Time-Sensitive) | 40 | 40% |

### By Domain Category
| Domain | Count | Percentage |
|--------|-------|------------|
| Technical | 30 | 30% |
| Quantitative | 30 | 30% |
| Geopolitical | 20 | 20% |
| Systemic | 20 | 20% |

---

## Next Steps

1. **Draft questions 1-30** (Technical domain) - prioritize foundational knowledge
2. **Draft questions 31-60** (Quantitative domain) - ensure temporal tags on Stratum B
3. **Draft questions 61-80** (Geopolitical domain) - verify policy dates/events
4. **Draft questions 81-100** (Systemic domain) - cross-commodity synthesis
5. **Validation pass** - source verification per methodology document
6. **Baseline execution** - deploy to models

---

*End of Allocation Matrix*
