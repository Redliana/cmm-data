"""
Helper script to find individual commodity catalog item IDs for 2022 MCS.

Since the 2022 release has individual commodity items, we need to find
the catalog item ID for each CMM commodity.
"""

import requests
import re
import json
from typing import Dict, List

# CMM commodities we need
CMM_COMMODITIES_2022 = [
    "RARE EARTHS",  # Covers both Heavy and Light REE
    "COBALT",
    "LITHIUM",
    "GALLIUM",
    "GRAPHITE",
    "NICKEL",
    "COPPER",
    "GERMANIUM",
    "MANGANESE",
    "TITANIUM",
    "TUNGSTEN",
    "PLATINUM",
    "PALLADIUM",
]


def search_commodity_item(year: int, commodity: str, parent_id: str = None) -> Dict:
    """
    Search for a specific commodity's catalog item ID.

    Args:
        year: Year (2022)
        commodity: Commodity name
        parent_id: Optional parent catalog ID to search within

    Returns:
        Dictionary with item info if found
    """
    # Try searching ScienceBase
    search_queries = [
        f"Mineral Commodity Summaries {year} {commodity}",
        f"MCS {year} {commodity}",
    ]

    for query in search_queries:
        try:
            # Try search endpoint
            search_url = (
                f"https://www.sciencebase.gov/catalog/items/query?q={query}&format=json&max=10"
            )
            response = requests.get(search_url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                items = data.get("items", []) if isinstance(data, dict) else data
                for item in items:
                    title = item.get("title", "").upper()
                    if str(year) in title and commodity.upper() in title:
                        return {
                            "commodity": commodity,
                            "item_id": item.get("id"),
                            "title": item.get("title"),
                            "url": f"https://www.sciencebase.gov/catalog/item/{item.get('id')}",
                        }
        except Exception as e:
            continue

    return None


def find_all_commodity_items(year: int = 2022) -> Dict[str, Dict]:
    """
    Find all CMM commodity item IDs for a given year.

    Args:
        year: Year to search for

    Returns:
        Dictionary mapping commodity names to item info
    """
    print(f"Searching for {year} MCS CMM commodity items...")
    print("=" * 70)

    results = {}

    for commodity in CMM_COMMODITIES_2022:
        print(f"\nSearching for {commodity}...")
        result = search_commodity_item(year, commodity)
        if result:
            results[commodity] = result
            print(f"  ✓ Found: {result['title']}")
            print(f"    ID: {result['item_id']}")
        else:
            print(f"  ✗ Not found via search")
            print(f"    Manual search: https://www.sciencebase.gov/catalog/")
            print(f"    Search for: 'Mineral Commodity Summaries {year} {commodity}'")

    return results


def main():
    """Main function."""
    results = find_all_commodity_items(2022)

    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"Found {len(results)}/{len(CMM_COMMODITIES_2022)} commodities")

    if results:
        print("\nFound commodity item IDs:")
        for commodity, info in results.items():
            print(f"  {commodity}: {info['item_id']}")

        # Save to file
        output_file = "2022_commodity_item_ids.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nSaved to: {output_file}")
    else:
        print("\nNo items found. You may need to:")
        print("1. Visit https://www.sciencebase.gov/catalog/item/6197ccbed34eb622f692ee1c")
        print("2. Browse the child items to find each commodity")
        print("3. Extract the item IDs from the URLs")


if __name__ == "__main__":
    main()
