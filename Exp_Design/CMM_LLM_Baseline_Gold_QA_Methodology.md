# CMM LLM Baseline Evaluation: Gold Q&A Methodology Framework

**Document Version:** 1.0  
**Date:** December 21, 2025  
**Authors:** Nancy [Surname], Claude (Anthropic)  
**Project:** CM2US Foundation Model Development

---

## 1. Executive Summary

This document establishes the methodology for constructing 100 gold-standard question-answer pairs to baseline three large language models (Llama-3, Phi-4, Mixtral 8x7b) on Critical Minerals and Materials (CMM) supply chain knowledge. The framework is designed to:

1. **Discriminate model capabilities** through stratified sampling across cognitive complexity levels
2. **Normalize for training cutoff disparities** via temporal stratification
3. **Prioritize strategically important commodities** based on U.S. supply chain vulnerabilities
4. **Enable rigorous, reproducible evaluation** with validated gold-standard answers

The methodology reflects CM2US mission priorities: compressing supply chain development timelines, identifying processing chokepoints, and enabling autonomous decision support for resource discovery through production.

---

## 2. Prioritization Framework

### 2.1 Commodity Selection Rationale

Commodities were prioritized at the intersection of three orthogonal criteria:

| Criterion | Definition | Discriminating Test |
|-----------|------------|---------------------|
| **End-use criticality** | Enables technology essential to U.S. economic/defense posture | Would substitution require fundamental redesign of deployed systems? |
| **Processing concentration** | Single-country or single-facility dominance | Does China (or any adversary) control >70% of any processing step? |
| **Supply chain opacity** | Poor data availability on flows, inventories, ownership | Can we answer basic questions about material provenance? |

### 2.2 Commodity Priority Tiers and Weightings

| Priority | Commodity/Group | Weight | Questions (n) | Justification |
|----------|-----------------|--------|---------------|---------------|
| 1 | Heavy REE (Dy, Tb) | 15% | 15 | Maximum vulnerability; ~90% Chinese separation capacity; active DOE/lab research |
| 2 | Cobalt | 12% | 12 | DRC instability (70% mine); China refining (75%); battery demand surge |
| 3 | Lithium | 12% | 12 | Highest demand growth; conversion chokepoint despite mining diversification |
| 4 | Gallium | 10% | 10 | Active export controls (2023-24); byproduct complexity; semiconductor criticality |
| 5 | Graphite | 10% | 10 | Underappreciated chokepoint; 100% Chinese spherical processing |
| 6 | Light REE (Nd, Pr) | 10% | 10 | Permanent magnet nexus; less extreme than heavy REE but still concentrated |
| 7 | Nickel (Class 1) | 8% | 8 | Battery-grade distinction critical; Indonesian ore vs. Chinese refining |
| 8 | Copper | 8% | 8 | Volume/infrastructure criticality; electrification backbone |
| 9 | Germanium | 5% | 5 | Semiconductor/defense (IR optics); August 2023 export controls |
| 10 | Other (Mn, Ti, PGM, W) | 10% | 10 | Coverage breadth; comparative vulnerability assessment |
| | **TOTAL** | **100%** | **100** | |

---

## 3. Evaluation Matrix Structure

### 3.1 Sub-Domain Taxonomy (Axis 1)

Questions are distributed across 10 sub-domains reflecting the full scope of CMM supply chain knowledge:

| Domain Category | Sub-Domain | Code | Description |
|-----------------|------------|------|-------------|
| **Technical** | Extraction Chemistry | T-EC | Separation coefficients, reagent systems, solvent extraction, ion exchange |
| | Processing Metallurgy | T-PM | Pyrometallurgical vs. hydrometallurgical routes, refining processes |
| | Geological Occurrence | T-GO | Deposit types, mineralogical associations, ore grades, reserve classifications |
| **Quantitative** | Production Statistics | Q-PS | Tonnages, growth rates, reserves vs. resources, capacity utilization |
| | Trade Flows | Q-TF | Import/export dependencies, concentration ratios, bilateral flows |
| | Economic Parameters | Q-EP | Pricing dynamics, cost structures, market mechanisms |
| **Geopolitical** | Policy/Regulatory | G-PR | Export controls, strategic stockpiling, permitting, environmental regulations |
| | Bilateral/Multilateral | G-BM | Trade agreements, sanctions, partnerships, diplomatic developments |
| **Systemic** | Cross-Commodity | S-CC | Substitution constraints, co-production dependencies, byproduct relationships |
| | Supply Chain Topology | S-ST | Processing chokepoints, vertical integration, network vulnerabilities |

