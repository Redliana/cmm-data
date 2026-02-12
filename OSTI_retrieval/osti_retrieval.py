#!/usr/bin/env python3
"""
OSTI.gov Automated Document Retrieval for CMM Supply Chain Training Data

.. deprecated::
    This is a duplicate copy. The canonical version is at:
        Globus_Sharing/OSTI_retrieval/osti_retrieval.py

    For MCP-based OSTI access, use the OSTI MCP Server:
        Data_Needs/OSTI_MCP/

    This copy is kept for reference only and may be removed in a future cleanup.

Based on the CMM LLM Baseline Gold Q&A Methodology Framework.
Retrieves DOE technical reports and journal preprints for critical minerals.
"""

from __future__ import annotations

import warnings

warnings.warn(
    "This is a duplicate copy of osti_retrieval.py. "
    "The canonical version is at Globus_Sharing/OSTI_retrieval/osti_retrieval.py. "
    "For MCP-based access, use the OSTI MCP Server (Data_Needs/OSTI_MCP/).",
    DeprecationWarning,
    stacklevel=2,
)

import json
import time
from datetime import datetime
from pathlib import Path

import requests

# Configuration
BASE_URL = "https://www.osti.gov/api/v1/records"
OUTPUT_DIR = Path(
    "/Users/wash198/Documents/Projects/Science_Projects/MPII_CMM/LLM_Fine_Tuning/Claude/OSTI_retrieval"
)
PDF_DIR = OUTPUT_DIR / "pdfs"
METADATA_DIR = OUTPUT_DIR / "metadata"

# Rate limiting (be respectful to OSTI servers)
REQUEST_DELAY = 1.0  # seconds between requests
MAX_RESULTS_PER_QUERY = 100  # OSTI default max is typically 1000

# Search queries based on CMM methodology commodity priorities
COMMODITY_SEARCHES = {
    "HREE": {
        "weight": 0.15,
        "queries": [
            "dysprosium separation",
            "terbium extraction",
            "heavy rare earth processing",
            "rare earth solvent extraction",
            "lanthanide separation chemistry",
        ],
    },
    "LREE": {
        "weight": 0.10,
        "queries": [
            "neodymium magnet",
            "praseodymium processing",
            "light rare earth",
            "NdFeB permanent magnet",
            "rare earth oxide production",
        ],
    },
    "CO": {
        "weight": 0.12,
        "queries": [
            "cobalt extraction",
            "cobalt refining",
            "cobalt supply chain",
            "battery cathode cobalt",
            "cobalt hydrometallurgy",
        ],
    },
    "LI": {
        "weight": 0.12,
        "queries": [
            "lithium extraction",
            "lithium brine processing",
            "lithium supply chain",
            "lithium-ion battery materials",
            "direct lithium extraction",
            "spodumene processing",
        ],
    },
    "GA": {
        "weight": 0.10,
        "queries": [
            "gallium production",
            "gallium arsenide",
            "gallium extraction byproduct",
            "III-V semiconductor materials",
            "gallium nitride",
        ],
    },
    "GR": {
        "weight": 0.10,
        "queries": [
            "graphite anode",
            "spherical graphite processing",
            "natural graphite battery",
            "graphite purification",
            "synthetic graphite production",
        ],
    },
    "NI": {
        "weight": 0.08,
        "queries": [
            "nickel sulfate battery",
            "Class 1 nickel",
            "nickel laterite processing",
            "high-purity nickel refining",
            "nickel cobalt manganese cathode",
        ],
    },
    "CU": {
        "weight": 0.08,
        "queries": [
            "copper electrolytic refining",
            "copper smelting",
            "copper supply chain",
            "copper solvent extraction",
            "copper concentrate processing",
        ],
    },
    "GE": {
        "weight": 0.05,
        "queries": [
            "germanium production",
            "germanium extraction",
            "germanium semiconductor",
            "infrared optics germanium",
            "germanium refining",
        ],
    },
    "OTH": {
        "weight": 0.10,
        "queries": [
            "manganese electrolytic",
            "titanium sponge production",
            "platinum group metals processing",
            "tungsten extraction",
            "critical minerals supply chain",
            "strategic minerals processing",
        ],
    },
}

