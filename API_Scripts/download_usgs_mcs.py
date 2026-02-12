"""
USGS Mineral Commodity Summaries Data Download Script

Downloads and extracts USGS MCS data for CMM-relevant commodities
for years 2020-2024 from ScienceBase catalog.

Based on: https://www.sciencebase.gov/catalog/item/65a6e45fd34e5af967a46749
"""

from __future__ import annotations

import json
import zipfile
from datetime import datetime
from pathlib import Path
from typing import dict, list

import pandas as pd
import requests

# CMM Commodities mapping to USGS file name patterns
# USGS files use format: mcs{year}-{commodity_abbrev}_salient.csv
# Based on methodology document and USGS MCS structure
# Note: USGS uses abbreviated names (e.g., "raree" for rare earths, "lithi" for lithium)
CMM_COMMODITY_MAPPING = {
    "Heavy REE": ["raree", "rare"],  # REE includes both heavy and light
    "Light REE": ["raree", "rare"],
    "Cobalt": ["cobalt", "cobal"],
    "Lithium": ["lithium", "lithi"],
    "Gallium": ["gallium", "galli"],
    "Graphite": ["graphite", "graph"],
    "Nickel": ["nickel", "nicke"],
    "Copper": ["copper", "coppe"],
    "Germanium": ["germanium", "germa"],
    "Manganese": ["manganese", "mangan"],
    "Titanium": ["titanium", "titani"],
    "Platinum Group Metals": ["platinum", "palladium", "rhodium", "ruthenium", "iridium", "osmium"],
    "Tungsten": ["tungsten", "tungs"],
}

# ScienceBase catalog item IDs for each year
# Format: https://www.sciencebase.gov/catalog/item/{ITEM_ID}
SCIENCEBASE_ITEMS = {
    2024: "65a6e45fd34e5af967a46749",  # https://www.sciencebase.gov/catalog/item/65a6e45fd34e5af967a46749
    2023: "63b5f411d34e92aad3caa57f",  # https://www.sciencebase.gov/catalog/item/63b5f411d34e92aad3caa57f
    2022: None,  # Will need to find
    2021: None,  # Will need to find
    2020: None,  # Will need to find
}

# Alternative: Direct download URLs if available
# USGS often provides direct links to zip files


