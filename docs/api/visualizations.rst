Visualizations
==============

The visualizations module provides functions for creating charts and plots
from CMM data. These require the ``viz`` optional dependencies.

.. contents:: Contents
   :local:
   :depth: 2

Installation
------------

To use visualization functions, install with the ``viz`` extra:

.. code-block:: bash

   pip install -e "cmm_data[viz]"

This installs matplotlib and plotly.

Commodity Visualizations
------------------------

Functions for visualizing commodity production, trade, and reserves data.

**World Production Chart:**

.. code-block:: python

   import cmm_data
   from cmm_data.visualizations.commodity import plot_world_production

   # Load lithium data
   df = cmm_data.load_usgs_commodity("lithi", "world")

   # Create bar chart of top producers
   fig = plot_world_production(df, "Lithium", top_n=10)
   fig.savefig("lithium_producers.png")

**Production Time Series:**

.. code-block:: python

   import cmm_data
   from cmm_data.visualizations.commodity import plot_production_timeseries

   # Load salient statistics
   df = cmm_data.load_usgs_commodity("cobal", "salient")

   # Create time series plot
   fig = plot_production_timeseries(df, "Cobalt")
   fig.savefig("cobalt_timeseries.png")

**Import Reliance Chart:**

.. code-block:: python

   import cmm_data
   from cmm_data.visualizations.commodity import plot_import_reliance

   # Load rare earths data
   df = cmm_data.load_usgs_commodity("raree", "salient")

   # Create import reliance chart
   fig = plot_import_reliance(df, "Rare Earths")
   fig.savefig("ree_import_reliance.png")

.. automodule:: cmm_data.visualizations.commodity
   :members:
   :undoc-members:
   :show-inheritance:

Time Series Visualizations
--------------------------

Functions for time series analysis and comparison plots.

**Critical Minerals Comparison:**

.. code-block:: python

   from cmm_data.visualizations.timeseries import plot_critical_minerals_comparison

   # Compare import values across critical minerals
   fig = plot_critical_minerals_comparison(metric="Imports_t", top_n=15)
   fig.savefig("critical_minerals_comparison.png")

.. automodule:: cmm_data.visualizations.timeseries
   :members:
   :undoc-members:
   :show-inheritance:

Geospatial Visualizations
-------------------------

Functions for mapping deposit locations and spatial data.
Requires the ``geo`` optional dependencies.

.. code-block:: bash

   pip install -e "cmm_data[geo]"

**Deposit Location Map:**

.. code-block:: python

   from cmm_data.visualizations.geospatial import plot_deposit_locations

   # Plot ore deposit locations
   fig = plot_deposit_locations(deposits_df, title="Global Ore Deposits")
   fig.savefig("deposit_map.png")

.. automodule:: cmm_data.visualizations.geospatial
   :members:
   :undoc-members:
   :show-inheritance:

Multi-Panel Figures
-------------------

Example of creating custom multi-panel figures:

.. code-block:: python

   import cmm_data
   from cmm_data.visualizations.commodity import (
       plot_world_production,
       plot_production_timeseries,
       plot_import_reliance
   )
   import matplotlib.pyplot as plt

   # Create 2x2 subplot figure
   fig, axes = plt.subplots(2, 2, figsize=(14, 10))

   # Panel 1: Lithium producers
   df_world = cmm_data.load_usgs_commodity("lithi", "world")
   plot_world_production(df_world, "Lithium", top_n=6, ax=axes[0, 0])

   # Panel 2: Lithium time series
   df_salient = cmm_data.load_usgs_commodity("lithi", "salient")
   plot_production_timeseries(df_salient, "Lithium", ax=axes[0, 1])

   # Panel 3: Cobalt producers
   df_world = cmm_data.load_usgs_commodity("cobal", "world")
   plot_world_production(df_world, "Cobalt", top_n=6, ax=axes[1, 0])

   # Panel 4: Cobalt import reliance
   df_salient = cmm_data.load_usgs_commodity("cobal", "salient")
   plot_import_reliance(df_salient, "Cobalt", ax=axes[1, 1])

   plt.tight_layout()
   plt.savefig("critical_minerals_dashboard.png", dpi=150)

Function Summary
----------------

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Function
     - Description
   * - ``plot_world_production()``
     - Bar chart of top producing countries
   * - ``plot_production_timeseries()``
     - Time series of production/trade data
   * - ``plot_import_reliance()``
     - U.S. net import reliance chart
   * - ``plot_deposit_locations()``
     - Geospatial map of deposit locations
   * - ``plot_ree_distribution()``
     - REE concentration distribution
   * - ``plot_critical_minerals_comparison()``
     - Compare metrics across minerals
