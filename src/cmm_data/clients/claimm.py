"""Client for NETL EDX CLAIMM dataset APIs."""

from __future__ import annotations

import os
from typing import Any

import httpx

from .models import DatasetInfo, DatasetResource


class CLAIMMClient:
    """Read CLAIMM datasets from NETL EDX CKAN endpoints."""

    DEFAULT_BASE_URL = "https://edx.netl.doe.gov/api/3/action"

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout: float = 30.0,
    ):
        self.base_url = (base_url or self.DEFAULT_BASE_URL).rstrip("/")
        self.api_key = api_key or os.environ.get("EDX_API_KEY")
        self.timeout = timeout

    def _headers(self) -> dict[str, str]:
        headers = {"User-Agent": "EDX-USER", "Content-Type": "application/json"}
        if self.api_key:
            headers["X-CKAN-API-Key"] = self.api_key
        return headers

    async def _request(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/{endpoint}",
                params=params,
                headers=self._headers(),
            )
            response.raise_for_status()
            payload = response.json()
            if not payload.get("success", False):
                raise ValueError(f"EDX API error: {payload.get('error', {})}")
            return payload.get("result", {})

    @staticmethod
    def _resource_to_model(resource: dict[str, Any]) -> DatasetResource:
        resource_id = str(resource.get("id", ""))
        return DatasetResource(
            id=resource_id,
            name=resource.get("name"),
            format=resource.get("format"),
            size=resource.get("size"),
            url=f"https://edx.netl.doe.gov/resource/{resource_id}/download" if resource_id else None,
        )

    @classmethod
    def _dataset_to_model(cls, pkg: dict[str, Any]) -> DatasetInfo:
        resources = [cls._resource_to_model(item) for item in pkg.get("resources", [])]
        return DatasetInfo(
            source="CLAIMM",
            id=str(pkg.get("id", "")),
            title=pkg.get("title", pkg.get("name", "")),
            description=pkg.get("notes"),
            tags=[tag.get("name", "") for tag in pkg.get("tags", [])],
            resources=resources,
        )

    async def search_datasets(
        self,
        query: str | None = None,
        tags: list[str] | None = None,
        limit: int = 20,
    ) -> list[DatasetInfo]:
        params: dict[str, Any] = {"rows": limit, "start": 0}
        params["q"] = f"claimm {query}" if query else "claimm"
        if tags:
            params["fq"] = " AND ".join(f"tags:{tag}" for tag in tags)

        result = await self._request("package_search", params=params)
        return [self._dataset_to_model(pkg) for pkg in result.get("results", [])]

    async def get_dataset(self, dataset_id: str) -> DatasetInfo | None:
        try:
            result = await self._request("package_show", params={"id": dataset_id})
        except httpx.HTTPError:
            return None
        return self._dataset_to_model(result)

    async def get_categories(self, limit: int = 200) -> dict[str, int]:
        datasets = await self.search_datasets(limit=limit)
        categories: dict[str, int] = {}
        for dataset in datasets:
            for tag in dataset.tags:
                categories[tag] = categories.get(tag, 0) + 1
        return dict(sorted(categories.items(), key=lambda item: item[1], reverse=True))
