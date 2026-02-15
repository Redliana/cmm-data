"""Loader facade for Google Scholar search results."""

from __future__ import annotations

import pandas as pd

from ..clients import GoogleScholarClient
from .base import BaseLoader


class GoogleScholarLoader(BaseLoader):
    """Expose Google Scholar search results through the loader interface."""

    dataset_name = "google_scholar"

    def __init__(self, api_key: str | None = None, config=None):
        super().__init__(config=config)
        self.client = GoogleScholarClient(api_key=api_key)

    def list_available(self) -> list[str]:
        """Google Scholar is query-driven and has no local item list."""
        return []

    def load(
        self,
        query: str = "",
        year_from: int | None = None,
        year_to: int | None = None,
        num_results: int = 10,
    ) -> pd.DataFrame:
        """Load query results as a DataFrame."""
        if not query:
            return pd.DataFrame()
        result = self.client.search_scholar(
            query=query,
            year_from=year_from,
            year_to=year_to,
            num_results=num_results,
        )
        if result.error:
            raise ValueError(result.error)
        return pd.DataFrame(result.to_dict()["papers"])