### 3.2 Cognitive Complexity Levels (Axis 2)

Questions are stratified across four complexity levels adapted from Bloom's taxonomy:

| Level | Designation | Code | Operational Definition | Expected Model Behavior |
|-------|-------------|------|------------------------|------------------------|
| 1 | Factual Recall | L1 | Single-fact retrieval, no inference required | Direct knowledge retrieval |
| 2 | Relational | L2 | Two-fact retrieval with explicit relationship | Connection of related facts |
| 3 | Inferential | L3 | Synthesis across facts not explicitly co-located in training | Reasoning across knowledge domains |
| 4 | Analytical | L4 | Multi-step reasoning with quantitative or causal logic | Complex causal/quantitative analysis |

### 3.3 Temporal Stratification (Axis 3)

To normalize for disparate training cutoffs across models:

| Model | Approximate Cutoff | Stratum A Access | Stratum B Access |
|-------|-------------------|------------------|------------------|
| Llama-3 (8B/70B) | December 2023 | Full | Pre-2024 only |
| Phi-4 | Mid-2024 | Full | Pre-mid-2024 |
| Mixtral 8x7b | Late 2023 | Full | Pre-2024 only |

**Stratum A: Time-Invariant Knowledge (60% of questions, n=60)**
- Fundamental extraction/separation chemistry
- Geological deposit typologies
- Processing dependencies established before 2023
- Established supply chain structures

**Stratum B: Time-Sensitive Knowledge (40% of questions, n=40)**
- Production statistics with explicit temporal anchoring
- Policy developments with date-stamped framing
- Recent market disruptions or supply events
- Questions include explicit temporal tags for post-hoc filtering

---

## 4. Full Allocation Matrix

### 4.1 Sub-Domain × Complexity Distribution

Target: 100 questions across 40 cells (10 sub-domains × 4 complexity levels)

| Sub-Domain | L1 (Factual) | L2 (Relational) | L3 (Inferential) | L4 (Analytical) | Row Total |
|------------|--------------|-----------------|------------------|-----------------|-----------|
| T-EC | 2 | 3 | 3 | 2 | 10 |
| T-PM | 2 | 3 | 3 | 2 | 10 |
| T-GO | 3 | 3 | 2 | 2 | 10 |
| Q-PS | 3 | 3 | 2 | 2 | 10 |
| Q-TF | 2 | 3 | 3 | 2 | 10 |
| Q-EP | 2 | 2 | 3 | 3 | 10 |
| G-PR | 2 | 3 | 3 | 2 | 10 |
| G-BM | 2 | 3 | 2 | 3 | 10 |
| S-CC | 2 | 2 | 3 | 3 | 10 |
| S-ST | 2 | 3 | 3 | 2 | 10 |
| **Column Total** | **22** | **28** | **27** | **23** | **100** |

**Rationale for weighting toward L2-L3:** Maximum discriminative power exists at intermediate complexity levels. L1 tests basic retrieval (floor effects likely). L4 may exceed all models' capabilities (ceiling effects). L2-L3 provide the steepest performance gradients.

### 4.2 Commodity × Sub-Domain Allocation

Each commodity must appear across multiple sub-domains to test breadth. Minimum coverage: each commodity appears in ≥4 sub-domains.

