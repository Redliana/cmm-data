# CMM Gold Q&A Source Analysis: Open Data Mapping

**Purpose:** Map available open data sources from the 251109_Supply_Chain_Datasets.csv inventory to our 100 Gold Q&A evaluation matrix  
**Date:** December 21, 2025

---

## 1. Selection Criteria

From the 65+ datasets inventoried, sources were selected based on:

| Criterion | Requirement |
|-----------|-------------|
| **Accessibility** | Open-source, Public, or CC-licensed (excludes Commercial/Subscription) |
| **AI-Readiness** | AI-ready or Partially AI-ready (structured, documented) |
| **CMM Relevance** | Covers ≥1 of our 10 priority commodity groups |
| **Sub-Domain Coverage** | Applicable to ≥1 of our 10 sub-domain categories |

---

## 2. Excluded Sources (Commercial/Restricted)

The following sources are **excluded** from Gold Q&A construction due to access restrictions:

| Dataset | Reason for Exclusion |
|---------|---------------------|
| BloombergNEF Battery Metals Database | Commercial subscription |
| S&P Global (SNL) Metals & Mining Database | Commercial subscription |
| Ecoinvent LCI Database | Commercial subscription |
| Minviro XYCLE | Commercial/proprietary |
| Exiger 1Exiger Platform | Commercial (FedRAMP) |
| British Geological Survey (BGS) World Mineral Statistics | Subscription for full access |
| NETL EDX ClaiMM | DOE internal/controlled access |
| DARPA CriticalMAAS Data | Internal R&D prototype |
| PSILCA (social LCA) | Commercial license |

**Note:** BGS has some open data; we can use publicly available summary statistics but not detailed datasets.

---

## 3. Primary Open Data Sources: Tier 1 (High Priority)

These sources provide direct, authoritative data for Gold Q&A construction:

### 3.1 USGS Mineral Commodity Summaries (MCS)

| Attribute | Value |
|-----------|-------|
| **URL** | https://pubs.usgs.gov/periodicals/mcs/ |
| **Accessibility** | Open-source (US Gov) |
| **AI-Readiness** | Partially AI-ready (some digitization required) |
| **Commodity Coverage** | Li, Co, Ni, Ga, Ge, REE, Cu, Mn, Ti, PGM, graphite, W — **ALL 10 PRIORITY GROUPS** |
| **Update Frequency** | Annual |
| **Primary Variables** | Production, reserves, trade, prices, consumption, import sources |

**Sub-Domain Mapping:**

| Sub-Domain | Relevance | Example Q&A Topics |
|------------|-----------|-------------------|
| Q-PS (Production Statistics) | ★★★★★ | Country production rankings, reserve estimates |
| Q-TF (Trade Flows) | ★★★★★ | Import sources, net import reliance |
| Q-EP (Economic Parameters) | ★★★★☆ | Pricing trends, consumption patterns |
| G-PR (Policy/Regulatory) | ★★★☆☆ | Strategic stockpile status, criticality designations |
| T-GO (Geological Occurrence) | ★★★☆☆ | Reserve locations, deposit summaries |

**Estimated Q&A Coverage:** 35-40 questions (L1-L2 primarily; some L3)

---

### 3.2 UN Comtrade Critical Minerals Trade Database

| Attribute | Value |
|-----------|-------|
| **URL** | https://comtradeplus.un.org/ |
| **Accessibility** | Open-source (API available) |
| **AI-Readiness** | AI-ready |
| **Commodity Coverage** | All traded mineral commodities via HS codes |
| **Update Frequency** | Monthly (with lag) |
| **Primary Variables** | Import/export values and quantities, partner countries, trade direction |

**Sub-Domain Mapping:**

| Sub-Domain | Relevance | Example Q&A Topics |
|------------|-----------|-------------------|
| Q-TF (Trade Flows) | ★★★★★ | Bilateral trade volumes, trade partners, concentration |
| Q-PS (Production Statistics) | ★★★☆☆ | Production proxies via export data |
| G-BM (Bilateral/Multilateral) | ★★★★☆ | Trade relationships, dependency patterns |
| S-ST (Supply Chain Topology) | ★★★☆☆ | Processing location inference from trade patterns |

**Estimated Q&A Coverage:** 15-20 questions (L2-L3 primarily)

