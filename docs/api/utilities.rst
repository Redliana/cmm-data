Utilities
=========

The utilities module provides helper functions for data parsing and caching.

.. contents:: Contents
   :local:
   :depth: 2

Parsing Utilities
-----------------

Functions for parsing USGS data values, which often contain special codes
and formatting that need to be converted to numeric values.

**Handling Special Codes:**

USGS data uses several special codes:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Code
     - Meaning
   * - ``W``
     - Withheld to avoid disclosing company proprietary data
   * - ``NA``
     - Not available
   * - ``--``
     - Zero or no data
   * - ``e``
     - Estimated
   * - ``r``
     - Revised
   * - ``p``
     - Preliminary
   * - ``>50``
     - Greater than 50
   * - ``<100``
     - Less than 100
   * - ``100-200``
     - Range between 100 and 200

**Example Usage:**

.. code-block:: python

   from cmm_data.utils.parsing import parse_numeric_value, parse_range

   # Parse numeric values
   parse_numeric_value(100)        # Returns: 100.0
   parse_numeric_value("1,000")    # Returns: 1000.0
   parse_numeric_value(">50")      # Returns: 50.0
   parse_numeric_value("W")        # Returns: nan
   parse_numeric_value("NA")       # Returns: nan
   parse_numeric_value("--")       # Returns: nan

   # Parse ranges
   parse_range("100-200")          # Returns: (100.0, 200.0)
   parse_range(">50")              # Returns: (50.0, None)
   parse_range("<100")             # Returns: (None, 100.0)

.. automodule:: cmm_data.utils.parsing
   :members:
   :undoc-members:
   :show-inheritance:

Caching Utilities
-----------------

The caching module provides infrastructure for memory and disk caching
to improve performance when loading large datasets repeatedly.

**Cache Configuration:**

Caching can be configured through the main configuration:

.. code-block:: python

   import cmm_data

   # Enable caching (default)
   cmm_data.configure(cache_enabled=True)

   # Set cache TTL (time-to-live) in seconds
   cmm_data.configure(cache_ttl_seconds=3600)  # 1 hour

   # Disable caching
   cmm_data.configure(cache_enabled=False)

**Cache Behavior:**

- **Memory Cache**: Fast, in-process caching for repeated access
- **Disk Cache**: Persistent caching for expensive operations
- **TTL**: Cached items expire after the configured time-to-live
- **Automatic Invalidation**: Cache is cleared when data files change

**Clearing Cache:**

.. code-block:: python

   import cmm_data
   import shutil

   config = cmm_data.get_config()

   # Clear disk cache
   if config.cache_dir and config.cache_dir.exists():
       shutil.rmtree(config.cache_dir)

   # Or disable caching entirely
   cmm_data.configure(cache_enabled=False)

.. automodule:: cmm_data.utils.caching
   :members:
   :undoc-members:
   :show-inheritance:

Utility Module
--------------

.. automodule:: cmm_data.utils
   :members:
   :undoc-members:
   :show-inheritance:

Function Reference
------------------

Parsing Functions
^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Function
     - Description
   * - ``parse_numeric_value(value)``
     - Convert value to float, handling special codes
   * - ``parse_range(value)``
     - Parse range strings like "100-200" or ">50"
   * - ``clean_column_name(name)``
     - Standardize column names
   * - ``standardize_country_name(name)``
     - Normalize country name variations

Caching Functions
^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Function/Class
     - Description
   * - ``MemoryCache``
     - In-memory LRU cache with TTL
   * - ``DiskCache``
     - Persistent disk-based cache
   * - ``cached(ttl)``
     - Decorator for caching function results
   * - ``clear_cache()``
     - Clear all cached data
