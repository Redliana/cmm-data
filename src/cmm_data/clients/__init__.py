"""Shared source clients for BGS, CLAIMM, OSTI, and Google Scholar."""

from __future__ import annotations

from .bgs import BGSClient
from .claimm import CLAIMMClient
from .google_scholar import GoogleScholarClient, ScholarPaper, ScholarResult
from .models import DatasetInfo, DatasetResource, MineralRecord, OSTIDocument
from .osti import OSTIClient

__all__ = [
    "BGSClient",
    "CLAIMMClient",
    "DatasetInfo",
    "DatasetResource",
    "GoogleScholarClient",
    "MineralRecord",
    "OSTIClient",
    "OSTIDocument",
    "ScholarPaper",
    "ScholarResult",
]