**Limitation:** HS codes don't align well with CMM-specific products; requires careful mapping.

---

### 3.3 USGS Mineral Yearbook

| Attribute | Value |
|-----------|-------|
| **URL** | https://www.usgs.gov/centers/national-minerals-information-center/mineral-yearbook |
| **Accessibility** | Open-source |
| **AI-Readiness** | Partially AI-ready (PDF digitization required) |
| **Commodity Coverage** | 90+ minerals including ALL CMMs |
| **Update Frequency** | Annual (2-3 year lag) |
| **Primary Variables** | Detailed production, trade, consumption, industry structure, technology applications |

**Sub-Domain Mapping:**

| Sub-Domain | Relevance | Example Q&A Topics |
|------------|-----------|-------------------|
| Q-PS (Production Statistics) | ★★★★★ | Detailed country-level production history |
| Q-TF (Trade Flows) | ★★★★★ | Comprehensive trade statistics |
| T-PM (Processing Metallurgy) | ★★★★☆ | Industry structure, processing routes |
| Q-EP (Economic Parameters) | ★★★★☆ | Consumption patterns, market structure |
| S-CC (Cross-Commodity) | ★★★☆☆ | Co-production relationships |

**Estimated Q&A Coverage:** 20-25 questions (L1-L3)

---

### 3.4 IEA Critical Minerals Data Explorer

| Attribute | Value |
|-----------|-------|
| **URL** | https://www.iea.org/data-and-statistics/data-tools/critical-minerals-data-explorer |
| **Accessibility** | Open-source |
| **AI-Readiness** | AI-ready |
| **Commodity Coverage** | Cu, Li, Ni, Co, Nd, REEs, graphite |
| **Update Frequency** | Annual (projections to 2050) |
| **Primary Variables** | Demand projections by technology/scenario, mineral intensity, deployment trends |

**Sub-Domain Mapping:**

| Sub-Domain | Relevance | Example Q&A Topics |
|------------|-----------|-------------------|
| S-CC (Cross-Commodity) | ★★★★★ | Technology-mineral linkages, substitution scenarios |
| Q-EP (Economic Parameters) | ★★★★☆ | Demand forecasts, scenario analysis |
| G-PR (Policy/Regulatory) | ★★★☆☆ | Energy transition policy implications |
| S-ST (Supply Chain Topology) | ★★★☆☆ | Technology value chain dependencies |

**Estimated Q&A Coverage:** 10-15 questions (L3-L4 primarily)

---

### 3.5 Columbia University Critical Materials Monitor

| Attribute | Value |
|-----------|-------|
| **URL** | https://criticalmaterials.energypolicy.columbia.edu/ |
| **Accessibility** | Open-source |
| **AI-Readiness** | AI-ready |
| **Commodity Coverage** | Critical minerals for energy technologies |
| **Update Frequency** | Periodic (2017-2022 current) |
| **Primary Variables** | Trade flows (UN Comtrade derived), reserves, production, technology components |

**Sub-Domain Mapping:**

| Sub-Domain | Relevance | Example Q&A Topics |
|------------|-----------|-------------------|
| Q-TF (Trade Flows) | ★★★★★ | Curated trade flow visualizations |
| S-ST (Supply Chain Topology) | ★★★★☆ | Supply chain stage mapping |
| S-CC (Cross-Commodity) | ★★★★☆ | Technology-commodity linkages |

**Estimated Q&A Coverage:** 8-10 questions (L2-L3)

---

## 4. Secondary Open Data Sources: Tier 2 (Specialized Coverage)

### 4.1 DOE Critical Materials Institute (CMI) Open-Source Models

| Dataset | Commodities | Sub-Domains | Q&A Use |
|---------|-------------|-------------|---------|
| **DREEM** (Dynamic REE Model) | REE | Q-PS, Q-EP, S-CC | REE supply-demand dynamics; 3-5 questions |
| **CoCuNi Model** | Co, Cu, Ni | Q-PS, S-CC | Multi-metal system dynamics; 3-5 questions |
| **LISA Model** | Li (geothermal) | T-EC, Q-PS | Lithium extraction technology; 2-3 questions |

**URL:** https://github.com/CMI-Hub

---

### 4.2 Argonne National Laboratory Models

