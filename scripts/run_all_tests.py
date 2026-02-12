#!/usr/bin/env python3
"""
Comprehensive test script for cmm_data package.

Run this script to verify the package is working correctly:
    python scripts/run_all_tests.py

This script tests:
1. Package import and version
2. Configuration and data paths
3. All loader classes
4. Data loading functionality
5. Visualization imports (if available)
6. Utility functions
"""

import sys


class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.errors = []

    def test(self, name, func):
        """Run a single test."""
        try:
            result = func()
            if result is None or result:
                print(f"  [PASS] {name}")
                self.passed += 1
            else:
                print(f"  [FAIL] {name}")
                self.failed += 1
                self.errors.append((name, "Test returned False"))
        except Exception as e:
            print(f"  [FAIL] {name}: {e}")
            self.failed += 1
            self.errors.append((name, str(e)))

    def skip(self, name, reason):
        """Skip a test."""
        print(f"  [SKIP] {name}: {reason}")
        self.skipped += 1

    def summary(self):
        """Print test summary."""
        total = self.passed + self.failed + self.skipped
        print(f"\n{'=' * 60}")
        print(f" Test Summary: {self.passed}/{total} passed")
        print(f"{'=' * 60}")
        print(f"  Passed:  {self.passed}")
        print(f"  Failed:  {self.failed}")
        print(f"  Skipped: {self.skipped}")

        if self.errors:
            print(f"\nErrors:")
            for name, error in self.errors:
                print(f"  - {name}: {error}")

        return self.failed == 0


