Data Loaders
============

The loaders module provides classes for accessing different data sources.
All loaders inherit from :class:`~cmm_data.loaders.base.BaseLoader` and provide
a consistent interface.

.. contents:: Contents
   :local:
   :depth: 2

Base Loader
-----------

.. automodule:: cmm_data.loaders.base
   :members:
   :undoc-members:
   :show-inheritance:

USGS Commodity Loader
---------------------

Provides access to USGS Mineral Commodity Summaries data for 80+ commodities.

**Example Usage:**

.. code-block:: python

   from cmm_data import USGSCommodityLoader

   loader = USGSCommodityLoader()

   # List available commodities
   commodities = loader.list_available()

   # Load world production data
   df = loader.load_world_production("lithi")

   # Get top producers
   top = loader.get_top_producers("lithi", top_n=10)

.. automodule:: cmm_data.loaders.usgs_commodity
   :members:
   :undoc-members:
   :show-inheritance:

USGS Ore Deposits Loader
------------------------

Provides access to the USGS National Geochemical Database for ore deposits.

**Example Usage:**

.. code-block:: python

   from cmm_data import USGSOreDepositsLoader

   loader = USGSOreDepositsLoader()

   # Load geology data
   geology = loader.load_geology()

   # Get REE samples
   ree = loader.get_ree_samples()

   # Get element statistics
   stats = loader.get_element_statistics("La")

.. automodule:: cmm_data.loaders.usgs_ore
   :members:
   :undoc-members:
   :show-inheritance:

OSTI Documents Loader
---------------------

Provides access to DOE OSTI technical reports and documents.

**Example Usage:**

.. code-block:: python

   from cmm_data import OSTIDocumentsLoader

   loader = OSTIDocumentsLoader()

   # Search documents
   results = loader.search_documents("lithium extraction")

   # Get document metadata
   metadata = loader.get_document_metadata("12345")

.. automodule:: cmm_data.loaders.osti_docs
   :members:
   :undoc-members:
   :show-inheritance:

Preprocessed Corpus Loader
--------------------------

Provides access to the preprocessed document corpus for LLM training.

**Example Usage:**

.. code-block:: python

   from cmm_data import PreprocessedCorpusLoader

   loader = PreprocessedCorpusLoader()

   # Get corpus statistics
   stats = loader.get_corpus_stats()

   # Search documents
   results = loader.search("rare earth elements", limit=10)

   # Iterate over documents
   for doc in loader.iter_documents():
       print(doc['title'])

.. automodule:: cmm_data.loaders.preprocessed
   :members:
   :undoc-members:
   :show-inheritance:

GA Chronostratigraphic Loader
-----------------------------

Provides access to Geoscience Australia's 3D chronostratigraphic model.

**Example Usage:**

.. code-block:: python

   from cmm_data import GAChronostratigraphicLoader

   loader = GAChronostratigraphicLoader()

   # List available surfaces
   surfaces = loader.list_surfaces()

   # Load surface data
   data = loader.load("Paleozoic_Top", format="xyz")

   # Get model info
   info = loader.get_model_info()

.. automodule:: cmm_data.loaders.ga_chronostrat
   :members:
   :undoc-members:
   :show-inheritance:

NETL REE Coal Loader
--------------------

Provides access to NETL's REE and Coal geodatabase.

**Example Usage:**

.. code-block:: python

   from cmm_data import NETLREECoalLoader

   loader = NETLREECoalLoader()

   # List available layers
   layers = loader.list_available()

   # Get REE samples
   samples = loader.get_ree_samples()

   # Get REE statistics
   stats = loader.get_ree_statistics()

.. automodule:: cmm_data.loaders.netl_ree
   :members:
   :undoc-members:
   :show-inheritance:

OECD Supply Chain Loader
------------------------

Provides access to OECD/IEA supply chain data and reports.

**Example Usage:**

.. code-block:: python

   from cmm_data import OECDSupplyChainLoader

   loader = OECDSupplyChainLoader()

   # Get available datasets
   available = loader.list_available()

   # Get export restrictions reports
   reports = loader.get_export_restrictions_reports()

   # Get minerals coverage info
   coverage = loader.get_minerals_coverage()

   # Get download URLs
   urls = loader.get_download_urls()

.. automodule:: cmm_data.loaders.oecd_supply
   :members:
   :undoc-members:
   :show-inheritance:

Loader Comparison
-----------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25

   * - Loader
     - Data Source
     - Records
     - Format
   * - USGSCommodityLoader
     - USGS MCS 2023
     - 80+ commodities
     - CSV
   * - USGSOreDepositsLoader
     - USGS NGDB
     - 356 fields
     - CSV
   * - OSTIDocumentsLoader
     - DOE OSTI
     - Variable
     - JSON
   * - PreprocessedCorpusLoader
     - CMM Corpus
     - 3,298 docs
     - JSONL
   * - GAChronostratigraphicLoader
     - Geoscience Australia
     - 9 surfaces
     - GeoTIFF/XYZ
   * - NETLREECoalLoader
     - NETL
     - Variable
     - Geodatabase
   * - OECDSupplyChainLoader
     - OECD/IEA
     - Multiple
     - PDF/CSV