| Dataset | Commodities | Sub-Domains | Q&A Use |
|---------|-------------|-------------|---------|
| **BatPaC** | Li, Ni, Co, Mn, graphite, Al, Cu | T-PM, Q-EP, S-CC | Battery material intensity; 5-8 questions |
| **GREET Model** | Battery metals, REEs | T-PM, Q-EP | Process energy/emissions; 3-5 questions |
| **EverBatt** | Li, Ni, Co, Mn | T-PM, Q-EP | Recycling economics; 2-3 questions |

**URLs:** https://www.anl.gov/cse/batpac-battery-manufacturing-cost-estimation; https://greet.anl.gov/

---

### 4.3 NREL Models

| Dataset | Commodities | Sub-Domains | Q&A Use |
|---------|-------------|-------------|---------|
| **LIBRA** | Li, Co, Ni | Q-PS, S-CC | Battery supply chain dynamics; 3-5 questions |
| **MFI Database** | CMM-related industrial materials | T-PM, Q-EP | Process input-output; 2-3 questions |

**URLs:** https://github.com/NREL/LIBRA; https://mfi.nrel.gov/

---

### 4.4 USGS Geospatial/Geological Datasets

| Dataset | Commodities | Sub-Domains | Q&A Use |
|---------|-------------|-------------|---------|
| **MRDS** (Mineral Resources Data System) | All mineral deposits | T-GO | Deposit locations, geology; 5-8 questions |
| **Alaska Geochemical Database** | Multi-element | T-GO, T-EC | Geochemistry; 1-2 questions |

**URL:** https://mrdata.usgs.gov/mrds/

---

### 4.5 LANL SAFE Database

| Attribute | Value |
|-----------|-------|
| **URL** | https://safe.lanl.gov |
| **Accessibility** | Open |
| **AI-Readiness** | AI-ready |
| **Commodity Coverage** | f-elements (REE, actinides) |
| **Primary Variables** | Extractant, metal identity, aqueous/organic matrix, separation factors |

**Sub-Domain Mapping:**

| Sub-Domain | Relevance | Example Q&A Topics |
|------------|-----------|-------------------|
| T-EC (Extraction Chemistry) | ★★★★★ | Separation factors, extractant systems |
| T-PM (Processing Metallurgy) | ★★★★☆ | Solvent extraction parameters |

**Estimated Q&A Coverage:** 5-8 questions (L1-L3 for REE extraction chemistry)

---

### 4.6 Facility/Mine Registries

| Dataset | Coverage | Sub-Domains | Q&A Use |
|---------|----------|-------------|---------|
| **ICMM Global Mining Dataset** | 8,508 mines/facilities, 47 commodities | S-ST, Q-PS | Facility geography; 3-5 questions |
| **Australian Mines Atlas** | Australia multi-commodity | T-GO, S-ST | Regional coverage; 2-3 questions |
| **MinCan (Canada)** | Canada facilities | S-ST | North America coverage; 1-2 questions |
| **Global Mining Data Platform** | 80+ materials, 1,171 mines | Q-PS, S-ST | Production data; 3-5 questions |
| **MSHA Mine Data** | U.S. mines | Q-PS | U.S. operational data; 2-3 questions |

---

### 4.7 Policy/Criticality Sources

| Dataset | Coverage | Sub-Domains | Q&A Use |
|---------|----------|-------------|---------|
| **OECD Critical Minerals Indicators** | ~51 minerals | G-PR, G-BM | Criticality metrics; 3-5 questions |
| **IRENA Geopolitics Report** | 51 materials | G-PR, G-BM | Geopolitical risk; 3-5 questions |
| **World Bank Climate-Smart Mining** | Graphite, Li, Co, Cu, Ni, REEs, Mn | S-CC, G-PR | Demand projections; 3-5 questions |
| **UNEP Global Material Flows** | Material classes (metals) | Q-TF, G-BM | Macro flows; 2-3 questions |

---

### 4.8 Mineralogical/Scientific Databases

| Dataset | Coverage | Sub-Domains | Q&A Use |
|---------|----------|-------------|---------|
| **MinDat** | All minerals | T-GO, T-EC | Mineral properties, occurrences; 3-5 questions |

**URL:** https://www.mindat.org/

---

## 5. Master Source-to-Matrix Mapping

### 5.1 Coverage by Sub-Domain

