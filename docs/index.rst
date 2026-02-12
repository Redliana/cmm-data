CMM Data Documentation
======================

**Critical Minerals Modeling Data Access Library**

.. image:: https://img.shields.io/badge/python-3.9+-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python 3.9+

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License: MIT

A comprehensive Python package providing unified access to datasets for critical minerals
supply chain modeling. Developed by Pacific Northwest National Laboratory (PNNL) for the
Critical Minerals Modeling (CMM) project.

Quick Start
-----------

.. code-block:: python

   import cmm_data

   # View available datasets
   catalog = cmm_data.get_data_catalog()
   print(catalog)

   # Load lithium production data
   df = cmm_data.load_usgs_commodity("lithi", "world")
   print(df)

   # Get critical minerals list
   critical = cmm_data.list_critical_minerals()
   print(critical)

Features
--------

* **Unified API** - Single interface for 7 different data sources
* **80+ Commodities** - Complete USGS Mineral Commodity Summaries coverage
* **Data Parsing** - Automatic handling of W (withheld), NA, ranges, and special codes
* **Caching** - Built-in memory and disk caching for performance
* **Visualizations** - Production charts, time series, import reliance plots
* **Type Safety** - Full type hints for IDE support

Installation
------------

.. code-block:: bash

   # Basic installation
   pip install -e cmm_data

   # With visualization support
   pip install -e "cmm_data[viz]"

   # With geospatial support
   pip install -e "cmm_data[geo]"

   # Full installation
   pip install -e "cmm_data[full]"

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   quickstart
   configuration
   datasets

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/modules
   api/loaders
   api/visualizations
   api/utilities

.. toctree::
   :maxdepth: 1
   :caption: Development

   contributing
   changelog

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
