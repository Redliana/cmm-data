Quick Start
===========

Get up and running with CMM Data in 5 minutes.

.. contents:: Contents
   :local:
   :depth: 2

Installation
------------

.. code-block:: bash

   cd /path/to/Globus_Sharing
   pip install -e cmm_data

Basic Usage
-----------

**Import the Package:**

.. code-block:: python

   import cmm_data

   # Check version
   print(f"CMM Data version: {cmm_data.__version__}")

**View Available Datasets:**

.. code-block:: python

   # Get data catalog
   catalog = cmm_data.get_data_catalog()
   print(catalog)

   # Output:
   #      dataset                  name  available
   # 0   usgs_commodity  USGS Commodity       True
   # 1   usgs_ore       USGS Ore Deposits    True
   # ...

**List Commodities:**

.. code-block:: python

   # All commodities
   commodities = cmm_data.list_commodities()
   print(f"Available: {len(commodities)} commodities")

   # Critical minerals only
   critical = cmm_data.list_critical_minerals()
   print(f"Critical minerals: {critical}")

Loading USGS Data
-----------------

**World Production Data:**

.. code-block:: python

   # Load lithium world production
   df = cmm_data.load_usgs_commodity("lithi", "world")
   print(df[['Country', 'Prod_t_est_2022', 'Reserves_t']])

   # Output:
   #          Country  Prod_t_est_2022   Reserves_t
   # 0      Australia          61000.0   6200000.0
   # 1          Chile          39000.0   9300000.0
   # 2          China          19000.0   2000000.0
   # ...

**Salient Statistics (U.S. Time Series):**

.. code-block:: python

   # Load cobalt salient statistics
   df = cmm_data.load_usgs_commodity("cobal", "salient")
   print(df[['Year', 'Imports_t', 'NIR_pct']])

   # Output:
   #    Year  Imports_t  NIR_pct
   # 0  2018      8500     76%
   # 1  2019      7800     72%
   # ...

Using Loader Classes
--------------------

**USGS Commodity Loader:**

.. code-block:: python

   from cmm_data import USGSCommodityLoader

   loader = USGSCommodityLoader()

   # Get top producers
   top = loader.get_top_producers("raree", top_n=5)
   print(top[['Country', 'Prod_t_est_2022']])

   # Get commodity name from code
   print(loader.get_commodity_name("lithi"))  # "Lithium"

**USGS Ore Deposits Loader:**

.. code-block:: python

   from cmm_data import USGSOreDepositsLoader

   loader = USGSOreDepositsLoader()

   # Get REE samples
   ree = loader.get_ree_samples()
   print(f"REE samples: {len(ree)}")

   # Get element statistics
   stats = loader.get_element_statistics("La")
   print(f"Lanthanum mean: {stats['mean']:.1f} ppm")

**Preprocessed Corpus Loader:**

.. code-block:: python

   from cmm_data import PreprocessedCorpusLoader

   loader = PreprocessedCorpusLoader()

   # Get corpus stats
   stats = loader.get_corpus_stats()
   print(f"Documents: {stats['total_documents']}")

   # Search documents
   results = loader.search("lithium extraction", limit=5)
   for _, doc in results.iterrows():
       print(f"  - {doc['title'][:50]}")

Creating Visualizations
-----------------------

**Install Visualization Dependencies:**

.. code-block:: bash

   pip install -e "cmm_data[viz]"

**World Production Chart:**

.. code-block:: python

   import cmm_data
   from cmm_data.visualizations.commodity import plot_world_production

   # Load data
   df = cmm_data.load_usgs_commodity("lithi", "world")

   # Create chart
   fig = plot_world_production(df, "Lithium", top_n=10)
   fig.savefig("lithium_producers.png")

**Time Series Chart:**

.. code-block:: python

   from cmm_data.visualizations.commodity import plot_production_timeseries

   df = cmm_data.load_usgs_commodity("cobal", "salient")
   fig = plot_production_timeseries(df, "Cobalt")
   fig.savefig("cobalt_timeseries.png")

Configuration
-------------

**Set Data Path:**

.. code-block:: python

   import cmm_data

   # Configure data root
   cmm_data.configure(data_root="/path/to/Globus_Sharing")

   # Or use environment variable
   import os
   os.environ['CMM_DATA_PATH'] = '/path/to/Globus_Sharing'

**Check Configuration:**

.. code-block:: python

   config = cmm_data.get_config()
   print(f"Data root: {config.data_root}")

   # Validate datasets
   status = config.validate()
   for dataset, available in status.items():
       icon = "[OK]" if available else "[--]"
       print(f"  {icon} {dataset}")

Common Commodity Codes
----------------------

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Code
     - Commodity
     - Critical Mineral?
   * - ``lithi``
     - Lithium
     - Yes
   * - ``cobal``
     - Cobalt
     - Yes
   * - ``nicke``
     - Nickel
     - Yes
   * - ``raree``
     - Rare Earths
     - Yes
   * - ``graph``
     - Graphite
     - Yes
   * - ``manga``
     - Manganese
     - Yes
   * - ``coppe``
     - Copper
     - No
   * - ``gold``
     - Gold
     - No

Next Steps
----------

* :doc:`configuration` - Configure data paths and caching
* :doc:`datasets` - Learn about available datasets
* :doc:`api/loaders` - Full loader API reference
* :doc:`api/visualizations` - Visualization functions