| Sub-Domain | Primary Sources | Secondary Sources | Coverage Quality |
|------------|-----------------|-------------------|------------------|
| **T-EC** (Extraction Chemistry) | LANL SAFE | MinDat, CMI models | ★★★★☆ |
| **T-PM** (Processing Metallurgy) | USGS Yearbook, ANL BatPaC/GREET | NREL MFI, EverBatt | ★★★★☆ |
| **T-GO** (Geological Occurrence) | USGS MRDS, MCS | MinDat, GA/NRCan registries | ★★★★★ |
| **Q-PS** (Production Statistics) | USGS MCS, Yearbook | UN Comtrade, ICMM, CMI models | ★★★★★ |
| **Q-TF** (Trade Flows) | UN Comtrade, USGS MCS | Columbia Monitor, UNEP GMFD | ★★★★★ |
| **Q-EP** (Economic Parameters) | USGS MCS, IEA Explorer | ANL models, World Bank | ★★★★☆ |
| **G-PR** (Policy/Regulatory) | USGS MCS, OECD Indicators | IRENA, World Bank | ★★★☆☆ |
| **G-BM** (Bilateral/Multilateral) | UN Comtrade, OECD | Columbia Monitor, IRENA | ★★★☆☆ |
| **S-CC** (Cross-Commodity) | IEA Explorer, CMI models | ANL BatPaC, NREL LIBRA | ★★★★☆ |
| **S-ST** (Supply Chain Topology) | Columbia Monitor, ICMM | Facility registries | ★★★☆☆ |

### 5.2 Coverage by Commodity

| Commodity | Primary Sources | Coverage Quality |
|-----------|-----------------|------------------|
| **HREE (Dy, Tb)** | USGS MCS/Yearbook, LANL SAFE, CMI DREEM | ★★★★☆ |
| **Cobalt** | USGS MCS/Yearbook, UN Comtrade, CMI CoCuNi, ANL models | ★★★★★ |
| **Lithium** | USGS MCS/Yearbook, IEA, CMI LISA, ANL BatPaC, NREL LIBRA | ★★★★★ |
| **Gallium** | USGS MCS/Yearbook | ★★★☆☆ |
| **Graphite** | USGS MCS/Yearbook, IEA, ANL BatPaC | ★★★★☆ |
| **LREE (Nd, Pr)** | USGS MCS/Yearbook, LANL SAFE, CMI DREEM, IEA | ★★★★☆ |
| **Nickel** | USGS MCS/Yearbook, UN Comtrade, CMI CoCuNi, ANL models | ★★★★★ |
| **Copper** | USGS MCS/Yearbook, UN Comtrade, CMI CoCuNi, IEA | ★★★★★ |
| **Germanium** | USGS MCS/Yearbook | ★★★☆☆ |
| **Other (Mn, Ti, PGM, W)** | USGS MCS/Yearbook, OECD | ★★★☆☆ |

---

## 6. Gap Analysis

### 6.1 Sub-Domains with Limited Open Data

| Sub-Domain | Gap Description | Mitigation Strategy |
|------------|-----------------|---------------------|
| **G-PR** (Policy/Regulatory) | Open sources lack real-time policy tracking | Supplement with government announcements, CRS reports |
| **G-BM** (Bilateral/Multilateral) | Agreement details often in gray literature | Use OECD, IRENA policy reports; government press releases |
| **S-ST** (Supply Chain Topology) | Processing facility data sparse | Infer from trade patterns; use ICMM facility registry |

### 6.2 Commodities with Limited Open Data

| Commodity | Gap Description | Mitigation Strategy |
|-----------|-----------------|---------------------|
| **Gallium** | Limited public production data (byproduct) | Rely heavily on USGS MCS; supplement with China trade data |
| **Germanium** | Similar byproduct opacity | USGS MCS primary source; zinc production proxies |
| **HREE** | Separation details often proprietary | LANL SAFE for chemistry; USGS for production |

### 6.3 Data Freshness Concerns

| Source | Lag | Implication |
|--------|-----|-------------|
| USGS Mineral Yearbook | 2-3 years | Use for historical/structural questions (Stratum A) |
| UN Comtrade | 1-2 months | Suitable for recent trade (Stratum B) |
| USGS MCS | ~1 year | Use for current-year production (Stratum A/B boundary) |

---

## 7. Recommended Source Strategy by Question Type

