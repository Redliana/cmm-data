"""Tests for OSTI client."""

from __future__ import annotations

import json

from cmm_data.clients import OSTIClient


def _write_catalog(tmp_path):
    catalog = [
        {
            "osti_id": "1",
            "title": "Lithium extraction advances",
            "authors": ["A. Author"],
            "publication_date": "2024-01-10",
            "description": "Extraction and processing methods",
            "subjects": ["lithium", "processing"],
            "commodity_category": "LI",
            "product_type": "Technical Report",
        },
        {
            "osti_id": "2",
            "title": "Rare earth separation",
            "authors": ["B. Author"],
            "publication_date": "2022-07-01",
            "description": "Separation chemistry",
            "subjects": ["rare earth"],
            "commodity_category": "HREE",
            "product_type": "Journal Article",
        },
    ]
    path = tmp_path / "document_catalog.json"
    with path.open("w", encoding="utf-8") as handle:
        json.dump(catalog, handle)
    return tmp_path


def test_search_documents(tmp_path):
    data_path = _write_catalog(tmp_path)
    client = OSTIClient(data_path=data_path)

    results = client.search_documents(query="lithium", year_from=2023)
    assert len(results) == 1
    assert results[0].osti_id == "1"


def test_get_recent_documents(tmp_path):
    data_path = _write_catalog(tmp_path)
    client = OSTIClient(data_path=data_path)

    recent = client.get_recent_documents(limit=1)
    assert len(recent) == 1
    assert recent[0].osti_id == "1"
