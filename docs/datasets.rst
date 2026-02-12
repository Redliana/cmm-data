Datasets
========

This guide describes all datasets available through the CMM Data package.

.. contents:: Contents
   :local:
   :depth: 2

Dataset Overview
----------------

.. list-table::
   :header-rows: 1
   :widths: 25 35 20 20

   * - Dataset
     - Description
     - Records
     - Format
   * - USGS Commodity
     - Mineral commodity statistics
     - 80+ commodities
     - CSV
   * - USGS Ore Deposits
     - Geochemical database
     - 356 fields
     - CSV
   * - OSTI Documents
     - Technical reports
     - Variable
     - JSON
   * - Preprocessed Corpus
     - LLM training corpus
     - 3,298 docs
     - JSONL
   * - GA Chronostratigraphic
     - 3D geological model
     - 9 surfaces
     - GeoTIFF/XYZ
   * - NETL REE/Coal
     - REE in coal data
     - Variable
     - Geodatabase
   * - OECD Supply Chain
     - Trade and policy data
     - Multiple
     - PDF/CSV

USGS Mineral Commodity Summaries
--------------------------------

**Location:** ``USGS_Data/``

**Source:** U.S. Geological Survey Mineral Commodity Summaries 2023

**Description:**

The USGS Mineral Commodity Summaries provide annual data on production, trade,
and reserves for over 80 mineral commodities worldwide. This is the primary
data source for critical minerals analysis.

**Data Types:**

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Type
     - Description
   * - World Production
     - Production by country, reserves, and notes
   * - Salient Statistics
     - U.S. production, imports, exports, consumption, prices

**World Production Fields:**

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``Country``
     - Producing country name
   * - ``Prod_t_2021``
     - Production in metric tons (2021)
   * - ``Prod_t_est_2022``
     - Estimated production (2022)
   * - ``Reserves_t``
     - Reserves in metric tons
   * - ``Prod_notes``
     - Production footnotes
   * - ``Reserves_notes``
     - Reserves footnotes

**Salient Statistics Fields:**

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``Year``
     - Data year
   * - ``USprod_t``
     - U.S. production (metric tons)
   * - ``Imports_t``
     - U.S. imports (metric tons)
   * - ``Exports_t``
     - U.S. exports (metric tons)
   * - ``Consump_t``
     - Apparent consumption
   * - ``Price_dt``
     - Unit value ($/metric ton)
   * - ``NIR_pct``
     - Net import reliance (%)

**Usage:**

.. code-block:: python

   from cmm_data import USGSCommodityLoader

   loader = USGSCommodityLoader()

   # World production
   world = loader.load_world_production("lithi")

   # Salient statistics
   salient = loader.load_salient_statistics("lithi")

   # Top producers
   top = loader.get_top_producers("lithi", top_n=10)

USGS Ore Deposits Database
--------------------------

**Location:** ``USGS_Ore_Deposits/``

**Source:** USGS National Geochemical Database (NGDB)

**Description:**

Geochemical analyses from ore deposits worldwide, compiled from the National
Geochemical Database. Contains detailed element concentration data for
thousands of samples.

**Tables:**

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Table
     - Description
   * - ``Geology``
     - Deposit locations and geological context
   * - ``BV_Ag_Mo``
     - Best values for Ag through Mo elements
   * - ``BV_Na_Zr``
     - Best values for Na through Zr elements
   * - ``ChemData1``
     - Raw chemical data (part 1)
   * - ``ChemData2``
     - Raw chemical data (part 2)
   * - ``DataDictionary``
     - Field definitions (356 fields)
   * - ``AnalyticMethod``
     - Analytical method descriptions
   * - ``Reference``
     - Data sources and citations

**Coverage:**

- **Elements:** 60+ major and trace elements
- **Samples:** Thousands of ore deposit analyses
- **Deposit Types:** Porphyry, VMS, sediment-hosted, etc.

**Usage:**

.. code-block:: python

   from cmm_data import USGSOreDepositsLoader

   loader = USGSOreDepositsLoader()

   # Load geology
   geology = loader.load_geology()

   # Get REE samples
   ree = loader.get_ree_samples()

   # Element statistics
   stats = loader.get_element_statistics("La")

Preprocessed Document Corpus
----------------------------

**Location:** ``Data/preprocessed/``

**File:** ``unified_corpus.jsonl``

**Description:**

Unified corpus of critical minerals documents prepared for LLM training and
text analysis. Contains technical reports, publications, and documents from
multiple sources.

**Fields:**

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Field
     - Description
   * - ``id``
     - Unique document identifier
   * - ``title``
     - Document title
   * - ``text``
     - Full text content
   * - ``source``
     - Origin (OSTI, USGS, etc.)
   * - ``doc_type``
     - Document type
   * - ``date``
     - Publication date

**Statistics:**

- **Documents:** 3,298
- **Sources:** OSTI, USGS, IEA, and others
- **Topics:** Critical minerals, extraction, processing, supply chains

**Usage:**

.. code-block:: python

   from cmm_data import PreprocessedCorpusLoader

   loader = PreprocessedCorpusLoader()

   # Get statistics
   stats = loader.get_corpus_stats()

   # Search documents
   results = loader.search("lithium extraction", limit=10)

   # Iterate over documents
   for doc in loader.iter_documents():
       print(doc['title'])

OECD Supply Chain Data
----------------------

**Location:** ``OECD_Supply_Chain_Data/``

**Source:** OECD and International Energy Agency (IEA)

**Description:**

