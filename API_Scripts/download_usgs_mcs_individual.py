"""
USGS Mineral Commodity Summaries Individual Commodity Download Script

For pre-2023 years, USGS MCS data is organized as individual commodity items.
This script downloads only CMM-relevant commodities from those releases.

Based on methodology: CMM_LLM_Baseline_Gold_QA_Methodology.md
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import requests

# CMM Commodities from methodology (Section 2.2)
# Priority commodities for CMM supply chain modeling
CMM_COMMODITIES = {
    # Priority 1-2: Heavy REE, Cobalt
    "RARE EARTHS": ["Heavy REE", "Light REE"],  # Covers both heavy and light REE
    "COBALT": ["Cobalt"],
    # Priority 3-5: Lithium, Gallium, Graphite
    "LITHIUM": ["Lithium"],
    "GALLIUM": ["Gallium"],
    "GRAPHITE": ["Graphite"],
    # Priority 6-9: Light REE (covered by RARE EARTHS), Nickel, Copper, Germanium
    "NICKEL": ["Nickel"],
    "COPPER": ["Copper"],
    "GERMANIUM": ["Germanium"],
    # Priority 10: Other (Mn, Ti, PGM, W)
    "MANGANESE": ["Manganese"],
    "TITANIUM": ["Titanium"],
    "PLATINUM": ["Platinum Group Metals"],
    "PALLADIUM": ["Platinum Group Metals"],
    "TUNGSTEN": ["Tungsten"],
}

# USGS commodity name variations (for matching)
USGS_COMMODITY_VARIANTS = {
    "RARE EARTHS": ["RARE EARTH", "RARE EARTHS", "REE", "RARE EARTH ELEMENTS"],
    "COBALT": ["COBALT"],
    "LITHIUM": ["LITHIUM"],
    "GALLIUM": ["GALLIUM"],
    "GRAPHITE": ["GRAPHITE"],
    "NICKEL": ["NICKEL"],
    "COPPER": ["COPPER"],
    "GERMANIUM": ["GERMANIUM"],
    "MANGANESE": ["MANGANESE", "MANGAN"],
    "TITANIUM": ["TITANIUM", "TITAN"],
    "PLATINUM": ["PLATINUM"],
    "PALLADIUM": ["PALLADIUM"],
    "TUNGSTEN": ["TUNGSTEN", "TUNGS"],
}


class USGSMCSIndividualDownloader:
    """Download individual commodity data from pre-2023 USGS MCS releases."""

    def __init__(self, output_dir: str = "usgs_mcs_data"):
        """
        Initialize downloader.

        Args:
            output_dir: Directory to save downloaded data
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": "Mozilla/5.0 (compatible; CMM-Data-Collector/1.0)"}
        )

    def get_catalog_item(self, item_id: str) -> dict:
        """Get catalog item information."""
        url = f"https://www.sciencebase.gov/catalog/item/{item_id}?format=json"
        try:
            response = self.session.get(url, timeout=30)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException as e:
            print(f"Error fetching item {item_id}: {e}")
        return {}

    def get_child_items(self, parent_id: str) -> list[dict]:
        """Get child items from a parent catalog item."""
        # Try multiple endpoints
        urls = [
            f"https://www.sciencebase.gov/catalog/item/{parent_id}/children?format=json",
            f"https://www.sciencebase.gov/catalog/items/{parent_id}/children?format=json",
        ]

        for url in urls:
            try:
                response = self.session.get(url, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list):
                        return data
                    elif isinstance(data, dict) and "items" in data:
                        return data["items"]
            except requests.RequestException:
                continue

        # Alternative: Try to parse HTML page for child item links
        try:
            import re

            html_url = f"https://www.sciencebase.gov/catalog/item/{parent_id}"
            response = self.session.get(html_url, timeout=30)
            if response.status_code == 200:
                html = response.text
                # Look for child item links in the HTML
                # ScienceBase often has links like: href="/catalog/item/{id}"
                item_ids = re.findall(r"/catalog/item/([a-f0-9]{24})", html)
                # Get info for each found ID (limit to reasonable number)
                children = []
                unique_ids = list(set(item_ids))
                print(f"  Found {len(unique_ids)} potential item IDs in HTML, checking...")
                for item_id in unique_ids[:200]:  # Increased limit to get all commodities
                    item_info = self.get_catalog_item(item_id)
                    if item_info and item_info.get("title"):
                        # Only include items that look like commodity data releases
                        title = item_info.get("title", "").upper()
                        if "DATA RELEASE" in title or "MINERAL COMMODITY" in title:
                            children.append(item_info)
                    time.sleep(0.1)  # Small delay to avoid rate limiting
                if children:
                    print(f"  Retrieved {len(children)} child items from HTML parsing")
                    return children
        except (requests.RequestException, ValueError) as e:
            print(f"  HTML parsing error: {e}")
            pass

        return []

    def find_cmm_commodity_items(
        self, parent_id: str, year: int | None = None
    ) -> dict[str, list[dict]]:
        """
        Find CMM-relevant commodity items from a parent catalog.

        Args:
            parent_id: ScienceBase catalog item ID for the year's data release
            year: Year (optional, for better matching)

        Returns:
            Dictionary mapping CMM categories to catalog items
        """
        print(f"\nSearching for CMM commodities in catalog {parent_id}...")
        print("=" * 80)

        # Get child items
        children = self.get_child_items(parent_id)
        print(f"Found {len(children)} child items")

        # Map commodities to items
        cmm_items = {}

        for child in children:
            title = child.get("title", "").upper()
            item_id = child.get("id")

            # Skip non-commodity items
            if not title or "DATA RELEASE" not in title:
                continue

            # Extract commodity name from title
            # Format: "Mineral Commodity Summaries 2022 - LITHIUM Data Release"
            # or "Mineral Commodity Summaries 2022 - RARE EARTHS Data Release"
            if " - " in title:
                commodity_part = title.split(" - ")[1].replace(" DATA RELEASE", "").strip()
            else:
                commodity_part = title

            # Check if this item matches any CMM commodity
            for usgs_commodity, cmm_categories in CMM_COMMODITIES.items():
                variants = USGS_COMMODITY_VARIANTS.get(usgs_commodity, [usgs_commodity])

                for variant in variants:
                    variant_upper = variant.upper()
                    # Match if variant appears in commodity part or full title
                    if variant_upper in commodity_part or variant_upper in title:
                        # Found a match
                        for cmm_cat in cmm_categories:
                            if cmm_cat not in cmm_items:
                                cmm_items[cmm_cat] = []
                            cmm_items[cmm_cat].append(
                                {
                                    "id": item_id,
                                    "title": child.get("title"),
                                    "usgs_commodity": usgs_commodity,
                                }
                            )
                        print(f"  ✓ {usgs_commodity}: {child.get('title')} (ID: {item_id})")
                        break

        print(
            f"\nFound {len(cmm_items)} CMM categories with {sum(len(v) for v in cmm_items.values())} items"
        )
        return cmm_items

    def download_commodity_item(self, item_id: str, commodity_name: str, year: int) -> list[Path]:
        """
        Download files from an individual commodity catalog item.

        Args:
            item_id: ScienceBase catalog item ID
            commodity_name: Name of the commodity
            year: Year of the data

        Returns:
            list of downloaded file paths
        """
        item_info = self.get_catalog_item(item_id)
        if not item_info:
            return []

        year_dir = self.output_dir / str(year) / "individual_commodities"
        year_dir.mkdir(parents=True, exist_ok=True)

        downloaded_files = []

        # Get attached files
        if "files" in item_info:
            for file_info in item_info["files"]:
                url = (
                    file_info.get("url")
                    or file_info.get("downloadUri")
                    or file_info.get("downloadURL")
                )
                if not url:
                    # Try constructing URL
                    filename = file_info.get("name", "")
                    url = f"https://www.sciencebase.gov/catalog/file/get/{item_id}?name={filename}"

                filename = file_info.get("name", url.split("/")[-1].split("?")[0])

                # Only download CSV files
                if filename.endswith(".csv"):
                    filepath = year_dir / f"{commodity_name.lower().replace(' ', '_')}_{filename}"

                    try:
                        print(f"    Downloading: {filename}")
                        response = self.session.get(url, stream=True, timeout=60)
                        response.raise_for_status()

                        with open(filepath, "wb") as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                f.write(chunk)

                        downloaded_files.append(filepath)
                        print(f"      ✓ Downloaded {filepath.stat().st_size / 1024:.1f} KB")
                        time.sleep(0.5)  # Rate limiting
                    except (requests.RequestException, OSError) as e:
                        print(f"      ✗ Error: {e}")

        return downloaded_files

    def download_year_individual_commodities(self, year: int, parent_id: str) -> dict:
        """
        Download CMM commodities for a year using individual commodity items.

        Args:
            year: Year to download
            parent_id: ScienceBase catalog item ID for the year's data release

        Returns:
            Summary of downloads
        """
        print(f"\n{'=' * 80}")
        print(f"Downloading USGS MCS {year} Data (Individual Commodities)")
        print(f"{'=' * 80}\n")

        # Find CMM commodity items
        cmm_items = self.find_cmm_commodity_items(parent_id, year=year)

        if not cmm_items:
            print("  ⚠ No CMM commodities found in this catalog")
            return {"year": year, "status": "no_commodities_found"}

        # Download each commodity
        summary = {
            "year": year,
            "commodities_downloaded": {},
            "total_files": 0,
            "status": "incomplete",
        }

        for cmm_category, items in cmm_items.items():
            print(f"\n{cmm_category}:")
            category_files = []

            for item in items:
                files = self.download_commodity_item(item["id"], item["usgs_commodity"], year)
                category_files.extend(files)

            if category_files:
                summary["commodities_downloaded"][cmm_category] = {
                    "items": len(items),
                    "files": len(category_files),
                    "filepaths": [str(f) for f in category_files],
                }
                summary["total_files"] += len(category_files)
                print(f"  ✓ Downloaded {len(category_files)} files")

        summary["status"] = "complete" if summary["total_files"] > 0 else "failed"

        return summary