| Commodity (n) | T-EC | T-PM | T-GO | Q-PS | Q-TF | Q-EP | G-PR | G-BM | S-CC | S-ST |
|---------------|------|------|------|------|------|------|------|------|------|------|
| Heavy REE (15) | 2 | 2 | 2 | 2 | 1 | 1 | 2 | 1 | 1 | 1 |
| Cobalt (12) | 1 | 1 | 2 | 2 | 2 | 1 | 1 | 1 | 1 | 0 |
| Lithium (12) | 2 | 1 | 2 | 2 | 1 | 1 | 1 | 1 | 0 | 1 |
| Gallium (10) | 1 | 1 | 1 | 1 | 1 | 1 | 2 | 0 | 1 | 1 |
| Graphite (10) | 1 | 2 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 1 |
| Light REE (10) | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Nickel (8) | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 |
| Copper (8) | 1 | 0 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 |
| Germanium (5) | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 0 |
| Other (10) | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 4 | 2 | 2 |
| **Column Total** | **10** | **10** | **11** | **11** | **10** | **10** | **10** | **10** | **10** | **8** |

*Note: Minor adjustments to reach exact totals may be needed during question drafting.*

---

## 5. Question-Answer Template Format

### 5.1 Metadata Schema

Each Q&A pair must include the following metadata fields:

```yaml
question_id: "CMM-[COMMODITY_CODE]-[SUBDOMAIN]-[COMPLEXITY]-[SEQUENCE]"
# Example: CMM-HREE-TEC-L3-001

commodity_primary: "Dysprosium"
commodity_secondary: ["Terbium", "Neodymium"]  # if cross-commodity
subdomain: "T-EC"
complexity_level: 3
temporal_stratum: "A"  # A = time-invariant, B = time-sensitive
temporal_tag: null  # For Stratum B: "2023-Q3" or similar
accessible_to: ["Llama-3", "Phi-4", "Mixtral"]  # Models with training access

question_text: |
  [Full question text]

gold_answer: |
  [Complete, validated answer]

answer_source:
  - citation: "USGS Mineral Commodity Summaries 2024, p. 58"
    url: "https://pubs.usgs.gov/publication/mcs2024"
    access_date: "2025-12-15"
  - citation: "DOE Critical Materials Assessment 2023"
    url: null
    access_date: null

validation_method: "primary_source"  # Options: primary_source, dual_coder, expert_review
confidence_score: 0.95  # 0.0-1.0

evaluation_criteria:
  required_elements:
    - "Must mention China's dominance in separation"
    - "Must state approximate percentage (85-95%)"
  partial_credit_elements:
    - "Mentions specific facilities or companies"
    - "Discusses implications for supply chain"
  disqualifying_errors:
    - "States U.S. has significant separation capacity"
    - "Confuses mining with processing"

notes: |
  [Any additional context for evaluators]
```

### 5.2 Question Formatting Rules

1. **Stratum B questions** must include explicit temporal anchoring:
   - ✓ "As of Q3 2023, what percentage..."
   - ✓ "Following China's July 2023 announcement..."
   - ✗ "What is the current percentage..." (ambiguous temporality)

2. **L3-L4 questions** should be phrased to require synthesis:
   - ✓ "Given X and Y, what Z would result?"
   - ✓ "How does A affect B through mechanism C?"
   - ✗ "What is X and what is Y?" (compound L1, not L3)

3. **Cross-commodity questions (S-CC)** must explicitly invoke multiple materials:
   - ✓ "How does cobalt-nickel co-dependency in NMC cathodes affect..."
   - ✗ "What materials are used in batteries?" (too broad)

---

## 6. Example Questions by Cell Type

### 6.1 Technical / Extraction Chemistry

**L1 - Factual (CMM-HREE-TEC-L1-001)**
```yaml
question_text: |
  What is the primary industrial method for separating individual rare earth 
  elements from mixed rare earth solutions?

gold_answer: |
  Solvent extraction (also called liquid-liquid extraction) using organic 
  extractants such as D2EHPA (di-2-ethylhexyl phosphoric acid), PC88A, or 
  Cyanex variants is the primary industrial method for rare earth separation.

complexity_level: 1
temporal_stratum: "A"
```

