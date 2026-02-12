"""
USGS MCS 2022 Individual Commodity Download Script (Manual Item IDs)

For 2022 and earlier years, USGS MCS data is organized as individual commodity items.
This script downloads CMM-relevant commodities when you provide the catalog item IDs.

Usage:
1. Find the catalog item IDs for each commodity (see instructions below)
2. Update the COMMODITY_ITEM_IDS dictionary with the IDs
3. Run the script to download all commodities
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import dict, list

import requests

# CMM Commodities from methodology (Section 2.2)
# Map to USGS commodity names and expected catalog item IDs
COMMODITY_ITEM_IDS = {
    # Format: 'USGS_COMMODITY_NAME': {'item_id': '...', 'cmm_categories': [...]}
    "RARE EARTHS": {
        "item_id": None,  # To be filled in
        "cmm_categories": ["Heavy REE", "Light REE"],
    },
    "COBALT": {"item_id": None, "cmm_categories": ["Cobalt"]},
    "LITHIUM": {"item_id": None, "cmm_categories": ["Lithium"]},
    "GALLIUM": {"item_id": None, "cmm_categories": ["Gallium"]},
    "GRAPHITE": {"item_id": None, "cmm_categories": ["Graphite"]},
    "NICKEL": {"item_id": None, "cmm_categories": ["Nickel"]},
    "COPPER": {"item_id": None, "cmm_categories": ["Copper"]},
    "GERMANIUM": {"item_id": None, "cmm_categories": ["Germanium"]},
    "MANGANESE": {"item_id": None, "cmm_categories": ["Manganese"]},
    "TITANIUM": {"item_id": None, "cmm_categories": ["Titanium"]},
    "TUNGSTEN": {"item_id": None, "cmm_categories": ["Tungsten"]},
    "PLATINUM": {"item_id": None, "cmm_categories": ["Platinum Group Metals"]},
    "PALLADIUM": {"item_id": None, "cmm_categories": ["Platinum Group Metals"]},
}


class USGSMCS2022Downloader:
    """Download individual commodity data from 2022 USGS MCS release."""

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
        except Exception as e:
            print(f"Error fetching item {item_id}: {e}")
        return {}

    def download_commodity_files(
        self, item_id: str, commodity_name: str, year: int = 2022
    ) -> list[Path]:
        """
        Download all CSV files from a commodity catalog item.

        Args:
            item_id: ScienceBase catalog item ID
            commodity_name: Name of the commodity
            year: Year of the data

        Returns:
            list of downloaded file paths
        """
        item_info = self.get_catalog_item(item_id)
        if not item_info:
            print(f"  ✗ Could not fetch item {item_id}")
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
                    except Exception as e:
                        print(f"      ✗ Error: {e}")

        return downloaded_files

    def download_all_commodities(self, commodity_ids: dict, year: int = 2022) -> dict:
        """
        Download all CMM commodities for 2022.

        Args:
            commodity_ids: Dictionary mapping commodity names to item IDs
            year: Year (2022)

        Returns:
            Summary of downloads
        """
        print(f"\n{'=' * 80}")
        print(f"Downloading USGS MCS {year} Individual Commodity Data")
        print(f"{'=' * 80}\n")

        summary = {
            "year": year,
            "commodities_downloaded": {},
            "total_files": 0,
            "status": "incomplete",
        }

        for commodity_name, info in commodity_ids.items():
            item_id = info.get("item_id")
            if not item_id:
                print(f"\n{commodity_name}: ⚠ No item ID provided - skipping")
                continue

            print(f"\n{commodity_name} (ID: {item_id}):")
            files = self.download_commodity_files(item_id, commodity_name, year)

            if files:
                cmm_categories = info.get("cmm_categories", [commodity_name])
                for cmm_cat in cmm_categories:
                    if cmm_cat not in summary["commodities_downloaded"]:
                        summary["commodities_downloaded"][cmm_cat] = []
                    summary["commodities_downloaded"][cmm_cat].extend([str(f) for f in files])

                summary["total_files"] += len(files)
                print(f"  ✓ Downloaded {len(files)} files")
            else:
                print(f"  ✗ No files downloaded")

        summary["status"] = "complete" if summary["total_files"] > 0 else "failed"

        # Save summary
        summary_file = self.output_dir / f"{year}_manual_download_summary.json"
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)

        print(f"\n{'=' * 80}")
        print("Download Summary")
        print(f"{'=' * 80}")
        print(f"Year: {summary['year']}")
        print(f"Status: {summary['status']}")
        print(f"Total files: {summary['total_files']}")
        print(f"Commodities: {len(summary['commodities_downloaded'])}")
        print(f"Summary saved to: {summary_file}")
        print(f"{'=' * 80}\n")

        return summary


def main():
    """Main function for command-line interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Download USGS MCS 2022 individual commodity data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
To find catalog item IDs:
1. Visit: https://www.sciencebase.gov/catalog/item/6197ccbed34eb622f692ee1c
2. Browse the child items (individual commodities)
3. Click on each CMM commodity (Lithium, Cobalt, etc.)
4. Copy the item ID from the URL: .../catalog/item/{ITEM_ID}
5. Update COMMODITY_ITEM_IDS in this script or use --item-ids-file

Alternatively, use --item-ids-file to provide a JSON file with item IDs.
        """,
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="usgs_mcs_data",
        help="Output directory for downloaded data",
    )

    parser.add_argument(
        "--item-ids-file",
        type=str,
        help='JSON file with commodity item IDs (format: {"RARE EARTHS": {"item_id": "..."}, ...})',
    )

    parser.add_argument("--year", type=int, default=2022, help="Year (default: 2022)")

    args = parser.parse_args()

    # Load item IDs
    if args.item_ids_file and Path(args.item_ids_file).exists():
        with open(args.item_ids_file) as f:
            commodity_ids = json.load(f)
    else:
        commodity_ids = COMMODITY_ITEM_IDS

    # Check if any item IDs are provided
    provided_ids = sum(1 for info in commodity_ids.values() if info.get("item_id"))
    if provided_ids == 0:
        print("⚠ No item IDs provided!")
        print("\nTo use this script:")
        print("1. Find catalog item IDs for each commodity")
        print("2. Update COMMODITY_ITEM_IDS in the script, or")
        print("3. Create a JSON file with item IDs and use --item-ids-file")
        print("\nSee script help for instructions on finding item IDs.")
        sys.exit(1)

    print(f"Using {provided_ids}/{len(commodity_ids)} commodity item IDs")

    downloader = USGSMCS2022Downloader(output_dir=args.output_dir)
    summary = downloader.download_all_commodities(commodity_ids, year=args.year)


if __name__ == "__main__":
    main()
