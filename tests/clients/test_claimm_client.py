"""Tests for CLAIMM client."""

from __future__ import annotations

import httpx
import pytest

from cmm_data.clients import CLAIMMClient


class _MockResponse:
    def __init__(self, payload: dict, status_code: int = 200):
        self._payload = payload
        self.status_code = status_code

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise httpx.HTTPStatusError("error", request=None, response=None)


class _MockAsyncClient:
    def __init__(self, *args, **kwargs):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def get(self, url, params=None, headers=None):
        if url.endswith("/package_search"):
            return _MockResponse(
                {
                    "success": True,
                    "result": {
                        "results": [
                            {
                                "id": "ds-1",
                                "title": "Lithium Data",
                                "tags": [{"name": "lithium"}],
                                "resources": [{"id": "res-1", "name": "table.csv", "format": "CSV"}],
                            }
                        ]
                    },
                }
            )
        if url.endswith("/package_show"):
            return _MockResponse(
                {
                    "success": True,
                    "result": {
                        "id": params["id"],
                        "title": "Dataset Detail",
                        "tags": [{"name": "rare-earth"}],
                        "resources": [{"id": "res-2", "name": "data.xlsx", "format": "XLSX"}],
                    },
                }
            )
        return _MockResponse({"success": False, "error": {"message": "unknown"}}, status_code=404)


@pytest.mark.asyncio
async def test_search_datasets(monkeypatch):
    monkeypatch.setattr("cmm_data.clients.claimm.httpx.AsyncClient", _MockAsyncClient)
    client = CLAIMMClient()
    datasets = await client.search_datasets(query="lithium", limit=5)
    assert len(datasets) == 1
    assert datasets[0].id == "ds-1"
    assert datasets[0].resources[0].url == "https://edx.netl.doe.gov/resource/res-1/download"


@pytest.mark.asyncio
async def test_get_categories(monkeypatch):
    monkeypatch.setattr("cmm_data.clients.claimm.httpx.AsyncClient", _MockAsyncClient)
    client = CLAIMMClient()
    categories = await client.get_categories(limit=5)
    assert categories.get("lithium") == 1