**L3 - Inferential (CMM-HREE-TEC-L3-001)**
```yaml
question_text: |
  Given that heavy rare earth elements (Dy, Tb) have similar ionic radii and 
  chemical properties to adjacent lanthanides, and that separation factors 
  between adjacent REE pairs are typically 1.5-3.0, what implications does 
  this have for the number of extraction stages required in a commercial 
  separation cascade?

gold_answer: |
  The low separation factors (1.5-3.0) between adjacent lanthanides necessitate 
  multi-stage counter-current extraction cascades with hundreds to thousands of 
  stages. For heavy REE separation specifically, commercial facilities typically 
  require 50-200+ mixer-settler stages per separation step, with the total 
  cascade potentially requiring 1,000+ stages to achieve commercial purity 
  (>99.9%). This capital-intensive infrastructure requirement is a primary 
  barrier to entry and explains why separation capacity is concentrated in 
  facilities with decades of operational optimization.

complexity_level: 3
temporal_stratum: "A"
```

### 6.2 Quantitative / Trade Flows

**L2 - Relational (CMM-CO-QTF-L2-001)**
```yaml
question_text: |
  Which country is the largest producer of mined cobalt, and what approximate 
  percentage of global mine production does it represent?

gold_answer: |
  The Democratic Republic of the Congo (DRC) is the largest producer of mined 
  cobalt, representing approximately 70-74% of global mine production 
  (approximately 170,000-190,000 tonnes annually as of 2023-2024).

complexity_level: 2
temporal_stratum: "A"
temporal_tag: "pre-2024"
```

**L4 - Analytical (CMM-CO-QTF-L4-001)**
```yaml
question_text: |
  If artisanal and small-scale mining (ASM) accounts for approximately 15-20% 
  of DRC cobalt production, and ASM-sourced cobalt faces increasing exclusion 
  from Western supply chains due to ESG concerns, calculate the approximate 
  tonnage affected and analyze the second-order market effects this exclusion 
  would create for battery-grade cobalt availability.

gold_answer: |
  Calculation: DRC production ~170,000-190,000 tonnes × 15-20% ASM share = 
  ~25,500-38,000 tonnes potentially affected annually.
  
  Second-order effects:
  1. Supply bifurcation: Creation of dual markets (ESG-compliant premium vs. 
     unrestricted discount) with price divergence
  2. Chinese market absorption: ASM material likely redirected to Chinese 
     refiners with less stringent sourcing requirements, strengthening 
     China's feedstock position
  3. Industrial cobalt pressure: ASM exclusion from battery supply may push 
     material into superalloy/catalyst markets, depressing those prices
  4. Refining bottleneck intensification: Compliant supply must route through 
     fewer verified channels, creating capacity constraints at certified refiners
  5. Price premium expansion: Battery-grade cobalt sulphate from verified 
     sources likely commands 10-20% premium over spot
  
  Net effect: Reduction of ~25,000-38,000 tonnes from Western-accessible 
  battery supply, representing 15-25% of global battery-grade demand.

complexity_level: 4
temporal_stratum: "A"
```

### 6.3 Geopolitical / Policy-Regulatory

**L2 - Relational (CMM-GA-GPR-L2-001)**
```yaml
question_text: |
  In 2023, China implemented export controls on which two semiconductor-critical 
  elements, and what justification did the Chinese government provide?

gold_answer: |
  China implemented export controls on gallium and germanium, effective 
  August 1, 2023. The Chinese government cited "national security and 
  interests" as justification, framing the controls as necessary to protect 
  strategic resources. The timing followed U.S. semiconductor export 
  restrictions, widely interpreted as a retaliatory measure.

complexity_level: 2
temporal_stratum: "B"
temporal_tag: "2023-Q3"
accessible_to: ["Llama-3", "Phi-4", "Mixtral"]
```

### 6.4 Systemic / Cross-Commodity

