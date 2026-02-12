#!/usr/bin/env python3
"""
Verify cmm_data installation and data availability.

Run this script after installation to check that everything is working:
    python scripts/verify_installation.py
"""

from __future__ import annotations

import sys


def print_header(text):
    print(f"\n{'=' * 60}")
    print(f" {text}")
    print("=" * 60)


def print_status(name, status, details=""):
    icon = "[OK]" if status else "[--]"
    print(f"  {icon} {name}" + (f": {details}" if details else ""))


def main():
    print_header("CMM Data Installation Verification")

    errors = []

    # 1. Check import
    print("\n1. Checking package import...")
    try:
        import cmm_data

        print_status("cmm_data import", True, f"version {cmm_data.__version__}")
    except ImportError as e:
        print_status("cmm_data import", False, str(e))
        errors.append("Package not installed correctly")
        print("\n[ERROR] Cannot continue without cmm_data installed.")
        print("Run: pip install -e /path/to/cmm_data")
        return 1

    # 2. Check configuration
    print("\n2. Checking configuration...")
    try:
        config = cmm_data.get_config()
        if config.data_root and config.data_root.exists():
            print_status("Data root", True, str(config.data_root))
        else:
            print_status("Data root", False, "Not found or not configured")
            errors.append("Data root not configured")
    except Exception as e:
        print_status("Configuration", False, str(e))
        errors.append("Configuration error")

    # 3. Check dataset availability
    print("\n3. Checking dataset availability...")
    try:
        catalog = cmm_data.get_data_catalog()
        for _, row in catalog.iterrows():
            print_status(row["dataset"], row["available"], row["name"])

        available_count = catalog["available"].sum()
        total_count = len(catalog)
        print(f"\n  Available: {available_count}/{total_count} datasets")

        if available_count == 0:
            errors.append("No datasets available")
    except Exception as e:
        print_status("Data catalog", False, str(e))
        errors.append("Cannot read data catalog")

    # 4. Check core loaders
    print("\n4. Checking core loaders...")
    loaders_to_check = [
        ("USGSCommodityLoader", "usgs_commodity"),
        ("USGSOreDepositsLoader", "usgs_ore"),
        ("PreprocessedCorpusLoader", "preprocessed"),
        ("OECDSupplyChainLoader", "oecd"),
    ]

    for loader_name, dataset_key in loaders_to_check:
        try:
            loader_class = getattr(cmm_data, loader_name)
            loader = loader_class()
            available = loader.list_available()
            print_status(loader_name, True, f"{len(available)} items")
        except Exception as e:
            print_status(loader_name, False, str(e))

    # 5. Test data loading
    print("\n5. Testing data loading...")
    try:
        df = cmm_data.load_usgs_commodity("lithi", "world")
        print_status("Load lithium data", True, f"{len(df)} rows")
    except Exception as e:
        print_status("Load lithium data", False, str(e))
        errors.append("Cannot load sample data")

    # 6. Check optional dependencies
    print("\n6. Checking optional dependencies...")

    # Visualization
    try:
        import matplotlib

        print_status("matplotlib (viz)", True, matplotlib.__version__)
    except ImportError:
        print_status("matplotlib (viz)", False, "pip install cmm-data[viz]")

    # Geospatial
    try:
        import geopandas

        print_status("geopandas (geo)", True, geopandas.__version__)
    except ImportError:
        print_status("geopandas (geo)", False, "pip install cmm-data[geo]")

    try:
        import rasterio

        print_status("rasterio (geo)", True, rasterio.__version__)
    except ImportError:
        print_status("rasterio (geo)", False, "pip install cmm-data[geo]")

    # Summary
    print_header("Summary")

    if errors:
        print(f"\n[WARNING] {len(errors)} issue(s) found:")
        for err in errors:
            print(f"  - {err}")
        print("\nSee README.md for setup instructions.")
        return 1
    else:
        print("\n[SUCCESS] All checks passed!")
        print("\nYou can now use cmm_data:")
        print("  import cmm_data")
        print("  df = cmm_data.load_usgs_commodity('lithi', 'world')")
        return 0


if __name__ == "__main__":
    sys.exit(main())