def main():
    """Main function for command-line interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Download USGS MCS individual commodity data for pre-2023 years",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download 2022 data from parent catalog
  python download_usgs_mcs_individual.py --year 2022 --parent-id 5c8c03e4e4b0938824529f7d

  # Download with specific data release ID (if known)
  python download_usgs_mcs_individual.py --year 2022 --release-id <ITEM_ID>
        """,
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="usgs_mcs_data",
        help="Output directory for downloaded data",
    )

    parser.add_argument("--year", type=int, required=True, help="Year to download (2020-2022)")

    parser.add_argument(
        "--parent-id", type=str, help="ScienceBase parent catalog item ID (e.g., NMIC catalog)"
    )

    parser.add_argument(
        "--release-id",
        type=str,
        help="ScienceBase catalog item ID for the specific year data release",
    )

    args = parser.parse_args()

    downloader = USGSMCSIndividualDownloader(output_dir=args.output_dir)

    # Determine which catalog item to use
    if args.release_id:
        # Use the specific release ID directly
        catalog_id = args.release_id
    elif args.parent_id:
        # Search for the year's release in the parent catalog
        children = downloader.get_child_items(args.parent_id)
        catalog_id = None

        for child in children:
            title = child.get("title", "").upper()
            if str(args.year) in title and (
                "MINERAL COMMODITY SUMMARIES" in title or "MCS" in title
            ):
                catalog_id = child.get("id")
                print(f"Found {args.year} MCS release: {child.get('title')}")
                print(f"Using catalog ID: {catalog_id}")
                break

        if not catalog_id:
            print(f"Error: Could not find {args.year} MCS release in parent catalog")
            sys.exit(1)
    else:
        print("Error: Must provide either --parent-id or --release-id")
        sys.exit(1)

    # Download commodities
    summary = downloader.download_year_individual_commodities(args.year, catalog_id)

    # Save summary
    summary_file = downloader.output_dir / f"{args.year}_individual_download_summary.json"
    with open(summary_file, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n{'=' * 80}")
    print("Download Summary")
    print(f"{'=' * 80}")
    print(f"Year: {summary['year']}")
    print(f"Status: {summary['status']}")
    print(f"Total files: {summary['total_files']}")
    print(f"Commodities: {len(summary.get('commodities_downloaded', {}))}")
    print(f"Summary saved to: {summary_file}")
    print(f"{'=' * 80}\n")


if __name__ == "__main__":
    main()