**L3 - Inferential (CMM-LI-SCC-L3-001)**
```yaml
question_text: |
  Given that lithium-ion battery cathode chemistries are evolving from 
  high-cobalt (LCO) toward high-nickel (NMC811, NCA) and cobalt-free (LFP) 
  formulations, what are the cross-commodity implications for cobalt, nickel, 
  and lithium demand trajectories?

gold_answer: |
  The cathode chemistry evolution creates divergent demand trajectories:
  
  Cobalt: Demand growth decelerates despite EV volume growth. Per-vehicle 
  cobalt intensity declining from ~8-12 kg (NMC111/523) to ~3-5 kg (NMC811) 
  to zero (LFP). Total demand may plateau mid-decade as chemistry shift 
  outpaces vehicle growth.
  
  Nickel (Class 1): Demand intensifies as NMC811/NCA adoption increases 
  nickel intensity per kWh. However, LFP adoption in standard-range vehicles 
  creates a segmented market where nickel demand concentrates in 
  premium/long-range segments.
  
  Lithium: Demand grows regardless of cathode chemistry—all formulations 
  require lithium. LFP actually increases lithium intensity per kWh 
  compared to NMC due to lower energy density requiring larger batteries 
  for equivalent range. Lithium demand trajectory is most directly coupled 
  to EV adoption rates.
  
  Net cross-commodity effect: Lithium faces most constrained outlook; 
  nickel demand remains strong but segmented; cobalt experiences relative 
  demand relief with potential oversupply risk.

complexity_level: 3
temporal_stratum: "A"
```

### 6.5 Systemic / Supply Chain Topology

**L4 - Analytical (CMM-GR-SST-L4-001)**
```yaml
question_text: |
  Natural graphite must be processed into spherical graphite before use in 
  lithium-ion battery anodes. Given that China controls approximately 100% 
  of global spherical graphite processing capacity, while natural graphite 
  mining is more geographically distributed (China ~65%, Mozambique, Brazil, 
  others ~35%), analyze the supply chain topology vulnerability and evaluate 
  whether mining diversification alone addresses the strategic risk.

gold_answer: |
  Analysis: Mining diversification is necessary but insufficient to address 
  strategic risk.
  
  Supply chain topology:
  Mine (distributed) → Concentration (partially distributed) → Spheroidization 
  (China monopoly) → Purification (China monopoly) → Coating (China monopoly) 
  → Anode production (China dominant)
  
  The chokepoint is not raw material but processing. Even if Western sources 
  capture 50% of mining, 100% of spheroidized product must transit through 
  Chinese facilities. This creates:
  
  1. Complete processing dependency regardless of mining origin
  2. Price-setting power at spheroidization stage
  3. Technology/IP concentration in Chinese equipment manufacturers
  4. 12-18 month minimum timeline to establish greenfield spheroidization 
     (assuming equipment availability)
  5. Environmental permitting challenges in Western jurisdictions for 
     graphite purification (HF acid processes)
  
  Strategic risk evaluation: Mining diversification addresses <30% of 
  vulnerability. Processing capacity diversification is the critical gap. 
  Current Western spherical graphite projects (e.g., Syrah Resources/Vidalia, 
  Nouveau Monde) total <5% of required capacity.
  
  Conclusion: Mining diversification without processing diversification 
  creates a false sense of security. Strategic risk remains near-total.

complexity_level: 4
temporal_stratum: "A"
```

---

## 7. Validation Protocol

### 7.1 Gold Answer Validation Requirements

| Complexity Level | Validation Method | Minimum Sources |
|------------------|-------------------|-----------------|
| L1 (Factual) | Primary source citation | 1 authoritative |
| L2 (Relational) | Primary source citation | 2 corroborating |
| L3 (Inferential) | Dual-coder verification | 2+ with reasoning chain |
| L4 (Analytical) | Expert review | 3+ with explicit logic validation |

### 7.2 Source Hierarchy

1. **Tier 1 (Preferred):** USGS Mineral Commodity Summaries, DOE Critical Materials Assessments, BGS World Mineral Statistics, peer-reviewed journals
2. **Tier 2 (Acceptable):** CRS Reports, IEA publications, UN Comtrade official statistics, national geological survey publications
3. **Tier 3 (Supporting only):** Industry reports (S&P Global, Wood Mackenzie), trade press, company filings