Trade data and policy information from OECD and IEA, including export
restrictions inventory and critical minerals outlook reports.

**Subdirectories:**

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Directory
     - Contents
   * - ``Export_Restrictions/``
     - OECD inventory of export restrictions (PDFs)
   * - ``IEA_Critical_Minerals/``
     - IEA Critical Minerals Outlook reports
   * - ``ICIO/``
     - Inter-Country Input-Output documentation
   * - ``BTIGE/``
     - Bilateral Trade documentation

**Export Restrictions Coverage:**

- **Commodities:** 65 industrial raw materials
- **Countries:** 82 producing nations
- **Years:** 2009-2023
- **Key Minerals:** Potash, molybdenum, tungsten, rare earths, lithium, cobalt

**Usage:**

.. code-block:: python

   from cmm_data import OECDSupplyChainLoader

   loader = OECDSupplyChainLoader()

   # Get export restrictions reports
   reports = loader.get_export_restrictions_reports()

   # Get minerals coverage
   coverage = loader.get_minerals_coverage()

   # Get download URLs for bulk data
   urls = loader.get_download_urls()

Geoscience Australia 3D Model
-----------------------------

**Location:** ``GA_149923_Chronostratigraphic/``

**Source:** Geoscience Australia eCat

**Description:**

Preliminary 3D chronostratigraphic model of Australia providing depth surfaces
for major geological time boundaries.

**Surfaces:**

1. Paleozoic_Top
2. Neoproterozoic_Top
3. Mesoproterozoic_Top
4. Paleoproterozoic_Top
5. Neoarchean_Top
6. Mesoarchean_Top
7. Paleoarchean_Top
8. Eoarchean_Top
9. Basement

**Formats:**

.. list-table::
   :header-rows: 1
   :widths: 20 50 30

   * - Format
     - Description
     - Size
   * - GeoTIFF
     - Raster grids for GIS
     - ~1.2 GB
   * - XYZ
     - ASCII point data
     - ~5.9 GB
   * - ZMAP
     - Grid format for modeling
     - ~1.2 GB
   * - PNG
     - Visualization images
     - ~51 MB

**Spatial Reference:** EPSG:3577 (GDA94 / Australian Albers)

**Usage:**

.. code-block:: python

   from cmm_data import GAChronostratigraphicLoader

   loader = GAChronostratigraphicLoader()

   # List surfaces
   surfaces = loader.list_surfaces()

   # Load surface data
   data = loader.load("Paleozoic_Top", format="xyz")

   # Get model info
   info = loader.get_model_info()

NETL REE and Coal Database
--------------------------

**Location:** ``NETL_REE_Coal/``

**Source:** National Energy Technology Laboratory

**Description:**

Rare earth element data from coal and coal-related resources compiled by NETL.

**Format:** ArcGIS Geodatabase (``.gdb``)

**Contents:**

- REE concentration data from coal samples
- Coal basin boundaries
- Sample locations with coordinates
- Analytical results for all REE elements

**REE Elements:**

La, Ce, Pr, Nd, Sm, Eu, Gd, Tb, Dy, Ho, Er, Tm, Yb, Lu, Y

**Requirements:**

.. code-block:: bash

   pip install cmm-data[geo]  # Installs geopandas, fiona

**Usage:**

.. code-block:: python

   from cmm_data import NETLREECoalLoader

   loader = NETLREECoalLoader()

   # List layers
   layers = loader.list_available()

   # Get REE samples
   samples = loader.get_ree_samples()

   # Get statistics
   stats = loader.get_ree_statistics()

OSTI Technical Reports
----------------------

**Location:** ``OSTI_retrieval/``

**Source:** DOE Office of Scientific and Technical Information

**Description:**

Technical reports and publications from DOE national laboratories and funded
research related to critical minerals.

**Usage:**

.. code-block:: python

   from cmm_data import OSTIDocumentsLoader

   loader = OSTIDocumentsLoader()

   # Search documents
   results = loader.search_documents("lithium extraction")

   # Get document metadata
   metadata = loader.get_document_metadata("12345")

Critical Minerals Coverage
--------------------------

The package covers 27 of the 50 DOE critical minerals with USGS data:

.. list-table::
   :header-rows: 1
   :widths: 20 30 20 30

   * - Code
     - Mineral
     - Code
     - Mineral
   * - ``alumi``
     - Aluminum
     - ``nicke``
     - Nickel
   * - ``antim``
     - Antimony
     - ``niobi``
     - Niobium
   * - ``arsen``
     - Arsenic
     - ``plati``
     - Platinum Group
   * - ``barit``
     - Barite
     - ``raree``
     - Rare Earths
   * - ``beryl``
     - Beryllium
     - ``tanta``
     - Tantalum
   * - ``bismu``
     - Bismuth
     - ``tellu``
     - Tellurium
   * - ``chrom``
     - Chromium
     - ``tin``
     - Tin
   * - ``cobal``
     - Cobalt
     - ``titan``
     - Titanium
   * - ``fluor``
     - Fluorspar
     - ``tungs``
     - Tungsten
   * - ``galli``
     - Gallium
     - ``vanad``
     - Vanadium
   * - ``germa``
     - Germanium
     - ``zinc``
     - Zinc
   * - ``graph``
     - Graphite
     - ``zirco-hafni``
     - Zirconium/Hafnium
   * - ``indiu``
     - Indium
     -
     -
   * - ``lithi``
     - Lithium
     -
     -
   * - ``manga``
     - Manganese
     -
     -
