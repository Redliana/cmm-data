"""Mindat.org mineralogical database loader."""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd

from .base import BaseLoader
from ..exceptions import DataNotFoundError, ConfigurationError


# Critical mineral elements for filtering Mindat queries
# Based on DOE Critical Minerals List
CRITICAL_ELEMENTS = {
    "Li": "Lithium",
    "Co": "Cobalt",
    "Ni": "Nickel",
    "Mn": "Manganese",
    "Al": "Aluminum",
    "Cr": "Chromium",
    "Ti": "Titanium",
    "V": "Vanadium",
    "W": "Tungsten",
    "Sn": "Tin",
    "Ta": "Tantalum",
    "Nb": "Niobium",
    "Be": "Beryllium",
    "Sb": "Antimony",
    "Bi": "Bismuth",
    "As": "Arsenic",
    "Te": "Tellurium",
    "Ga": "Gallium",
    "Ge": "Germanium",
    "In": "Indium",
    "Zr": "Zirconium",
    "Hf": "Hafnium",
    "F": "Fluorine",
    "Ba": "Barium",
    "Zn": "Zinc",
    "Pt": "Platinum",
    "Pd": "Palladium",
    "Rh": "Rhodium",
    "Ir": "Iridium",
    "Ru": "Ruthenium",
    "Os": "Osmium",
    # Rare Earth Elements
    "La": "Lanthanum",
    "Ce": "Cerium",
    "Pr": "Praseodymium",
    "Nd": "Neodymium",
    "Pm": "Promethium",
    "Sm": "Samarium",
    "Eu": "Europium",
    "Gd": "Gadolinium",
    "Tb": "Terbium",
    "Dy": "Dysprosium",
    "Ho": "Holmium",
    "Er": "Erbium",
    "Tm": "Thulium",
    "Yb": "Ytterbium",
    "Lu": "Lutetium",
    "Y": "Yttrium",
    "Sc": "Scandium",
}

# Grouped elements for common queries
ELEMENT_GROUPS = {
    "ree_light": ["La", "Ce", "Pr", "Nd", "Pm", "Sm"],
    "ree_heavy": ["Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Y"],
    "ree_all": ["La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy",
                "Ho", "Er", "Tm", "Yb", "Lu", "Y", "Sc"],
    "pgm": ["Pt", "Pd", "Rh", "Ir", "Ru", "Os"],
    "battery_metals": ["Li", "Co", "Ni", "Mn"],
    "tech_metals": ["Ga", "Ge", "In", "Te"],
}


def _check_openmindat_installed() -> bool:
    """Check if openmindat package is installed."""
    try:
        import openmindat
        return True
    except ImportError:
        return False


def _check_api_key_configured() -> bool:
    """Check if Mindat API key is configured."""
    return bool(os.environ.get("MINDAT_API_KEY"))