### 7.3 Confidence Scoring

Each gold answer receives a confidence score (0.0-1.0):

| Score Range | Interpretation | Validation Status |
|-------------|----------------|-------------------|
| 0.95-1.00 | Definitive, unambiguous fact | Single authoritative source sufficient |
| 0.85-0.94 | High confidence, minor uncertainty | Multiple sources agree |
| 0.70-0.84 | Moderate confidence, some ambiguity | Sources partially conflict; majority position stated |
| <0.70 | Low confidence | Flag for expert review before inclusion |

---

## 8. Evaluation Metrics

### 8.1 Scoring Rubric (per question)

| Score | Criteria |
|-------|----------|
| 1.0 | Complete, accurate answer with all required elements |
| 0.75 | Accurate on core facts; missing minor details |
| 0.50 | Partially correct; contains errors but demonstrates relevant knowledge |
| 0.25 | Minimal relevant content; significant errors |
| 0.0 | Incorrect, irrelevant, or refused to answer |

### 8.2 Aggregate Metrics

**Primary metrics:**
- Mean score by complexity level (L1, L2, L3, L4)
- Mean score by sub-domain (10 categories)
- Mean score by commodity (10 categories)
- Mean score by temporal stratum (A vs. B)

**Derived metrics:**
- Complexity degradation curve: Score(L1) → Score(L4) trajectory
- Domain expertise variance: Standard deviation across sub-domains
- Commodity knowledge gaps: Commodities with score <0.5

### 8.3 Model Comparison Framework

For fair cross-model comparison:
1. Report Stratum A scores separately (all models have training access)
2. Report Stratum B scores with temporal filtering (only questions within each model's cutoff)
3. Compute normalized scores accounting for temporal access

---

## 9. Implementation Timeline

| Week | Phase | Deliverables |
|------|-------|--------------|
| 1 | Question drafting | 100 draft Q&A pairs with metadata |
| 2 | Validation | Source verification; dual-coder review for L3-L4 |
| 2 | Baseline execution | Run all three models on evaluation set |
| 3 | Scoring | Apply rubric; compute aggregate metrics |
| 3-4 | Gap analysis | Identify systematic knowledge deficiencies |
| 4 | Fine-tuning corpus specification | Target data acquisition toward identified gaps |

---

## 10. Appendices

### Appendix A: Commodity Codes

| Code | Commodity |
|------|-----------|
| HREE | Heavy Rare Earth Elements (Dy, Tb) |
| LREE | Light Rare Earth Elements (Nd, Pr) |
| CO | Cobalt |
| LI | Lithium |
| GA | Gallium |
| GR | Graphite |
| NI | Nickel |
| CU | Copper |
| GE | Germanium |
| OTH | Other (Mn, Ti, PGM, W) |

### Appendix B: Sub-Domain Codes

| Code | Sub-Domain |
|------|------------|
| T-EC | Technical: Extraction Chemistry |
| T-PM | Technical: Processing Metallurgy |
| T-GO | Technical: Geological Occurrence |
| Q-PS | Quantitative: Production Statistics |
| Q-TF | Quantitative: Trade Flows |
| Q-EP | Quantitative: Economic Parameters |
| G-PR | Geopolitical: Policy/Regulatory |
| G-BM | Geopolitical: Bilateral/Multilateral |
| S-CC | Systemic: Cross-Commodity |
| S-ST | Systemic: Supply Chain Topology |

### Appendix C: Question ID Format

`CMM-[COMMODITY]-[SUBDOMAIN]-[LEVEL]-[SEQUENCE]`

Example: `CMM-HREE-TEC-L3-001`
- CMM: Project prefix
- HREE: Heavy rare earth elements
- TEC: Technical/Extraction Chemistry
- L3: Complexity level 3 (Inferential)
- 001: Sequence number within cell

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-21 | Nancy/Claude | Initial methodology framework |

---

*End of Document*
