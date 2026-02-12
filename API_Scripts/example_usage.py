"""
Example usage of the UN Comtrade API query tool.

This script demonstrates various ways to use the ComtradeQuery class
to retrieve CMM trade flow data.
"""

import os
from un_comtrade_query import ComtradeQuery, CMM_HS_CODES


# Example 1: Basic query using API key from environment variable
def example_basic_query():
    """Basic query example."""
    print("Example 1: Basic Query")
    print("-" * 60)

    # Make sure to set your API key as environment variable:
    # export UN_COMTRADE_API_KEY=your_key_here

    # Or pass it directly:
    api_key = os.getenv("UN_COMTRADE_API_KEY")
    if not api_key:
        print("Please set UN_COMTRADE_API_KEY environment variable")
        return

    query = ComtradeQuery(api_key=api_key)

    # Query REE compounds trade between USA and China in 2023
    df = query.query_trade_data(
        reporter="USA",
        partner="CHN",
        commodity_code="2846",  # REE compounds
        year=2023,
        trade_flow="both",
    )

    print(f"Retrieved {len(df)} records")
    print(df.head())
    print()


# Example 2: Query using commodity name
def example_commodity_name_query():
    """Query using CMM commodity name."""
    print("Example 2: Query Using Commodity Name")
    print("-" * 60)

    api_key = os.getenv("UN_COMTRADE_API_KEY")
    if not api_key:
        print("Please set UN_COMTRADE_API_KEY environment variable")
        return

    query = ComtradeQuery(api_key=api_key)

    # Query Lithium ores trade
    df = query.query_cmm_commodity(
        commodity_name="Lithium_ores",
        reporter="AUS",  # Australia (major lithium producer)
        partner="CHN",  # China (major consumer)
        year=2023,
        trade_flow="export",  # Only exports from Australia
    )

    print(f"Retrieved {len(df)} records")
    print(df.head())
    print()


# Example 3: Query multiple commodities
def example_multiple_commodities():
    """Query multiple CMM commodities."""
    print("Example 3: Query Multiple Commodities")
    print("-" * 60)

    api_key = os.getenv("UN_COMTRADE_API_KEY")
    if not api_key:
        print("Please set UN_COMTRADE_API_KEY environment variable")
        return

    query = ComtradeQuery(api_key=api_key)

    # Query all REE-related commodities
    ree_commodities = {"REE_compounds": "2846", "REE_metals": "280530"}

    all_results = []
    for name, code in ree_commodities.items():
        print(f"Querying {name} (HS: {code})...")
        df = query.query_trade_data(
            reporter="USA", partner="CHN", commodity_code=code, year=2023, trade_flow="both"
        )
        if not df.empty:
            df["commodity_name"] = name
            all_results.append(df)

    if all_results:
        import pandas as pd

        combined = pd.concat(all_results, ignore_index=True)
        print(f"\nTotal records across all REE commodities: {len(combined)}")
        print(combined.head())
    print()


# Example 4: Save results to file
def example_save_results():
    """Save query results to file."""
    print("Example 4: Save Results to File")
    print("-" * 60)

    api_key = os.getenv("UN_COMTRADE_API_KEY")
    if not api_key:
        print("Please set UN_COMTRADE_API_KEY environment variable")
        return

    query = ComtradeQuery(api_key=api_key)

    # Query Cobalt trade
    df = query.query_cmm_commodity(
        commodity_name="Cobalt",
        reporter="USA",
        partner="ALL",  # All partners
        year=2023,
        trade_flow="both",
    )

    # Save to different formats
    if not df.empty:
        query.save_results(df, "cobalt_trade_2023.csv", format="csv")
        query.save_results(df, "cobalt_trade_2023.json", format="json")
        print("Results saved to cobalt_trade_2023.csv and cobalt_trade_2023.json")
    print()


# Example 5: Preview mode (no API key needed, limited to 500 records)
def example_preview_mode():
    """Use preview mode without API key."""
    print("Example 5: Preview Mode (No API Key Required)")
    print("-" * 60)

    # Preview mode doesn't require an API key
    query = ComtradeQuery(api_key=None)  # No API key needed for preview mode

    # Use preview=True for testing (limited to 500 records)
    df = query.query_trade_data(
        reporter="USA",
        partner="CHN",
        commodity_code="2846",
        year=2023,
        trade_flow="import",
        preview=True,  # Preview mode
    )

    print(f"Retrieved {len(df)} records (preview mode)")
    print(df.head())
    print()


# Example 6: List all available CMM commodities
def example_list_commodities():
    """List all available CMM commodities."""
    print("Example 6: Available CMM Commodities")
    print("-" * 60)

    print("\nCMM HS Codes:")
    for name, code in CMM_HS_CODES.items():
        print(f"  {name:30s}  HS Code: {code}")
    print()


if __name__ == "__main__":
    print("UN Comtrade API Query Examples")
    print("=" * 60)
    print()

    # Check if API key is set
    api_key = os.getenv("UN_COMTRADE_API_KEY")
    if not api_key:
        print("NOTE: UN_COMTRADE_API_KEY environment variable not set.")
        print("Some examples require an API key. You can:")
        print("  1. Register at https://comtradedeveloper.un.org/apis")
        print("  2. Set the key: export UN_COMTRADE_API_KEY=your_key_here")
        print()

    # Run examples (comment out those that require API key if not set)
    example_list_commodities()

    if api_key:
        # Uncomment the examples you want to run:
        # example_basic_query()
        # example_commodity_name_query()
        # example_multiple_commodities()
        # example_save_results()
        # example_preview_mode()
        print("Uncomment examples in the script to run them.")
    else:
        example_preview_mode()  # This one doesn't require API key
