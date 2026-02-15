"""Client for Google Scholar search via SerpAPI."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv
from serpapi import GoogleScholarSearch

# Load .env from current working directory when available.
load_dotenv()


@dataclass
class ScholarPaper:
    """A single Google Scholar search result."""

    title: str
    authors: str
    venue: str
    year: str
    snippet: str
    citations: int
    url: str
    pdf_url: str = ""


@dataclass
class ScholarResult:
    """Result set for a Google Scholar query."""

    query: str
    total_results: int
    papers: list[ScholarPaper] = field(default_factory=list)
    error: str | None = None

    def to_dict(self) -> dict:
        """Serialize the result to a JSON-safe dictionary."""
        return {
            "query": self.query,
            "total_results": self.total_results,
            "papers": [
                {
                    "title": p.title,
                    "authors": p.authors,
                    "venue": p.venue,
                    "year": p.year,
                    "snippet": p.snippet,
                    "citations": p.citations,
                    "url": p.url,
                    "pdf_url": p.pdf_url,
                }
                for p in self.papers
            ],
            "error": self.error,
        }


class GoogleScholarClient:
    """Thin client for Google Scholar search using SerpAPI."""

    def __init__(self, api_key: str | None = None, env_file: str | Path | None = None):
        if env_file:
            load_dotenv(Path(env_file))
        self.api_key = api_key or os.environ.get("SERPAPI_KEY", "")

    def set_api_key(self, api_key: str) -> None:
        """Set SerpAPI key for subsequent calls."""
        self.api_key = api_key

    def _require_api_key(self) -> str:
        if not self.api_key:
            raise ValueError(
                "SerpAPI key not set. Set SERPAPI_KEY or pass api_key to GoogleScholarClient."
            )
        return self.api_key

    @staticmethod
    def _parse_venue_year(summary: str) -> tuple[str, str]:
        venue = "Unknown"
        year = "Unknown"
        if summary:
            parts = summary.split(" - ")
            if len(parts) > 1:
                venue_year = parts[-1]
                year_match = re.search(r"\b(19|20)\d{2}\b", venue_year)
                if year_match:
                    year = year_match.group()
                venue = (
                    venue_year.rsplit(",", 1)[0].strip() if "," in venue_year else venue_year.strip()
                )
        return venue, year

    def search_scholar(
        self,
        query: str,
        year_from: int | None = None,
        year_to: int | None = None,
        num_results: int = 10,
    ) -> ScholarResult:
        """Search Google Scholar and return normalized results."""
        try:
            api_key = self._require_api_key()
            num_results = max(1, min(num_results, 20))

            params: dict[str, str | int] = {
                "engine": "google_scholar",
                "q": query,
                "api_key": api_key,
                "num": num_results,
            }
            if year_from:
                params["as_ylo"] = year_from
            if year_to:
                params["as_yhi"] = year_to

            search = GoogleScholarSearch(params)
            results = search.get_dict()

            if "error" in results:
                return ScholarResult(query=query, total_results=0, error=results["error"])

            papers: list[ScholarPaper] = []
            for result in results.get("organic_results", [])[:num_results]:
                pub_info = result.get("publication_info", {})
                summary = pub_info.get("summary", "")
                venue, year = self._parse_venue_year(summary)
                papers.append(
                    ScholarPaper(
                        title=result.get("title", "Unknown"),
                        authors=summary.split(" - ")[0] if " - " in summary else summary,
                        venue=venue,
                        year=year,
                        snippet=result.get("snippet", ""),
                        citations=result.get("inline_links", {}).get("cited_by", {}).get("total", 0),
                        url=result.get("link", ""),
                        pdf_url=result.get("resources", [{}])[0].get("link", "")
                        if result.get("resources")
                        else "",
                    )
                )

            return ScholarResult(query=query, total_results=len(papers), papers=papers)
        except Exception as exc:
            return ScholarResult(query=query, total_results=0, error=str(exc))
