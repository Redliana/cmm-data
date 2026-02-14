"""Client for BGS World Mineral Statistics OGC API."""

from __future__ import annotations

from typing import Any

import httpx

from .models import MineralRecord


class BGSClient:
    """Read BGS production and trade data."""

    DEFAULT_BASE_URL = "https://ogcapi.bgs.ac.uk/collections/world-mineral-statistics"

    def __init__(self, base_url: str | None = None, timeout: float = 60.0):
        self.base_url = base_url or self.DEFAULT_BASE_URL
        self.timeout = timeout

    async def _request(
        self,
        params: dict[str, Any] | None = None,
        limit: int = 1000,
        offset: int = 0,
    ) -> dict[str, Any]:
        query_params = {"limit": limit, "offset": offset}
        if params:
            query_params.update(params)

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/items",
                params=query_params,
                headers={"Accept": "application/json"},
            )
            response.raise_for_status()
            return response.json()

    @staticmethod
    def _parse_records(data: dict[str, Any]) -> list[MineralRecord]:
        records: list[MineralRecord] = []
        for feature in data.get("features", []):
            props = feature.get("properties", {})
            year_raw = props.get("year")
            year = None
            if isinstance(year_raw, str) and len(year_raw) >= 4:
                try:
                    year = int(year_raw[:4])
                except ValueError:
                    year = None

            records.append(
                MineralRecord(
                    source="BGS",
                    commodity=props.get("bgs_commodity_trans", ""),
                    country=props.get("country_trans"),
                    country_iso2=props.get("country_iso2_code"),
                    country_iso3=props.get("country_iso3_code"),
                    year=year,
                    quantity=props.get("quantity"),
                    units=props.get("units"),
                    statistic_type=props.get("bgs_statistic_type_trans"),
                    notes=props.get("concat_table_notes_text"),
                )
            )
        return records

    async def search_production(
        self,
        commodity: str | None = None,
        country: str | None = None,
        country_iso: str | None = None,
        year_from: int | None = None,
        year_to: int | None = None,
        statistic_type: str = "Production",
        limit: int = 1000,
    ) -> list[MineralRecord]:
        params: dict[str, Any] = {"bgs_statistic_type_trans": statistic_type}
        if commodity:
            params["bgs_commodity_trans"] = commodity
        if country:
            params["country_trans"] = country
        if country_iso:
            if len(country_iso) == 2:
                params["country_iso2_code"] = country_iso.upper()
            else:
                params["country_iso3_code"] = country_iso.upper()

        all_records: list[MineralRecord] = []
        offset = 0

        while len(all_records) < limit:
            fetch_limit = min(1000, limit - len(all_records))
            data = await self._request(params=params, limit=fetch_limit, offset=offset)
            records = self._parse_records(data)
            if not records:
                break

            for record in records:
                if year_from and record.year and record.year < year_from:
                    continue
                if year_to and record.year and record.year > year_to:
                    continue
                all_records.append(record)
                if len(all_records) >= limit:
                    break

            if len(records) < fetch_limit:
                break
            offset += fetch_limit

        all_records.sort(key=lambda r: r.year or 0, reverse=True)
        return all_records[:limit]

    async def get_commodities(self, limit_pages: int = 4) -> list[str]:
        commodities: set[str] = set()
        for i in range(limit_pages):
            data = await self._request(limit=5000, offset=i * 5000)
            features = data.get("features", [])
            if not features:
                break
            for feature in features:
                commodity = feature.get("properties", {}).get("bgs_commodity_trans")
                if commodity:
                    commodities.add(commodity)
        return sorted(commodities)

    async def get_ranking(
        self,
        commodity: str,
        year: int | None = None,
        top_n: int = 15,
    ) -> list[dict[str, Any]]:
        records = await self.search_production(commodity=commodity, limit=5000)
        if not records:
            return []

        target_year = year
        if target_year is None:
            valid_years = [r.year for r in records if r.year is not None]
            if not valid_years:
                return []
            target_year = max(valid_years)

        totals: dict[str, dict[str, Any]] = {}
        for record in records:
            if record.year != target_year or record.quantity is None:
                continue
            key = record.country or "Unknown"
            if key not in totals:
                totals[key] = {
                    "country": key,
                    "country_iso": record.country_iso3,
                    "year": target_year,
                    "quantity": 0.0,
                    "units": record.units,
                }
            totals[key]["quantity"] += float(record.quantity)

        ranked = sorted(totals.values(), key=lambda r: r["quantity"], reverse=True)
        total_quantity = sum(item["quantity"] for item in ranked)
        for idx, item in enumerate(ranked[:top_n], 1):
            item["rank"] = idx
            item["share_percent"] = round(
                (item["quantity"] / total_quantity * 100.0) if total_quantity else 0.0,
                2,
            )
        return ranked[:top_n]
