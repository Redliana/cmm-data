"""Tests for Google Scholar client integration."""

from __future__ import annotations

from cmm_data.clients.google_scholar import GoogleScholarClient


def test_google_scholar_requires_api_key():
    client = GoogleScholarClient(api_key="")
    result = client.search_scholar("critical minerals")
    assert result.error is not None
    assert result.total_results == 0


def test_google_scholar_search_success(monkeypatch):
    class FakeSearch:
        def __init__(self, params):
            self.params = params

        def get_dict(self):
            return {
                "organic_results": [
                    {
                        "title": "Lithium supply risk analysis",
                        "publication_info": {"summary": "A Author - Journal of Minerals, 2024"},
                        "snippet": "Critical lithium supply chain trends",
                        "inline_links": {"cited_by": {"total": 12}},
                        "link": "https://example.org/paper",
                        "resources": [{"link": "https://example.org/paper.pdf"}],
                    }
                ]
            }

    monkeypatch.setattr("cmm_data.clients.google_scholar.GoogleScholarSearch", FakeSearch)
    client = GoogleScholarClient(api_key="test-key")
    result = client.search_scholar("lithium", num_results=1)

    assert result.error is None
    assert result.total_results == 1
    assert result.papers[0].title == "Lithium supply risk analysis"
    assert result.papers[0].year == "2024"
