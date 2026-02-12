"""
Helper script to find ScienceBase catalog item IDs for USGS MCS data releases.

This script provides methods to search for or construct URLs for finding
ScienceBase catalog items for years 2020-2022.
"""

from typing import List, Optional

import requests


def search_sciencebase(query: str, max_results: int = 10) -> list[dict]:
    """
    Search ScienceBase catalog for items.

    Args:
        query: Search query string
        max_results: Maximum number of results to return

    Returns:
        List of item dictionaries
    """
    # ScienceBase search endpoint (may vary)
    search_urls = [
        f"https://www.sciencebase.gov/catalog/items/query?q={query}&format=json&max={max_results}",
        f"https://www.sciencebase.gov/catalog/search?q={query}&format=json",
    ]

    for url in search_urls:
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if "items" in data:
                    return data["items"]
                elif isinstance(data, list):
                    return data
        except Exception as e:
            continue

    return []


def find_mcs_item_id(year: int) -> Optional[str]:
    """
    Try to find ScienceBase catalog item ID for a given year.

    Args:
        year: Year to search for (2020-2022)

    Returns:
        Catalog item ID if found, None otherwise
    """
    query = f"Mineral Commodity Summaries {year}"
    results = search_sciencebase(query)

    for item in results:
        title = item.get("title", "").upper()
        if f"{year}" in title and "MINERAL COMMODITY SUMMARIES" in title:
            return item.get("id")

    return None


def main():
    """Main function to search for missing catalog item IDs."""
    print("Searching for USGS MCS ScienceBase Catalog Item IDs")
    print("=" * 70)
    print()

    known_ids = {
        2024: "65a6e45fd34e5af967a46749",
        2023: "63b5f411d34e92aad3caa57f",
    }

    missing_years = [2022, 2021, 2020]

    print("Known catalog item IDs:")
    for year, item_id in known_ids.items():
        print(f"  {year}: {item_id}")
        print(f"    URL: https://www.sciencebase.gov/catalog/item/{item_id}")
    print()

    print("Searching for missing years...")
    print("-" * 70)

    for year in missing_years:
        print(f"\n{year}:")
        item_id = find_mcs_item_id(year)
        if item_id:
            print(f"  ✓ Found: {item_id}")
            print(f"    URL: https://www.sciencebase.gov/catalog/item/{item_id}")
        else:
            print(f"  ✗ Not found via search")
            print(f"    Manual search: https://www.sciencebase.gov/catalog/")
            print(f"    Search for: 'Mineral Commodity Summaries {year}'")

    print("\n" + "=" * 70)
    print("Note: If automatic search fails, you can:")
    print("1. Visit https://www.sciencebase.gov/catalog/")
    print("2. Search for 'Mineral Commodity Summaries [YEAR]'")
    print("3. The item ID is in the URL: .../catalog/item/{ITEM_ID}")
    print("4. Or check USGS data release pages for direct links")


if __name__ == "__main__":
    main()
