Installation
============

This guide covers installing the CMM Data package and its dependencies.

.. contents:: Contents
   :local:
   :depth: 2

Requirements
------------

**System Requirements:**

* Python 3.9 or higher
* pip package manager
* Access to the Globus_Sharing data directory

**Required Dependencies:**

* pandas >= 2.0.0
* numpy >= 1.24.0

**Optional Dependencies:**

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Extra
     - Packages
     - Use Case
   * - ``viz``
     - matplotlib, plotly
     - Visualization functions
   * - ``geo``
     - geopandas, rasterio, fiona
     - Geospatial data
   * - ``full``
     - All optional packages
     - Complete functionality

Basic Installation
------------------

**From Source (Development Mode):**

.. code-block:: bash

   # Navigate to the data directory
   cd /path/to/Globus_Sharing

   # Install in development mode
   pip install -e cmm_data

**Verify Installation:**

.. code-block:: python

   import cmm_data
   print(f"Version: {cmm_data.__version__}")
   print(cmm_data.get_data_catalog())

Installation with Extras
------------------------

**Visualization Support:**

.. code-block:: bash

   pip install -e "cmm_data[viz]"

This enables:

* ``plot_world_production()``
* ``plot_production_timeseries()``
* ``plot_import_reliance()``

**Geospatial Support:**

.. code-block:: bash

   pip install -e "cmm_data[geo]"

This enables:

* ``NETLREECoalLoader`` with geometry
* ``GAChronostratigraphicLoader`` GeoTIFF support
* ``plot_deposit_locations()``

**Full Installation:**

.. code-block:: bash

   pip install -e "cmm_data[full]"

Virtual Environment
-------------------

**Recommended: Using a Virtual Environment**

.. code-block:: bash

   # Create virtual environment
   python3 -m venv .venv

   # Activate (Linux/macOS)
   source .venv/bin/activate

   # Activate (Windows)
   .venv\Scripts\activate

   # Install package
   pip install -e "cmm_data[full]"

**Using Conda:**

.. code-block:: bash

   # Create conda environment
   conda create -n cmm python=3.11
   conda activate cmm

   # Install package
   pip install -e "cmm_data[full]"

Installing from Wheel
---------------------

If you received a pre-built wheel file:

.. code-block:: bash

   # Install wheel
   pip install cmm_data-0.1.0-py3-none-any.whl

   # Or with extras
   pip install "cmm_data[full] @ file:///path/to/cmm_data-0.1.0-py3-none-any.whl"

Building a Wheel
----------------

To build a wheel for distribution:

.. code-block:: bash

   # Install build tool
   pip install build

   # Build wheel
   cd /path/to/cmm_data
   python -m build

   # Output in dist/
   # - cmm_data-0.1.0-py3-none-any.whl
   # - cmm_data-0.1.0.tar.gz

Troubleshooting
---------------

**Import Error:**

.. code-block:: bash

   # Check installation
   pip list | grep cmm

   # Reinstall
   pip uninstall cmm-data
   pip install -e /path/to/cmm_data

**Missing Dependencies:**

.. code-block:: bash

   # Install missing dependencies
   pip install pandas numpy

   # For visualizations
   pip install matplotlib plotly

   # For geospatial
   pip install geopandas rasterio fiona

**Data Not Found:**

.. code-block:: python

   import cmm_data

   # Check configuration
   config = cmm_data.get_config()
   print(f"Data root: {config.data_root}")

   # Reconfigure if needed
   cmm_data.configure(data_root="/correct/path/to/Globus_Sharing")

**Running Verification:**

.. code-block:: bash

   # Run verification script
   python cmm_data/scripts/verify_installation.py

   # Run full test suite
   python cmm_data/scripts/run_all_tests.py