### 7.1 L1 (Factual) Questions — 22 questions

**Primary Sources:**
- USGS MCS (production, reserves, import sources)
- USGS MRDS (deposit types, locations)
- LANL SAFE (separation chemistry fundamentals)
- MinDat (mineral properties)

**Strategy:** Direct fact extraction; verify against single authoritative source.

### 7.2 L2 (Relational) Questions — 28 questions

**Primary Sources:**
- USGS MCS + UN Comtrade (production-trade linkages)
- IEA Explorer (technology-mineral relationships)
- ANL BatPaC (material-component relationships)

**Strategy:** Combine two related facts from complementary sources; ensure relationship is explicitly documented.

### 7.3 L3 (Inferential) Questions — 27 questions

**Primary Sources:**
- CMI system dynamics models (supply-demand implications)
- IEA Explorer scenarios (technology transition impacts)
- Columbia Monitor (supply chain dependencies)
- OECD/IRENA (criticality/risk synthesis)

**Strategy:** Require synthesis across sources; gold answer must include explicit reasoning chain.

### 7.4 L4 (Analytical) Questions — 23 questions

**Primary Sources:**
- Multiple sources combined for complex scenarios
- ANL models for quantitative analysis
- CMI models for dynamic system behavior

**Strategy:** Multi-step reasoning with quantitative elements; gold answer must show calculation or causal logic.

---

## 8. Source Retrieval Workflow

### Phase 1: Bulk Download (Week 1)

| Source | Format | Action |
|--------|--------|--------|
| USGS MCS 2024/2025 | PDF, CSV | Download all commodity chapters |
| USGS Mineral Yearbook | PDF | Download REE, Co, Li, Ni, Cu, Ga, Ge, graphite chapters |
| UN Comtrade | API/CSV | Query HS codes for 10 commodity groups (2020-2024) |
| IEA Critical Minerals Explorer | Web/API | Export demand projections |
| CMI Models (DREEM, CoCuNi, LISA) | GitHub | Clone repositories |
| LANL SAFE | Database | Export f-element separation data |

### Phase 2: Extraction & Validation (Week 1-2)

1. Extract key statistics from USGS sources
2. Cross-validate production figures (USGS vs. Comtrade exports)
3. Map trade flows to processing dependencies
4. Document extraction chemistry parameters from SAFE

### Phase 3: Q&A Drafting (Week 2-3)

1. Draft L1 questions from single-source facts
2. Draft L2 questions linking related facts
3. Draft L3-L4 questions requiring synthesis
4. Attach source citations to each gold answer

### Phase 4: Validation (Week 3-4)

1. Verify all citations accessible
2. Dual-coder review for L3-L4 answers
3. Temporal tag verification for Stratum B questions

---

## 9. Summary: Prioritized Source List

### Must-Use Sources (Core)

| Rank | Source | Q&A Coverage |
|------|--------|--------------|
| 1 | USGS Mineral Commodity Summaries | 35-40 questions |
| 2 | UN Comtrade | 15-20 questions |
| 3 | USGS Mineral Yearbook | 20-25 questions |
| 4 | IEA Critical Minerals Explorer | 10-15 questions |
| 5 | LANL SAFE Database | 5-8 questions |
| 6 | ANL BatPaC/GREET | 5-8 questions |
| 7 | CMI Models (DREEM, CoCuNi, LISA) | 8-12 questions |

### Should-Use Sources (Supplementary)

| Rank | Source | Q&A Coverage |
|------|--------|--------------|
| 8 | Columbia Critical Materials Monitor | 5-8 questions |
| 9 | USGS MRDS | 5-8 questions |
| 10 | OECD Critical Minerals Indicators | 3-5 questions |
| 11 | World Bank Climate-Smart Mining | 3-5 questions |
| 12 | ICMM Global Mining Dataset | 3-5 questions |
| 13 | NREL LIBRA | 3-5 questions |

### Nice-to-Have Sources (Edge Cases)

| Source | Use Case |
|--------|----------|
| MinDat | Mineralogical properties (T-GO, T-EC) |
| IRENA Geopolitics Report | Policy/risk questions (G-PR, G-BM) |
| Geoscience Australia / NRCan | Regional deposit questions |
| MSHA Mine Data | U.S. operational specifics |

---

*End of Source Analysis*