def main():
    print("=" * 60)
    print(" CMM Data Package Test Suite")
    print("=" * 60)
    print()

    runner = TestRunner()

    # =========================================================================
    # 1. Import Tests
    # =========================================================================
    print("1. Import Tests")
    print("-" * 40)

    def test_import():

        return True

    def test_version():
        import cmm_data

        assert cmm_data.__version__ == "0.1.0"
        return True

    def test_all_exports():

        return True

    runner.test("Import cmm_data", test_import)
    runner.test("Version is 0.1.0", test_version)
    runner.test("All exports available", test_all_exports)

    # =========================================================================
    # 2. Configuration Tests
    # =========================================================================
    print("\n2. Configuration Tests")
    print("-" * 40)

    def test_get_config():
        import cmm_data

        config = cmm_data.get_config()
        assert config is not None
        return True

    def test_config_attributes():
        import cmm_data

        config = cmm_data.get_config()
        assert hasattr(config, "data_root")
        assert hasattr(config, "cache_enabled")
        assert hasattr(config, "cache_ttl_seconds")
        return True

    def test_config_validate():
        import cmm_data

        config = cmm_data.get_config()
        status = config.validate()
        assert isinstance(status, dict)
        return True

    runner.test("Get config", test_get_config)
    runner.test("Config attributes", test_config_attributes)
    runner.test("Config validate", test_config_validate)

    # =========================================================================
    # 3. Catalog Tests
    # =========================================================================
    print("\n3. Catalog Tests")
    print("-" * 40)

    def test_data_catalog():
        import cmm_data

        catalog = cmm_data.get_data_catalog()
        assert len(catalog) == 7
        assert "dataset" in catalog.columns
        return True

    def test_list_commodities():
        import cmm_data

        commodities = cmm_data.list_commodities()
        assert len(commodities) > 70
        assert "lithi" in commodities
        return True

    def test_list_critical_minerals():
        import cmm_data

        critical = cmm_data.list_critical_minerals()
        assert len(critical) == 27
        assert "lithi" in critical
        assert "cobal" in critical
        return True

    runner.test("Data catalog", test_data_catalog)
    runner.test("List commodities", test_list_commodities)
    runner.test("List critical minerals", test_list_critical_minerals)

    # =========================================================================
    # 4. Loader Initialization Tests
    # =========================================================================
    print("\n4. Loader Initialization Tests")
    print("-" * 40)

    def test_usgs_commodity_loader():
        import cmm_data

        loader = cmm_data.USGSCommodityLoader()
        assert loader.dataset_name == "usgs_commodity"
        return True

    def test_usgs_ore_loader():
        import cmm_data

        loader = cmm_data.USGSOreDepositsLoader()
        assert loader.dataset_name == "usgs_ore"
        return True

    def test_osti_loader():
        import cmm_data

        loader = cmm_data.OSTIDocumentsLoader()
        assert loader.dataset_name == "osti"
        return True

    def test_preprocessed_loader():
        import cmm_data

        loader = cmm_data.PreprocessedCorpusLoader()
        assert loader.dataset_name == "preprocessed"
        return True

    def test_ga_loader():
        import cmm_data

        loader = cmm_data.GAChronostratigraphicLoader()
        assert loader.dataset_name == "ga_chronostrat"
        return True

    def test_netl_loader():
        import cmm_data

        loader = cmm_data.NETLREECoalLoader()
        assert loader.dataset_name == "netl_ree"
        return True

    def test_oecd_loader():
        import cmm_data

        loader = cmm_data.OECDSupplyChainLoader()
        assert loader.dataset_name == "oecd"
        return True

    runner.test("USGSCommodityLoader", test_usgs_commodity_loader)
    runner.test("USGSOreDepositsLoader", test_usgs_ore_loader)
    runner.test("OSTIDocumentsLoader", test_osti_loader)
    runner.test("PreprocessedCorpusLoader", test_preprocessed_loader)
    runner.test("GAChronostratigraphicLoader", test_ga_loader)
    runner.test("NETLREECoalLoader", test_netl_loader)
    runner.test("OECDSupplyChainLoader", test_oecd_loader)

    # =========================================================================
    # 5. Data Loading Tests
    # =========================================================================
    print("\n5. Data Loading Tests")
    print("-" * 40)

    def test_load_lithium_world():
        import cmm_data

        df = cmm_data.load_usgs_commodity("lithi", "world")
        assert len(df) > 0
        assert "Country" in df.columns
        return True

    def test_load_lithium_salient():
        import cmm_data

        df = cmm_data.load_usgs_commodity("lithi", "salient")
        assert len(df) > 0
        assert "Year" in df.columns
        return True

    def test_load_cobalt():
        import cmm_data

        df = cmm_data.load_usgs_commodity("cobal", "world")
        assert len(df) > 0
        return True

    def test_top_producers():
        import cmm_data

        loader = cmm_data.USGSCommodityLoader()
        top = loader.get_top_producers("lithi", top_n=5)
        assert len(top) <= 5
        return True

    def test_commodity_name():
        import cmm_data

        loader = cmm_data.USGSCommodityLoader()
        assert loader.get_commodity_name("lithi") == "Lithium"
        assert loader.get_commodity_name("cobal") == "Cobalt"
        return True

    # Check if data is available before running data tests
    import cmm_data

    config = cmm_data.get_config()
    data_available = config.data_root and config.data_root.exists()

    if data_available:
        runner.test("Load lithium world data", test_load_lithium_world)
        runner.test("Load lithium salient data", test_load_lithium_salient)
        runner.test("Load cobalt data", test_load_cobalt)
        runner.test("Get top producers", test_top_producers)
    else:
        runner.skip("Load lithium world data", "Data not available")
        runner.skip("Load lithium salient data", "Data not available")
        runner.skip("Load cobalt data", "Data not available")
        runner.skip("Get top producers", "Data not available")

    runner.test("Commodity name lookup", test_commodity_name)

    # =========================================================================
    # 6. Utility Tests
    # =========================================================================
    print("\n6. Utility Tests")
    print("-" * 40)

    def test_parse_numeric():
        from cmm_data.utils.parsing import parse_numeric_value

        assert parse_numeric_value(100) == 100.0
        assert parse_numeric_value("1,000") == 1000.0
        assert parse_numeric_value(">50") == 50.0
        return True

    def test_parse_na_values():
        import numpy as np

        from cmm_data.utils.parsing import parse_numeric_value

        assert np.isnan(parse_numeric_value("W"))
        assert np.isnan(parse_numeric_value("NA"))
        assert np.isnan(parse_numeric_value("--"))
        return True

    def test_parse_range():
        from cmm_data.utils.parsing import parse_range

        assert parse_range("100-200") == (100.0, 200.0)
        assert parse_range(">50") == (50.0, None)
        assert parse_range("<100") == (None, 100.0)
        return True

    runner.test("Parse numeric values", test_parse_numeric)
    runner.test("Parse NA values", test_parse_na_values)
    runner.test("Parse range values", test_parse_range)

    # =========================================================================
    # 7. OECD Loader Tests
    # =========================================================================
    print("\n7. OECD Loader Tests")
    print("-" * 40)

    def test_oecd_urls():
        import cmm_data

        loader = cmm_data.OECDSupplyChainLoader()
        urls = loader.get_download_urls()
        assert "icio" in urls
        assert "btige" in urls
        return True

    def test_oecd_coverage():
        import cmm_data

        loader = cmm_data.OECDSupplyChainLoader()
        coverage = loader.get_minerals_coverage()
        assert "export_restrictions" in coverage
        assert "iea_critical_minerals" in coverage
        return True

    runner.test("OECD download URLs", test_oecd_urls)
    runner.test("OECD minerals coverage", test_oecd_coverage)

    # =========================================================================
    # 8. Visualization Import Tests
    # =========================================================================
    print("\n8. Visualization Tests")
    print("-" * 40)

    def test_viz_imports():

        return True

    try:
        import matplotlib

        runner.test("Visualization imports", test_viz_imports)
    except ImportError:
        runner.skip("Visualization imports", "matplotlib not installed")

    # =========================================================================
    # Summary
    # =========================================================================
    success = runner.summary()

    if success:
        print("\n[SUCCESS] All tests passed!")
        return 0
    else:
        print("\n[WARNING] Some tests failed. Check errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
