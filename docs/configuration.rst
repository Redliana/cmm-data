Configuration
=============

This guide covers configuring the CMM Data package.

.. contents:: Contents
   :local:
   :depth: 2

Automatic Configuration
-----------------------

The package automatically detects the data directory by:

1. Checking the ``CMM_DATA_PATH`` environment variable
2. Searching parent directories for ``Globus_Sharing``
3. Checking common installation paths

In most cases, no manual configuration is needed.

Environment Variable
--------------------

Set the data path using an environment variable:

**Bash/Zsh:**

.. code-block:: bash

   export CMM_DATA_PATH=/path/to/Globus_Sharing

**Fish:**

.. code-block:: fish

   set -x CMM_DATA_PATH /path/to/Globus_Sharing

**Windows (PowerShell):**

.. code-block:: powershell

   $env:CMM_DATA_PATH = "C:\path\to\Globus_Sharing"

**In Python:**

.. code-block:: python

   import os
   os.environ['CMM_DATA_PATH'] = '/path/to/Globus_Sharing'

   import cmm_data
   # Now uses the configured path

Runtime Configuration
---------------------

Configure settings at runtime using the ``configure()`` function:

**Set Data Root:**

.. code-block:: python

   import cmm_data

   cmm_data.configure(data_root="/path/to/Globus_Sharing")

**Configure Caching:**

.. code-block:: python

   import cmm_data

   # Enable caching with 2-hour TTL
   cmm_data.configure(
       cache_enabled=True,
       cache_ttl_seconds=7200
   )

   # Disable caching
   cmm_data.configure(cache_enabled=False)

**Multiple Settings:**

.. code-block:: python

   import cmm_data

   cmm_data.configure(
       data_root="/path/to/Globus_Sharing",
       cache_enabled=True,
       cache_ttl_seconds=3600
   )

Configuration Object
--------------------

Access the current configuration using ``get_config()``:

.. code-block:: python

   import cmm_data

   config = cmm_data.get_config()

   # Available attributes
   print(f"Data root: {config.data_root}")
   print(f"Cache enabled: {config.cache_enabled}")
   print(f"Cache TTL: {config.cache_ttl_seconds} seconds")
   print(f"Cache directory: {config.cache_dir}")

**CMMDataConfig Attributes:**

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Attribute
     - Type
     - Description
   * - ``data_root``
     - Path
     - Root directory for data files
   * - ``cache_enabled``
     - bool
     - Whether caching is enabled
   * - ``cache_ttl_seconds``
     - int
     - Cache time-to-live in seconds
   * - ``cache_dir``
     - Path
     - Directory for disk cache

Validating Configuration
------------------------

Check which datasets are available:

.. code-block:: python

   import cmm_data

   config = cmm_data.get_config()
   status = config.validate()

   print("Dataset availability:")
   for dataset, available in status.items():
       icon = "[OK]" if available else "[--]"
       print(f"  {icon} {dataset}")

   # Output:
   # Dataset availability:
   #   [OK] usgs_commodity
   #   [OK] usgs_ore
   #   [OK] osti
   #   [OK] preprocessed
   #   [--] ga_chronostrat
   #   [--] netl_ree
   #   [OK] oecd

Dataset Paths
-------------

Each dataset has a specific location within the data root:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Dataset
     - Path
   * - USGS Commodity
     - ``USGS_Data/``
   * - USGS Ore Deposits
     - ``USGS_Ore_Deposits/``
   * - OSTI Documents
     - ``OSTI_retrieval/``
   * - Preprocessed Corpus
     - ``Data/preprocessed/``
   * - GA Chronostratigraphic
     - ``GA_149923_Chronostratigraphic/``
   * - NETL REE/Coal
     - ``NETL_REE_Coal/``
   * - OECD Supply Chain
     - ``OECD_Supply_Chain_Data/``

Caching
-------

The package provides two levels of caching:

**Memory Cache:**

- Fast, in-process caching
- Lost when Python exits
- Good for repeated access in a session

**Disk Cache:**

- Persistent across sessions
- Stored in ``cache_dir``
- Good for expensive operations

**Cache Behavior:**

.. code-block:: python

   import cmm_data

   # First load - reads from disk
   df1 = cmm_data.load_usgs_commodity("lithi", "world")

   # Second load - returns cached data
   df2 = cmm_data.load_usgs_commodity("lithi", "world")

   # Same data, no disk read
   assert df1.equals(df2)

**Clearing Cache:**

.. code-block:: python

   import cmm_data
   import shutil

   config = cmm_data.get_config()

   # Clear disk cache
   if config.cache_dir and config.cache_dir.exists():
       shutil.rmtree(config.cache_dir)
       print("Cache cleared")

**Disabling Cache:**

.. code-block:: python

   import cmm_data

   # Disable for all operations
   cmm_data.configure(cache_enabled=False)

   # Now always reads from disk
   df = cmm_data.load_usgs_commodity("lithi", "world")

Configuration Files
-------------------

The package does not use configuration files by default. However, you can
create a setup script for your project:

**config.py:**

.. code-block:: python

   # config.py - Project configuration
   import cmm_data

   def setup_cmm():
       """Configure CMM Data for this project."""
       cmm_data.configure(
           data_root="/shared/data/Globus_Sharing",
           cache_enabled=True,
           cache_ttl_seconds=86400  # 24 hours
       )

   # Run on import
   setup_cmm()

**Usage:**

.. code-block:: python

   import config  # Runs setup_cmm()
   import cmm_data

   # Now configured
   df = cmm_data.load_usgs_commodity("lithi", "world")

Troubleshooting
---------------

**Data Not Found:**

.. code-block:: python

   import cmm_data

   config = cmm_data.get_config()
   print(f"Looking for data in: {config.data_root}")

   # If None, set manually
   if config.data_root is None:
       cmm_data.configure(data_root="/correct/path")

**Cache Issues:**

.. code-block:: python

   import cmm_data

   # Disable caching to debug
   cmm_data.configure(cache_enabled=False)

   # Try loading again
   df = cmm_data.load_usgs_commodity("lithi", "world")

**Permission Errors:**

.. code-block:: python

   import cmm_data

   # Use a writable cache directory
   cmm_data.configure(
       cache_dir="/tmp/cmm_cache"
   )
