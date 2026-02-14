"""Shared data models for external source clients."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MineralRecord:
    """Unified mineral production/trade record."""

    source: str
    commodity: str
    country: str | None = None
    country_iso2: str | None = None
    country_iso3: str | None = None
    year: int | None = None
    quantity: float | None = None
    units: str | None = None
    statistic_type: str | None = None
    notes: str | None = None


@dataclass
class DatasetResource:
    """Resource metadata for a dataset."""

    id: str
    name: str | None = None
    format: str | None = None
    size: int | None = None
    url: str | None = None


@dataclass
class DatasetInfo:
    """Dataset metadata normalized across sources."""

    source: str
    id: str
    title: str
    description: str | None = None
    tags: list[str] = field(default_factory=list)
    resources: list[DatasetResource] = field(default_factory=list)


@dataclass
class OSTIDocument:
    """OSTI document metadata."""

    osti_id: str
    title: str
    authors: list[str] = field(default_factory=list)
    publication_date: str | None = None
    description: str | None = None
    subjects: list[str] = field(default_factory=list)
    commodity_category: str | None = None
    doi: str | None = None
    product_type: str | None = None
    research_orgs: list[str] = field(default_factory=list)
    sponsor_orgs: list[str] = field(default_factory=list)


def dataclass_to_dict(instance: Any) -> dict[str, Any]:
    """Convert a dataclass instance to a plain dictionary."""
    return dict(instance.__dict__)