class USGSMCSDownloader:
    """Download and extract USGS Mineral Commodity Summaries data."""

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

    def get_sciencebase_item_info(self, item_id: str) -> dict:
        """
        Get information about a ScienceBase catalog item.

        Args:
            item_id: ScienceBase catalog item ID

        Returns:
            Dictionary with item information including download URLs
        """
        # Try multiple API endpoints
        api_urls = [
            f"https://www.sciencebase.gov/catalog/item/{item_id}?format=json",
            f"https://www.sciencebase.gov/catalog/items/{item_id}?format=json",
        ]

        for api_url in api_urls:
            try:
                response = self.session.get(api_url, timeout=30)
                if response.status_code == 200:
                    return response.json()
            except Exception as e:
                continue

        # If API fails, return empty dict - we'll use direct download URLs
        print(f"  Note: Could not fetch ScienceBase API for {item_id}, will try direct downloads")
        return {}

    def download_file(self, url: str, filepath: Path) -> bool:
        """
        Download a file from URL.

        Args:
            url: URL to download from
            filepath: Local path to save file

        Returns:
            True if successful, False otherwise
        """
        try:
            print(f"  Downloading: {filepath.name}")
            response = self.session.get(url, stream=True, timeout=60)
            response.raise_for_status()

            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"    ✓ Downloaded {filepath.stat().st_size / 1024:.1f} KB")
            return True
        except Exception as e:
            print(f"    ✗ Error downloading {url}: {e}")
            return False

    def extract_zip(self, zip_path: Path, extract_to: Path) -> bool:
        """
        Extract a zip file.

        Args:
            zip_path: Path to zip file
            extract_to: Directory to extract to

        Returns:
            True if successful, False otherwise
        """
        try:
            extract_to.mkdir(exist_ok=True)
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_to)
            print(f"    ✓ Extracted to {extract_to}")
            return True
        except Exception as e:
            print(f"    ✗ Error extracting {zip_path}: {e}")
            return False

    def download_year_data(self, year: int, item_id: str | None = None) -> dict:
        """
        Download USGS MCS data for a specific year.

        Args:
            year: Year to download (2020-2024)
            item_id: ScienceBase catalog item ID (if None, will try to find)

        Returns:
            Dictionary with download status and file paths
        """
        print(f"\n{'=' * 80}")
        print(f"Downloading USGS MCS {year} Data")
        print(f"{'=' * 80}\n")

        year_dir = self.output_dir / str(year)
        year_dir.mkdir(exist_ok=True)

        result = {
            "year": year,
            "downloaded_files": [],
            "extracted_dirs": [],
            "status": "incomplete",
        }

        # Try to get info from ScienceBase
        if item_id:
            item_info = self.get_sciencebase_item_info(item_id)

            # Look for attached files (zip files)
            if item_info and "files" in item_info:
                for file_info in item_info["files"]:
                    if file_info.get("name", "").endswith(".zip"):
                        url = (
                            file_info.get("url")
                            or file_info.get("downloadUri")
                            or file_info.get("downloadURL")
                        )
                        if url:
                            filename = file_info.get("name", url.split("/")[-1])
                            zip_path = year_dir / filename

                            if self.download_file(url, zip_path):
                                result["downloaded_files"].append(str(zip_path))

                                # Extract
                                extract_dir = year_dir / filename.replace(".zip", "")
                                if self.extract_zip(zip_path, extract_dir):
                                    result["extracted_dirs"].append(str(extract_dir))

        # Also try direct download from ScienceBase file service
        # ScienceBase file URLs follow pattern: https://www.sciencebase.gov/catalog/file/get/{item_id}?name={filename}
        if item_id and not result["downloaded_files"]:
            # Common zip file names for MCS data
            zip_names = [
                "salient.zip",
                "world.zip",
                f"mcs{year}_data.zip",
                f"MCS_{year}_Data.zip",
            ]

            for zip_name in zip_names:
                url = f"https://www.sciencebase.gov/catalog/file/get/{item_id}?name={zip_name}"
                zip_path = year_dir / zip_name

                if self.download_file(url, zip_path):
                    result["downloaded_files"].append(str(zip_path))
                    extract_dir = year_dir / zip_name.replace(".zip", "")
                    if self.extract_zip(zip_path, extract_dir):
                        result["extracted_dirs"].append(str(extract_dir))
                    break

        if not result["downloaded_files"]:
            print(f"  ⚠ No files downloaded for {year}")
            print(f"  Note: May need to manually download from:")
            print(f"    https://www.sciencebase.gov/catalog/item/{item_id}")

        result["status"] = "complete" if result["downloaded_files"] else "failed"
        return result

    def extract_cmm_commodities(self, year: int) -> dict:
        """
        Extract CMM-relevant commodity data from downloaded files.

        Args:
            year: Year to process

        Returns:
            Dictionary with extracted commodity data
        """
        print(f"\n{'=' * 80}")
        print(f"Extracting CMM Commodities for {year}")
        print(f"{'=' * 80}\n")

        year_dir = self.output_dir / str(year)
        cmm_dir = self.output_dir / "cmm_extracted" / str(year)
        cmm_dir.mkdir(parents=True, exist_ok=True)

        extracted = {}

        # Find all CSV files in year directory
        csv_files = list(year_dir.rglob("*.csv"))

        print(f"Found {len(csv_files)} CSV files")

        # Map USGS commodity names to our CMM categories
        # USGS files use format: mcs{year}-{commodity_abbrev}_salient.csv
        for cmm_category, usgs_patterns in CMM_COMMODITY_MAPPING.items():
            matching_files = []

            for csv_file in csv_files:
                filename_lower = csv_file.name.lower()
                # Check if file matches any pattern for this CMM category
                for pattern in usgs_patterns:
                    if pattern.lower() in filename_lower:
                        matching_files.append(csv_file)
                        break

            if matching_files:
                print(f"\n{cmm_category}:")
                for csv_file in matching_files:
                    print(f"  Found: {csv_file.name}")

                    # Copy to CMM directory
                    dest_file = (
                        cmm_dir / f"{cmm_category.lower().replace(' ', '_')}_{csv_file.name}"
                    )
                    try:
                        df = pd.read_csv(csv_file)
                        df.to_csv(dest_file, index=False)
                        extracted[cmm_category] = extracted.get(cmm_category, []) + [str(dest_file)]
                        print(f"    ✓ Extracted {len(df)} rows")
                    except Exception as e:
                        print(f"    ✗ Error processing {csv_file}: {e}")

        return extracted

    def download_all_years(self, years: list[int] = [2020, 2021, 2022, 2023, 2024]) -> dict:
        """
        Download USGS MCS data for all specified years.

        Args:
            years: list of years to download

        Returns:
            Summary of downloads
        """
        print("\n" + "=" * 80)
        print("USGS Mineral Commodity Summaries Data Download")
        print("=" * 80)
        print(f"Output directory: {self.output_dir}")
        print(f"Years: {years}")
        print("=" * 80)

        summary = {"download_date": datetime.now().isoformat(), "years": {}, "cmm_extracted": {}}

        for year in years:
            item_id = SCIENCEBASE_ITEMS.get(year)
            result = self.download_year_data(year, item_id)
            summary["years"][year] = result

            # Extract CMM commodities
            if result["status"] == "complete":
                extracted = self.extract_cmm_commodities(year)
                summary["cmm_extracted"][year] = extracted

        # Save summary
        summary_file = self.output_dir / "download_summary.json"
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)

        print(f"\n{'=' * 80}")
        print("Download Summary")
        print(f"{'=' * 80}")
        print(f"Summary saved to: {summary_file}")
        print(f"{'=' * 80}\n")

        return summary


def main():
    """Main function for command-line interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Download USGS Mineral Commodity Summaries data for CMM commodities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download all years (2020-2024)
  python download_usgs_mcs.py --output-dir usgs_mcs_data
  
  # Download specific year
  python download_usgs_mcs.py --year 2024 --output-dir usgs_mcs_data
  
  # Download with ScienceBase item ID
  python download_usgs_mcs.py --year 2024 --item-id 65a6e45fd34e5af967a46749
        """,
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="usgs_mcs_data",
        help="Output directory for downloaded data (default: usgs_mcs_data)",
    )

    parser.add_argument(
        "--year", type=int, help="Specific year to download (default: all years 2020-2024)"
    )

    parser.add_argument("--item-id", type=str, help="ScienceBase catalog item ID for the year")

    parser.add_argument(
        "--years",
        type=int,
        nargs="+",
        default=[2020, 2021, 2022, 2023, 2024],
        help="List of years to download (default: 2020-2024)",
    )

    args = parser.parse_args()

    downloader = USGSMCSDownloader(output_dir=args.output_dir)

    if args.year:
        # Download single year
        item_id = args.item_id or SCIENCEBASE_ITEMS.get(args.year)
        result = downloader.download_year_data(args.year, item_id)
        if result["status"] == "complete":
            downloader.extract_cmm_commodities(args.year)
    else:
        # Download all years
        downloader.download_all_years(args.years)


if __name__ == "__main__":
    main()