class MindatLoader(BaseLoader):
    """
    Loader for Mindat.org mineralogical database.

    Provides access to mineral species data, localities, IMA-approved minerals,
    and classification systems (Dana, Strunz) via the OpenMindat API.

    Requirements:
        - openmindat package: pip install openmindat
        - MINDAT_API_KEY environment variable set with valid API key

    Data is cached locally in the Mindat directory for offline access
    and to minimize API calls.

    Example:
        >>> from cmm_data.loaders import MindatLoader
        >>> loader = MindatLoader()
        >>>
        >>> # Fetch minerals containing lithium
        >>> li_minerals = loader.fetch_minerals_by_element("Li")
        >>>
        >>> # Load cached data
        >>> df = loader.load(data_type="geomaterials", element="Li")
    """

    dataset_name = "mindat"

    def __init__(self, config=None, api_key: Optional[str] = None):
        """
        Initialize the Mindat loader.

        Args:
            config: Optional CMMDataConfig instance
            api_key: Optional API key (uses MINDAT_API_KEY env var if not provided)
        """
        super().__init__(config)

        if api_key:
            os.environ["MINDAT_API_KEY"] = api_key

        self._openmindat_available = _check_openmindat_installed()

    @property
    def api_configured(self) -> bool:
        """Check if API is ready for use."""
        return self._openmindat_available and _check_api_key_configured()

    def _ensure_api_ready(self) -> None:
        """Ensure API is configured and ready."""
        if not self._openmindat_available:
            raise ConfigurationError(
                "openmindat package not installed. Install with: pip install openmindat"
            )
        if not _check_api_key_configured():
            raise ConfigurationError(
                "MINDAT_API_KEY environment variable not set. "
                "Get your API key from mindat.org and set it with: "
                "os.environ['MINDAT_API_KEY'] = 'your_key'"
            )

    def _get_data_file(self, data_type: str, identifier: str) -> Path:
        """Get the path to a cached data file."""
        return self.data_path / data_type / f"{identifier}.json"

    def _save_data(self, data: Union[List, Dict], data_type: str, identifier: str) -> Path:
        """Save data to the cache directory."""
        file_path = self._get_data_file(data_type, identifier)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return file_path

    def _load_cached_data(self, data_type: str, identifier: str) -> Optional[List[Dict]]:
        """Load data from cache if available."""
        file_path = self._get_data_file(data_type, identifier)

        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def list_available(self) -> List[str]:
        """List available cached data files."""
        if not self.data_path.exists():
            return []

        available = []
        for data_type_dir in self.data_path.iterdir():
            if data_type_dir.is_dir():
                for f in data_type_dir.glob("*.json"):
                    available.append(f"{data_type_dir.name}/{f.stem}")

        return sorted(available)

    def list_cached_elements(self) -> List[str]:
        """List elements that have cached mineral data."""
        geomaterials_dir = self.data_path / "geomaterials"
        if not geomaterials_dir.exists():
            return []

        elements = []
        for f in geomaterials_dir.glob("element_*.json"):
            # Extract element symbol from filename
            elem = f.stem.replace("element_", "")
            elements.append(elem)

        return sorted(elements)

    def list_critical_elements(self) -> List[str]:
        """List all critical mineral elements."""
        return list(CRITICAL_ELEMENTS.keys())

    def get_element_name(self, symbol: str) -> str:
        """Get full element name from symbol."""
        return CRITICAL_ELEMENTS.get(symbol, symbol)

    def get_element_group(self, group_name: str) -> List[str]:
        """Get list of elements in a predefined group."""
        return ELEMENT_GROUPS.get(group_name, [])

    # =========================================================================
    # API Fetch Methods (requires openmindat and API key)
    # =========================================================================

    def fetch_minerals_by_element(
        self,
        element: str,
        ima_only: bool = True,
        save: bool = True,
        fields: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch minerals containing a specific element from Mindat API.

        Args:
            element: Element symbol (e.g., 'Li', 'Co', 'Ni')
            ima_only: If True, only return IMA-approved minerals
            save: If True, cache results locally
            fields: Optional list of fields to retrieve

        Returns:
            List of mineral dictionaries
        """
        self._ensure_api_ready()

        from openmindat import GeomaterialRetriever

        retriever = GeomaterialRetriever()
        retriever.elements_inc(element)

        if ima_only:
            retriever.ima(True)

        if fields:
            retriever.fields(",".join(fields))

        results = retriever.get_dict()

        if save and results:
            identifier = f"element_{element}"
            if ima_only:
                identifier += "_ima"
            self._save_data(results, "geomaterials", identifier)

        return results

    def fetch_minerals_by_elements(
        self,
        elements: List[str],
        ima_only: bool = True,
        save: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Fetch minerals containing ALL specified elements.

        Args:
            elements: List of element symbols
            ima_only: If True, only return IMA-approved minerals
            save: If True, cache results locally

        Returns:
            List of mineral dictionaries
        """
        self._ensure_api_ready()

        from openmindat import GeomaterialRetriever

        retriever = GeomaterialRetriever()

        for elem in elements:
            retriever.elements_inc(elem)

        if ima_only:
            retriever.ima(True)

        results = retriever.get_dict()

        if save and results:
            identifier = f"elements_{'_'.join(sorted(elements))}"
            if ima_only:
                identifier += "_ima"
            self._save_data(results, "geomaterials", identifier)

        return results

    def fetch_mineral_by_id(self, mineral_id: int, save: bool = True) -> Dict[str, Any]:
        """
        Fetch a specific mineral by its Mindat ID.

        Args:
            mineral_id: Mindat geomaterial ID
            save: If True, cache result locally

        Returns:
            Mineral data dictionary
        """
        self._ensure_api_ready()

        from openmindat import GeomaterialIdRetriever

        retriever = GeomaterialIdRetriever()
        result = retriever.id(mineral_id).get_dict()

        if save and result:
            self._save_data(result, "geomaterials", f"id_{mineral_id}")

        return result

    def fetch_mineral_by_name(
        self,
        name: str,
        save: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Search for minerals by name.

        Args:
            name: Mineral name to search for
            save: If True, cache results locally

        Returns:
            List of matching mineral dictionaries
        """
        self._ensure_api_ready()

        from openmindat import GeomaterialSearchRetriever

        retriever = GeomaterialSearchRetriever()
        results = retriever.geomaterials_search(name).get_dict()

        if save and results:
            safe_name = name.lower().replace(" ", "_")
            self._save_data(results, "geomaterials", f"search_{safe_name}")

        return results

    def fetch_ima_minerals(self, save: bool = True) -> List[Dict[str, Any]]:
        """
        Fetch all IMA-approved minerals.

        Args:
            save: If True, cache results locally

        Returns:
            List of IMA-approved mineral dictionaries
        """
        self._ensure_api_ready()

        from openmindat import MineralsIMARetriever

        retriever = MineralsIMARetriever()
        results = retriever.get_dict()

        if save and results:
            self._save_data(results, "ima", "all_minerals")

        return results

    def fetch_localities_for_mineral(
        self,
        mineral_id: int,
        save: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Fetch localities where a mineral occurs.

        Args:
            mineral_id: Mindat geomaterial ID
            save: If True, cache results locally

        Returns:
            List of locality dictionaries
        """
        self._ensure_api_ready()

        from openmindat import LocalitiesRetriever

        retriever = LocalitiesRetriever()
        results = retriever.mineral_id(mineral_id).get_dict()

        if save and results:
            self._save_data(results, "localities", f"mineral_{mineral_id}")

        return results

    def fetch_localities_by_country(
        self,
        country: str,
        save: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Fetch mineral localities in a specific country.

        Args:
            country: Country name
            save: If True, cache results locally

        Returns:
            List of locality dictionaries
        """
        self._ensure_api_ready()

        from openmindat import LocalitiesRetriever

        retriever = LocalitiesRetriever()
        results = retriever.country(country).get_dict()

        if save and results:
            safe_country = country.lower().replace(" ", "_")
            self._save_data(results, "localities", f"country_{safe_country}")

        return results

    def fetch_critical_minerals_data(
        self,
        elements: Optional[List[str]] = None,
        ima_only: bool = True,
        save: bool = True
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Fetch mineral data for all or specified critical elements.

        Args:
            elements: List of element symbols (defaults to all critical elements)
            ima_only: If True, only return IMA-approved minerals
            save: If True, cache results locally

        Returns:
            Dictionary mapping element symbols to lists of minerals
        """
        if elements is None:
            elements = list(CRITICAL_ELEMENTS.keys())

        results = {}
        for elem in elements:
            try:
                minerals = self.fetch_minerals_by_element(
                    elem, ima_only=ima_only, save=save
                )
                results[elem] = minerals
            except Exception as e:
                results[elem] = {"error": str(e)}

        return results

    # =========================================================================
    # Load Methods (for cached data)
    # =========================================================================

    def load(
        self,
        data_type: str = "geomaterials",
        element: Optional[str] = None,
        identifier: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        Load cached Mindat data as a DataFrame.

        Args:
            data_type: Type of data ('geomaterials', 'localities', 'ima')
            element: Element symbol to load minerals for
            identifier: Specific data file identifier
            **kwargs: Additional filter parameters

        Returns:
            pandas.DataFrame with the loaded data
        """
        if element:
            identifier = f"element_{element}"
            if kwargs.get("ima_only", True):
                identifier += "_ima"

        if not identifier:
            raise ValueError("Must specify either 'element' or 'identifier'")

        cache_key = self._cache_key(data_type, identifier)
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        data = self._load_cached_data(data_type, identifier)

        if data is None:
            raise DataNotFoundError(
                f"No cached data found for {data_type}/{identifier}. "
                f"Use fetch_* methods to download data first, or check available "
                f"data with list_available()."
            )

        df = pd.json_normalize(data)

        # Add element metadata if loading by element
        if element:
            df["query_element"] = element
            df["query_element_name"] = self.get_element_name(element)

        self._set_cached(cache_key, df)
        return df

    def load_all_critical_minerals(self) -> pd.DataFrame:
        """
        Load all cached critical mineral data into a single DataFrame.

        Returns:
            pandas.DataFrame with all cached mineral data
        """
        dfs = []
        for elem in self.list_cached_elements():
            if elem in CRITICAL_ELEMENTS:
                try:
                    df = self.load(element=elem)
                    dfs.append(df)
                except DataNotFoundError:
                    continue

        if not dfs:
            raise DataNotFoundError(
                "No cached critical mineral data found. "
                "Use fetch_critical_minerals_data() to download data first."
            )

        return pd.concat(dfs, ignore_index=True)

    def load_localities(self, identifier: str) -> pd.DataFrame:
        """
        Load cached locality data.

        Args:
            identifier: Locality data identifier (e.g., 'mineral_12345', 'country_usa')

        Returns:
            pandas.DataFrame with locality data
        """
        return self.load(data_type="localities", identifier=identifier)

    def load_ima_minerals(self) -> pd.DataFrame:
        """
        Load cached IMA-approved minerals list.

        Returns:
            pandas.DataFrame with IMA mineral data
        """
        return self.load(data_type="ima", identifier="all_minerals")

    # =========================================================================
    # Query Methods
    # =========================================================================

    def query(
        self,
        element: Optional[str] = None,
        crystal_system: Optional[str] = None,
        ima_status: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        Query cached mineral data with filters.

        Args:
            element: Filter by element symbol
            crystal_system: Filter by crystal system
            ima_status: Filter by IMA status
            **kwargs: Additional column filters

        Returns:
            Filtered pandas.DataFrame
        """
        if element:
            df = self.load(element=element)
        else:
            df = self.load_all_critical_minerals()

        if crystal_system and "crystalsystem" in df.columns:
            df = df[df["crystalsystem"].str.contains(crystal_system, case=False, na=False)]

        if ima_status and "ima_status" in df.columns:
            df = df[df["ima_status"] == ima_status]

        # Apply additional filters
        for col, value in kwargs.items():
            if col in df.columns:
                if isinstance(value, (list, tuple)):
                    df = df[df[col].isin(value)]
                else:
                    df = df[df[col] == value]

        return df

    def get_mineral_summary(self, element: str) -> Dict[str, Any]:
        """
        Get a summary of minerals containing an element.

        Args:
            element: Element symbol

        Returns:
            Dictionary with summary statistics
        """
        try:
            df = self.load(element=element)
        except DataNotFoundError:
            return {
                "element": element,
                "element_name": self.get_element_name(element),
                "status": "no_data",
                "mineral_count": 0
            }

        summary = {
            "element": element,
            "element_name": self.get_element_name(element),
            "status": "available",
            "mineral_count": len(df),
        }

        if "name" in df.columns:
            summary["minerals"] = df["name"].tolist()[:20]  # First 20

        if "crystalsystem" in df.columns:
            summary["crystal_systems"] = df["crystalsystem"].value_counts().to_dict()

        return summary

    # =========================================================================
    # Describe Method
    # =========================================================================

    def describe(self) -> Dict[str, Any]:
        """Describe the Mindat dataset and loader status."""
        base = super().describe()

        base["api_configured"] = self.api_configured
        base["openmindat_installed"] = self._openmindat_available
        base["api_key_set"] = _check_api_key_configured()
        base["cached_elements"] = self.list_cached_elements()
        base["critical_elements"] = list(CRITICAL_ELEMENTS.keys())
        base["element_groups"] = list(ELEMENT_GROUPS.keys())

        return base