# Cross-cutting technical queries (sub-domain coverage)
SUBDOMAIN_QUERIES = {
    "T-EC": [  # Extraction Chemistry
        "solvent extraction critical minerals",
        "ion exchange rare earth",
        "hydrometallurgical extraction",
        "leaching process minerals",
    ],
    "T-PM": [  # Processing Metallurgy
        "pyrometallurgical processing",
        "electrorefining metals",
        "mineral beneficiation",
        "ore concentrate processing",
    ],
    "T-GO": [  # Geological Occurrence
        "critical mineral deposits",
        "rare earth ore geology",
        "mineral resource assessment",
        "ore grade characterization",
    ],
    "S-ST": [  # Supply Chain Topology
        "critical minerals supply chain",
        "mineral processing chokepoint",
        "strategic materials vulnerability",
        "domestic mineral production",
    ],
    "G-PR": [  # Policy/Regulatory
        "critical minerals policy",
        "strategic mineral stockpile",
        "mineral export controls",
        "domestic sourcing critical materials",
    ],
}


class OSTIRetriever:
    """Automated retrieval of documents from OSTI.gov API."""

    def __init__(self, output_dir: Path = OUTPUT_DIR):
        self.output_dir = output_dir
        self.pdf_dir = output_dir / "pdfs"
        self.metadata_dir = output_dir / "metadata"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "User-Agent": "CMM-Research-Bot/1.0 (PNNL Critical Materials Research)",
            }
        )

        # Create directories
        self.pdf_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_dir.mkdir(parents=True, exist_ok=True)

        # Track downloaded documents
        self.downloaded_ids = self._load_downloaded_ids()
        self.stats = {
            "queries_executed": 0,
            "records_found": 0,
            "pdfs_downloaded": 0,
            "pdfs_skipped": 0,
            "errors": 0,
        }

    def _load_downloaded_ids(self) -> set:
        """Load set of already downloaded OSTI IDs."""
        ids = set()
        tracking_file = self.output_dir / "downloaded_ids.txt"
        if tracking_file.exists():
            with open(tracking_file) as f:
                ids = {line.strip() for line in f if line.strip()}
        return ids

    def _save_downloaded_id(self, osti_id: str):
        """Save newly downloaded OSTI ID to tracking file."""
        self.downloaded_ids.add(osti_id)
        with open(self.output_dir / "downloaded_ids.txt", "a") as f:
            f.write(f"{osti_id}\n")

    def search(
        self, query: str, max_results: int = MAX_RESULTS_PER_QUERY, has_fulltext: bool = True
    ) -> list[dict]:
        """Search OSTI for documents matching query."""
        all_records = []
        page = 1
        rows_per_page = min(100, max_results)  # OSTI typically limits to 100/page

        while len(all_records) < max_results:
            params = {
                "q": query,
                "has_fulltext": str(has_fulltext).lower(),
                "rows": rows_per_page,
                "page": page,
            }

            try:
                response = self.session.get(BASE_URL, params=params)
                response.raise_for_status()
                records = response.json()

                if not records:
                    break

                all_records.extend(records)
                self.stats["queries_executed"] += 1

                # Check if we got fewer records than requested (last page)
                if len(records) < rows_per_page:
                    break

                page += 1
                time.sleep(REQUEST_DELAY)

            except requests.RequestException as e:
                print(f"  Error searching for '{query}': {e}")
                self.stats["errors"] += 1
                break

        self.stats["records_found"] += len(all_records)
        return all_records[:max_results]

    def download_pdf(self, record: dict, commodity: str = "unknown") -> Path | None:
        """Download PDF for a record if available."""
        osti_id = record.get("osti_id")

        if not osti_id:
            return None

        if osti_id in self.downloaded_ids:
            self.stats["pdfs_skipped"] += 1
            return None

        # Find fulltext link
        fulltext_url = None
        for link in record.get("links", []):
            if link.get("rel") == "fulltext":
                fulltext_url = link.get("href")
                break

        if not fulltext_url:
            return None

        # Create commodity subdirectory
        commodity_dir = self.pdf_dir / commodity
        commodity_dir.mkdir(exist_ok=True)

        # Generate safe filename
        title = record.get("title", "unknown")[:80]
        safe_title = "".join(c if c.isalnum() or c in " -_" else "_" for c in title)
        filename = f"{osti_id}_{safe_title}.pdf"
        filepath = commodity_dir / filename

        try:
            response = self.session.get(fulltext_url, stream=True, timeout=60)
            response.raise_for_status()

            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            self._save_downloaded_id(osti_id)
            self.stats["pdfs_downloaded"] += 1

            # Save metadata alongside
            meta_file = commodity_dir / f"{osti_id}_metadata.json"
            with open(meta_file, "w") as f:
                json.dump(record, f, indent=2)

            time.sleep(REQUEST_DELAY)
            return filepath

        except requests.RequestException as e:
            print(f"  Error downloading PDF for {osti_id}: {e}")
            self.stats["errors"] += 1
            return None

    def retrieve_commodity(self, commodity_code: str, max_per_query: int = 50):
        """Retrieve documents for a specific commodity."""
        if commodity_code not in COMMODITY_SEARCHES:
            print(f"Unknown commodity code: {commodity_code}")
            return

        config = COMMODITY_SEARCHES[commodity_code]
        queries = config["queries"]

        print(f"\n{'=' * 60}")
        print(f"Retrieving documents for {commodity_code} (weight: {config['weight'] * 100:.0f}%)")
        print(f"{'=' * 60}")

        all_records = []
        seen_ids = set()

        for query in queries:
            print(f"\n  Searching: '{query}'")
            records = self.search(query, max_results=max_per_query)

            # Deduplicate
            new_records = [r for r in records if r.get("osti_id") not in seen_ids]
            for r in new_records:
                seen_ids.add(r.get("osti_id"))

            print(f"    Found {len(records)} records ({len(new_records)} new)")
            all_records.extend(new_records)

        print(f"\n  Total unique records for {commodity_code}: {len(all_records)}")

        # Download PDFs
        downloaded = 0
        for i, record in enumerate(all_records):
            if i % 10 == 0:
                print(f"    Downloading {i + 1}/{len(all_records)}...")

            result = self.download_pdf(record, commodity_code)
            if result:
                downloaded += 1

        print(f"  Downloaded {downloaded} new PDFs for {commodity_code}")
        return all_records

    def retrieve_subdomain(self, subdomain_code: str, max_per_query: int = 30):
        """Retrieve documents for a specific subdomain."""
        if subdomain_code not in SUBDOMAIN_QUERIES:
            print(f"Unknown subdomain code: {subdomain_code}")
            return

        queries = SUBDOMAIN_QUERIES[subdomain_code]

        print(f"\n{'=' * 60}")
        print(f"Retrieving documents for subdomain: {subdomain_code}")
        print(f"{'=' * 60}")

        all_records = []
        seen_ids = set()

        for query in queries:
            print(f"\n  Searching: '{query}'")
            records = self.search(query, max_results=max_per_query)

            new_records = [r for r in records if r.get("osti_id") not in seen_ids]
            for r in new_records:
                seen_ids.add(r.get("osti_id"))

            print(f"    Found {len(records)} records ({len(new_records)} new)")
            all_records.extend(new_records)

        print(f"\n  Total unique records for {subdomain_code}: {len(all_records)}")

        # Download to subdomain directory
        downloaded = 0
        for i, record in enumerate(all_records):
            if i % 10 == 0:
                print(f"    Downloading {i + 1}/{len(all_records)}...")

            result = self.download_pdf(record, f"subdomain_{subdomain_code}")
            if result:
                downloaded += 1

        print(f"  Downloaded {downloaded} new PDFs for {subdomain_code}")
        return all_records

    def retrieve_all(self, max_per_query: int = 50):
        """Retrieve documents for all commodities and subdomains."""
        print("\n" + "=" * 70)
        print("OSTI Document Retrieval for CMM Supply Chain Training Data")
        print(f"Started: {datetime.now().isoformat()}")
        print("=" * 70)

        # Commodities
        for commodity in COMMODITY_SEARCHES:
            self.retrieve_commodity(commodity, max_per_query)

        # Subdomains
        for subdomain in SUBDOMAIN_QUERIES:
            self.retrieve_subdomain(subdomain, max_per_query)

        # Print summary
        print("\n" + "=" * 70)
        print("RETRIEVAL SUMMARY")
        print("=" * 70)
        print(f"Queries executed: {self.stats['queries_executed']}")
        print(f"Total records found: {self.stats['records_found']}")
        print(f"PDFs downloaded: {self.stats['pdfs_downloaded']}")
        print(f"PDFs skipped (already downloaded): {self.stats['pdfs_skipped']}")
        print(f"Errors: {self.stats['errors']}")
        print(f"Completed: {datetime.now().isoformat()}")

        # Save stats
        stats_file = self.output_dir / "retrieval_stats.json"
        with open(stats_file, "w") as f:
            json.dump(
                {
                    **self.stats,
                    "timestamp": datetime.now().isoformat(),
                    "total_downloaded_ids": len(self.downloaded_ids),
                },
                f,
                indent=2,
            )

        return self.stats

    def export_metadata_catalog(self):
        """Export a catalog of all downloaded document metadata."""
        catalog = []

        for commodity_dir in self.pdf_dir.iterdir():
            if commodity_dir.is_dir():
                for meta_file in commodity_dir.glob("*_metadata.json"):
                    with open(meta_file) as f:
                        record = json.load(f)
                        catalog.append(
                            {
                                "osti_id": record.get("osti_id"),
                                "title": record.get("title"),
                                "authors": record.get("authors", []),
                                "publication_date": record.get("publication_date"),
                                "description": record.get("description", "")[:500],
                                "subjects": record.get("subjects", []),
                                "commodity_category": commodity_dir.name,
                                "doi": record.get("doi"),
                                "product_type": record.get("product_type"),
                                "research_orgs": record.get("research_orgs", []),
                                "sponsor_orgs": record.get("sponsor_orgs", []),
                            }
                        )

        # Save catalog
        catalog_file = self.output_dir / "document_catalog.json"
        with open(catalog_file, "w") as f:
            json.dump(catalog, f, indent=2)

        print(f"\nExported catalog with {len(catalog)} documents to {catalog_file}")
        return catalog


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="OSTI Document Retrieval for CMM Research")
    parser.add_argument(
        "--commodity", "-c", help="Retrieve for specific commodity (e.g., HREE, LI, CO)"
    )
    parser.add_argument(
        "--subdomain", "-s", help="Retrieve for specific subdomain (e.g., T-EC, S-ST)"
    )
    parser.add_argument(
        "--all", "-a", action="store_true", help="Retrieve all commodities and subdomains"
    )
    parser.add_argument("--max-per-query", "-m", type=int, default=50, help="Max results per query")
    parser.add_argument("--catalog", action="store_true", help="Export metadata catalog only")

    args = parser.parse_args()

    retriever = OSTIRetriever()

    if args.catalog:
        retriever.export_metadata_catalog()
    elif args.commodity:
        retriever.retrieve_commodity(args.commodity.upper(), args.max_per_query)
        retriever.export_metadata_catalog()
    elif args.subdomain:
        retriever.retrieve_subdomain(args.subdomain.upper(), args.max_per_query)
        retriever.export_metadata_catalog()
    elif args.all:
        retriever.retrieve_all(args.max_per_query)
        retriever.export_metadata_catalog()
    else:
        # Default: retrieve all
        print("No specific target specified. Use --help for options.")
        print("Running full retrieval...")
        retriever.retrieve_all(args.max_per_query)
        retriever.export_metadata_catalog()


if __name__ == "__main__":
    main()
