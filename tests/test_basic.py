"""Basic tests for cmm_data package."""

from __future__ import annotations


def test_import():
    """Test that the package can be imported."""
    import cmm_data

    assert cmm_data.__version__ == "0.1.0"


def test_list_commodities():
    """Test listing commodities."""
    import cmm_data

    commodities = cmm_data.list_commodities()
    assert isinstance(commodities, list)
    assert len(commodities) > 0
    assert "lithi" in commodities
    assert "cobal" in commodities


def test_list_critical_minerals():
    """Test listing critical minerals."""
    import cmm_data

    critical = cmm_data.list_critical_minerals()
    assert isinstance(critical, list)
    assert len(critical) > 0
    assert "lithi" in critical


def test_get_data_catalog():
    """Test getting data catalog."""
    import cmm_data

    catalog = cmm_data.get_data_catalog()
    assert len(catalog) == 7
    assert "dataset" in catalog.columns
    assert "name" in catalog.columns
    assert "available" in catalog.columns


def test_config():
    """Test configuration."""
    import cmm_data

    config = cmm_data.get_config()
    assert config is not None
    assert hasattr(config, "data_root")
    assert hasattr(config, "cache_enabled")


def test_usgs_commodity_loader_init():
    """Test USGSCommodityLoader initialization."""
    import cmm_data

    loader = cmm_data.USGSCommodityLoader()
    assert loader is not None
    assert loader.dataset_name == "usgs_commodity"


def test_commodity_names():
    """Test commodity name lookup."""
    from cmm_data.loaders.usgs_commodity import COMMODITY_NAMES

    assert "lithi" in COMMODITY_NAMES
    assert COMMODITY_NAMES["lithi"] == "Lithium"
    assert COMMODITY_NAMES["cobal"] == "Cobalt"


def test_exceptions():
    """Test custom exceptions."""
    from cmm_data.exceptions import CMMDataError, ConfigurationError, DataNotFoundError

    assert issubclass(DataNotFoundError, CMMDataError)
    assert issubclass(ConfigurationError, CMMDataError)


def test_parsing_utilities():
    """Test parsing utilities."""
    from cmm_data.utils.parsing import parse_numeric_value

    assert parse_numeric_value(100) == 100.0
    assert parse_numeric_value("1,000") == 1000.0
    assert parse_numeric_value(">50") == 50.0

    import numpy as np

    assert np.isnan(parse_numeric_value("W"))
    assert np.isnan(parse_numeric_value("NA"))
    assert np.isnan(parse_numeric_value("--"))


class TestUSGSCommodityLoader:
    """Tests for USGSCommodityLoader."""

    def test_list_available(self):
        """Test listing available commodities."""
        import cmm_data

        loader = cmm_data.USGSCommodityLoader()
        available = loader.list_available()
        # May be empty if data not available, but should be a list
        assert isinstance(available, list)

    def test_get_commodity_name(self):
        """Test getting commodity name from code."""
        import cmm_data

        loader = cmm_data.USGSCommodityLoader()
        assert loader.get_commodity_name("lithi") == "Lithium"
        assert loader.get_commodity_name("unknown") == "Unknown"

    def test_describe(self):
        """Test describe method."""
        import cmm_data

        loader = cmm_data.USGSCommodityLoader()
        desc = loader.describe()
        assert isinstance(desc, dict)
        assert "name" in desc


class TestOECDLoader:
    """Tests for OECDSupplyChainLoader."""

    def test_init(self):
        """Test initialization."""
        import cmm_data

        loader = cmm_data.OECDSupplyChainLoader()
        assert loader.dataset_name == "oecd"

    def test_get_download_urls(self):
        """Test getting download URLs."""
        import cmm_data

        loader = cmm_data.OECDSupplyChainLoader()
        urls = loader.get_download_urls()
        assert isinstance(urls, dict)
        assert "icio" in urls
        assert "btige" in urls

    def test_get_minerals_coverage(self):
        """Test getting minerals coverage."""
        import cmm_data

        loader = cmm_data.OECDSupplyChainLoader()
        coverage = loader.get_minerals_coverage()
        assert isinstance(coverage, dict)
        assert "export_restrictions" in coverage
