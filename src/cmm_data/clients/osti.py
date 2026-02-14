"""Client for local OSTI catalog data."""

from __future__ import annotations

import json
from pathlib import Path
from typing import ClassVar

import pandas as pd

from .models import OSTIDocument


class OSTIClient:
    """Read and filter OSTI catalog metadata from local JSON."""

    COMMODITIES: ClassVar[dict[str, str]] = {
        "HREE": "Heavy Rare Earth Elements",
        "LREE": "Light Rare Earth Elements",
        "CO": "Cobalt",
        "LI": "Lithium",
        "GA": "Gallium",
        "GR": "Graphite",
        "NI": "Nickel",
        "CU": "Copper",
        "GE": "Germanium",
        "OTH": "Other Critical Materials",
    }

    def __init__(self, data_path: str | Path | None = None):
        self.data_path = Path(data_path) if data_path else None
        self._catalog: pd.DataFrame | None = None

    @property
    def catalog(self) -> pd.DataFrame:
        if self._catalog is None:
            if self.data_path is None:
                raise FileNotFoundError("OSTI data path is not configured")
            catalog_path = self.data_path / "document_catalog.json"
            if not catalog_path.exists():
                raise FileNotFoundError(f"Document catalog not found at {catalog_path}")
            with catalog_path.open(encoding="utf-8") as handle:
                data = json.load(handle)
            self._catalog = pd.DataFrame(data)
        return self._catalog

    def get_statistics(self) -> dict:
        frame = self.catalog
        stats = {"total_documents": len(frame), "commodities": {}, "product_types": {}, "year_range": {}}

        if "commodity_category" in frame.columns:
            counts = frame["commodity_category"].value_counts().to_dict()
            stats["commodities"] = {
                key: {"count": value, "name": self.COMMODITIES.get(key, key)}
                for key, value in counts.items()
            }
        if "product_type" in frame.columns:
            stats["product_types"] = frame["product_type"].value_counts().to_dict()
        if "publication_date" in frame.columns:
            years = pd.to_datetime(frame["publication_date"], errors="coerce").dt.year.dropna()
            if len(years) > 0:
                stats["year_range"] = {"min": int(years.min()), "max": int(years.max())}
        return stats

    def _to_document(self, row: pd.Series) -> OSTIDocument:
        return OSTIDocument(
            osti_id=str(row.get("osti_id", "")),
            title=row.get("title", ""),
            authors=row.get("authors", []) if isinstance(row.get("authors"), list) else [],
            publication_date=row.get("publication_date"),
            description=row.get("description"),
            subjects=row.get("subjects", []) if isinstance(row.get("subjects"), list) else [],
            commodity_category=row.get("commodity_category"),
            doi=row.get("doi"),
            product_type=row.get("product_type"),
            research_orgs=row.get("research_orgs", []) if isinstance(row.get("research_orgs"), list) else [],
            sponsor_orgs=row.get("sponsor_orgs", []) if isinstance(row.get("sponsor_orgs"), list) else [],
        )

    def search_documents(
        self,
        query: str | None = None,
        commodity: str | None = None,
        product_type: str | None = None,
        year_from: int | None = None,
        year_to: int | None = None,
        limit: int = 50,
    ) -> list[OSTIDocument]:
        frame = self.catalog.copy()
        if query:
            query_lower = query.lower()
            mask = (
                frame["title"].str.lower().str.contains(query_lower, na=False)
                | frame["description"].fillna("").str.lower().str.contains(query_lower, na=False)
                | frame["subjects"].astype(str).str.lower().str.contains(query_lower, na=False)
            )
            frame = frame[mask]
        if commodity:
            frame = frame[frame["commodity_category"] == commodity.upper()]
        if product_type:
            frame = frame[frame["product_type"].str.lower() == product_type.lower()]
        if year_from or year_to:
            years = pd.to_datetime(frame["publication_date"], errors="coerce").dt.year
            if year_from:
                frame = frame[years >= year_from]
            if year_to:
                frame = frame[years <= year_to]

        return [self._to_document(row) for _, row in frame.head(limit).iterrows()]

    def get_document(self, osti_id: str) -> OSTIDocument | None:
        frame = self.catalog
        match = frame[frame["osti_id"].astype(str) == str(osti_id)]
        if match.empty:
            return None
        return self._to_document(match.iloc[0])

    def list_commodities(self) -> dict[str, str]:
        return self.COMMODITIES.copy()

    def get_documents_by_commodity(self, commodity: str, limit: int = 100) -> list[OSTIDocument]:
        return self.search_documents(commodity=commodity, limit=limit)

    def get_recent_documents(self, limit: int = 20) -> list[OSTIDocument]:
        frame = self.catalog.copy()
        frame["_date"] = pd.to_datetime(frame["publication_date"], errors="coerce")
        frame = frame.sort_values("_date", ascending=False).head(limit)
        return [self._to_document(row) for _, row in frame.iterrows()]
