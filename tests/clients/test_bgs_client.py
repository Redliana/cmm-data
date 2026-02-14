"""Tests for BGS client."""

from __future__ import annotations

import httpx
import pytest

from cmm_data.clients import BGSClient


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
        self._payload = kwargs.pop("_payload")

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def get(self, url, params=None, headers=None):
        return _MockResponse(self._payload)


@pytest.mark.asyncio
async def test_search_production(monkeypatch):
    payload = {
        "features": [
            {
                "properties": {
                    "bgs_commodity_trans": "lithium minerals",
                    "country_trans": "Chile",
                    "country_iso2_code": "CL",
                    "country_iso3_code": "CHL",
                    "year": "2023",
                    "quantity": 100.0,
                    "units": "t",
                    "bgs_statistic_type_trans": "Production",
                }
            },
            {
                "properties": {
                    "bgs_commodity_trans": "lithium minerals",
                    "country_trans": "Chile",
                    "country_iso2_code": "CL",
                    "country_iso3_code": "CHL",
                    "year": "2021",
                    "quantity": 50.0,
                    "units": "t",
                    "bgs_statistic_type_trans": "Production",
                }
            },
        ]
    }

    monkeypatch.setattr(
        "cmm_data.clients.bgs.httpx.AsyncClient",
        lambda *a, **k: _MockAsyncClient(*a, _payload=payload, **k),
    )

    client = BGSClient()
    records = await client.search_production(commodity="lithium minerals", year_from=2022)
    assert len(records) == 1
    assert records[0].country == "Chile"
    assert records[0].year == 2023


@pytest.mark.asyncio
async def test_get_ranking(monkeypatch):
    payload = {
        "features": [
            {
                "properties": {
                    "bgs_commodity_trans": "cobalt, mine",
                    "country_trans": "A",
                    "country_iso3_code": "AAA",
                    "year": "2022",
                    "quantity": 40.0,
                    "units": "t",
                    "bgs_statistic_type_trans": "Production",
                }
            },
            {
                "properties": {
                    "bgs_commodity_trans": "cobalt, mine",
                    "country_trans": "B",
                    "country_iso3_code": "BBB",
                    "year": "2022",
                    "quantity": 60.0,
                    "units": "t",
                    "bgs_statistic_type_trans": "Production",
                }
            },
        ]
    }
    monkeypatch.setattr(
        "cmm_data.clients.bgs.httpx.AsyncClient",
        lambda *a, **k: _MockAsyncClient(*a, _payload=payload, **k),
    )

    client = BGSClient()
    ranking = await client.get_ranking("cobalt, mine", year=2022, top_n=2)
    assert len(ranking) == 2
    assert ranking[0]["country"] == "B"
    assert ranking[0]["share_percent"] == 60.0
