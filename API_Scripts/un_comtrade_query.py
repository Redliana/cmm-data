"""
UN Comtrade API Query Tool for Critical Minerals and Materials (CMM)

.. deprecated::
    This standalone script is deprecated. Use the UNComtrade MCP Server instead,
    which provides the same functionality (and more) as an MCP tool server:

        Location: Data_Needs/UNComtrade_MCP/
        Install:  cd Data_Needs/UNComtrade_MCP && pip install -e .
        Run:      uncomtrade-mcp

    The MCP server includes all HS codes from this script plus additional minerals,
    supports async queries, provides country trade profiles, commodity summaries,
    and integrates directly with Claude Code and Claude Desktop.

    This file is kept for reference only and may be removed in a future cleanup.

Original description:
    This script provides functions to query the UN Comtrade API for trade flow data
    related to critical minerals and materials, including rare earth elements,
    lithium, cobalt, graphite, gallium, and germanium.

Usage (deprecated):
    python un_comtrade_query.py --reporter USA --partner CHN --commodity 2846 --year 2023 --api-key YOUR_KEY

Or set API key as environment variable:
    export UN_COMTRADE_API_KEY=your_key_here
    python un_comtrade_query.py --reporter USA --partner CHN --commodity 2846 --year 2023
"""

from __future__ import annotations

import argparse
import os
import sys
import warnings

import pandas as pd

warnings.warn(
    "un_comtrade_query.py is deprecated. Use the UNComtrade MCP Server instead "
    "(Data_Needs/UNComtrade_MCP/). See module docstring for details.",
    DeprecationWarning,
    stacklevel=2,
)

try:
    from comtradeapicall import getFinalData, previewFinalData
except ImportError:
    print("Error: comtradeapicall package not found. Please install it with:")
    print("  pip install comtradeapicall")
    sys.exit(1)

# CMM HS Codes (per UNCTAD mapping from CMM_API_MCP_Analysis.md)
CMM_HS_CODES = {
    # Rare Earth Elements
    "REE_compounds": "2846",  # Rare earth compounds
    "REE_metals": "280530",  # Rare earth metals
    # Lithium
    "Lithium_ores": "253090",  # Lithium ores/carbonate
    "Lithium_carbonate": "283691",  # Lithium carbonate
    "Lithium_hydroxide": "282520",  # Lithium hydroxide
    # Cobalt
    "Cobalt": "8105",  # Cobalt and articles
    "Cobalt_oxides": "282200",  # Cobalt oxides
    # Graphite
    "Graphite_natural": "250410",  # Natural graphite
    "Graphite_artificial": "380110",  # Artificial graphite
    # Gallium and Germanium
    "Gallium_Germanium": "811292",  # Gallium and Germanium
    # Nickel (for battery-grade Class 1 nickel)
    "Nickel_unwrought": "7502",  # Unwrought nickel (refined)
    "Nickel_matte": "7501",  # Nickel mattes and intermediate products
    "Nickel_oxides": "281122",  # Nickel oxides and hydroxides
    # Copper
    "Copper_refined": "7402",  # Unwrought refined copper
    "Copper_unrefined": "7403",  # Unwrought unrefined copper
}

# ISO country codes to UN Comtrade numeric codes
# UN Comtrade uses numeric codes: https://unstats.un.org/unsd/tradekb/knowledgebase/country-code
COUNTRY_CODES = {
    "USA": "842",  # United States
    "CHN": "156",  # China
    "DEU": "276",  # Germany
    "JPN": "392",  # Japan
    "KOR": "410",  # South Korea
    "AUS": "36",  # Australia
    "CAN": "124",  # Canada
    "GBR": "826",  # United Kingdom
    "FRA": "250",  # France
    "IND": "699",  # India
    "COD": "180",  # Democratic Republic of the Congo (DRC)
    "IDN": "360",  # Indonesia
    "ALL": "0",  # All partners
}


class ComtradeQuery:
    """Class to handle UN Comtrade API queries for CMM data."""

    def __init__(self, api_key: str | None = None):
        """
        Initialize ComtradeQuery instance.

        Args:
            api_key: UN Comtrade API key. If None, will try to get from
                    UN_COMTRADE_API_KEY environment variable. API key is only
                    required for non-preview queries (preview mode doesn't need it).
        """
        if api_key is None:
            api_key = os.getenv("UN_COMTRADE_API_KEY")

        self.api_key = api_key  # Store None if not provided (OK for preview mode)

    def query_trade_data(
        self,
        reporter: str,
        partner: str,
        commodity_code: str,
        year: int,
        trade_flow: str = "both",  # 'import', 'export', or 'both'
        preview: bool = False,
    ) -> pd.DataFrame:
        """
        Query UN Comtrade API for trade flow data.

        Args:
            reporter: ISO 3-letter country code for reporting country (e.g., 'USA', 'CHN')
            partner: ISO 3-letter country code for partner country (e.g., 'USA', 'CHN', 'ALL')
            commodity_code: HS commodity code (e.g., '2846' for REE compounds)
            year: Year of trade data (e.g., 2023)
            trade_flow: 'import' (1), 'export' (2), or 'both' (queries both)
            preview: If True, uses previewFinalData (500 records, no key needed)
                    If False, uses getFinalData (up to 250,000 records, requires key)

        Returns:
            pandas DataFrame with trade data
        """
        results = []

        flows_to_query = []
        if trade_flow == "both":
            flows_to_query = ["1", "2"]  # Import and Export
        elif trade_flow == "import":
            flows_to_query = ["1"]
        elif trade_flow == "export":
            flows_to_query = ["2"]
        else:
            raise ValueError(f"trade_flow must be 'import', 'export', or 'both', got: {trade_flow}")

        # Convert country codes to numeric format
        reporter_code = COUNTRY_CODES.get(reporter, reporter)
        partner_code = COUNTRY_CODES.get(partner, partner)

        # Map flow codes: '1' or 'import' -> 'M', '2' or 'export' -> 'X'
        flow_map = {"1": "M", "2": "X", "import": "M", "export": "X"}

        for flow in flows_to_query:
            try:
                # Convert flow code to UN Comtrade format
                flow_code = flow_map.get(flow, flow)
                if flow_code not in ["M", "X"]:
                    raise ValueError(
                        f"Invalid flow code: {flow}. Must be 'M' (import) or 'X' (export)"
                    )

                # Format period as year string (e.g., '2023')
                period = str(year)

                if not preview:
                    # Validate API key is present for non-preview queries
                    if not self.api_key:
                        raise ValueError(
                            "API key required for non-preview queries. "
                            "Provide it as parameter to ComtradeQuery() or set "
                            "UN_COMTRADE_API_KEY environment variable. "
                            "Register at: https://comtradedeveloper.un.org/apis"
                        )
                    # getFinalData parameters: (subscription_key, typeCode, freqCode, clCode, period,
                    #                          reporterCode, cmdCode, flowCode, partnerCode,
                    #                          partner2Code, customsCode, motCode, ...)
                    data = getFinalData(
                        subscription_key=self.api_key,
                        typeCode="C",  # Commodities
                        freqCode="A",  # Annual
                        clCode="HS",  # Harmonized System
                        period=period,
                        reporterCode=reporter_code,
                        cmdCode=commodity_code,
                        flowCode=flow_code,  # 'M' for import, 'X' for export
                        partnerCode=partner_code,
                        partner2Code=None,  # Not used
                        customsCode=None,  # Not used
                        motCode=None,  # Not used
                    )
                else:
                    # previewFinalData parameters: (typeCode, freqCode, clCode, period, reporterCode,
                    #                               cmdCode, flowCode, partnerCode, partner2Code,
                    #                               customsCode, motCode, ...)
                    data = previewFinalData(
                        typeCode="C",
                        freqCode="A",
                        clCode="HS",
                        period=period,
                        reporterCode=reporter_code,
                        cmdCode=commodity_code,
                        flowCode=flow_code,
                        partnerCode=partner_code,
                        partner2Code=None,
                        customsCode=None,
                        motCode=None,
                    )

                if data is not None and not data.empty:
                    results.append(data)

            except Exception as e:
                print(f"Warning: Error querying flow {flow} for {reporter}-{partner}: {e}")
                continue

        if results:
            combined_df = pd.concat(results, ignore_index=True)
            return combined_df
        else:
            return pd.DataFrame()  # Return empty DataFrame if no results

    def query_cmm_commodity(
        self,
        commodity_name: str,
        reporter: str,
        partner: str,
        year: int,
        trade_flow: str = "both",
        preview: bool = False,
    ) -> pd.DataFrame:
        """
        Query trade data for a CMM commodity by name.

        Args:
            commodity_name: Name of commodity (e.g., 'REE_compounds', 'Lithium_ores')
            reporter: ISO 3-letter country code for reporting country
            partner: ISO 3-letter country code for partner country
            year: Year of trade data
            trade_flow: 'import', 'export', or 'both'
            preview: Use preview API (limited to 500 records)

        Returns:
            pandas DataFrame with trade data
        """
        if commodity_name not in CMM_HS_CODES:
            available = ", ".join(CMM_HS_CODES.keys())
            raise ValueError(f"Unknown commodity: {commodity_name}. Available options: {available}")

        hs_code = CMM_HS_CODES[commodity_name]
        return self.query_trade_data(
            reporter=reporter,
            partner=partner,
            commodity_code=hs_code,
            year=year,
            trade_flow=trade_flow,
            preview=preview,
        )

    def save_results(self, df: pd.DataFrame, output_file: str, format: str = "auto"):
        """
        Save query results to file.

        Args:
            df: DataFrame to save
            output_file: Output file path
            format: File format ('csv', 'json', 'excel', or 'auto' to infer from extension)
        """
        if format == "auto":
            ext = os.path.splitext(output_file)[1].lower()
            if ext == ".csv":
                format = "csv"
            elif ext == ".json":
                format = "json"
            elif ext in [".xlsx", ".xls"]:
                format = "excel"
            else:
                format = "csv"  # Default to CSV

        if format == "csv":
            df.to_csv(output_file, index=False)
        elif format == "json":
            df.to_json(output_file, orient="records", indent=2)
        elif format == "excel":
            df.to_excel(output_file, index=False)
        else:
            raise ValueError(f"Unsupported format: {format}")


def main():
    """Main function for command-line interface."""
    parser = argparse.ArgumentParser(
        description="Query UN Comtrade API for CMM trade data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Query REE compounds trade between USA and China in 2023
  python un_comtrade_query.py --reporter USA --partner CHN --commodity 2846 --year 2023
  
  # Query using commodity name
  python un_comtrade_query.py --reporter USA --partner CHN --commodity-name REE_compounds --year 2023
  
  # Query only imports
  python un_comtrade_query.py --reporter USA --partner CHN --commodity 2846 --year 2023 --flow import
  
  # Save to CSV
  python un_comtrade_query.py --reporter USA --partner CHN --commodity 2846 --year 2023 --output results.csv
  
  # list available CMM commodities
  python un_comtrade_query.py --list-commodities
        """,
    )

    parser.add_argument(
        "--api-key", type=str, help="UN Comtrade API key (or set UN_COMTRADE_API_KEY env var)"
    )

    parser.add_argument(
        "--reporter",
        type=str,
        help="ISO 3-letter country code for reporting country (e.g., USA, CHN)",
    )

    parser.add_argument(
        "--partner",
        type=str,
        help="ISO 3-letter country code for partner country (e.g., USA, CHN, ALL)",
    )

    parser.add_argument(
        "--commodity", type=str, help="HS commodity code (e.g., 2846 for REE compounds)"
    )

    parser.add_argument(
        "--commodity-name", type=str, help="CMM commodity name (e.g., REE_compounds, Lithium_ores)"
    )

    parser.add_argument("--year", type=int, help="Year of trade data (e.g., 2023)")

    parser.add_argument(
        "--flow",
        type=str,
        choices=["import", "export", "both"],
        default="both",
        help="Trade flow direction (default: both)",
    )

    parser.add_argument("--output", type=str, help="Output file path (CSV, JSON, or Excel format)")

    parser.add_argument(
        "--preview",
        action="store_true",
        help="Use preview API (500 records max, no API key needed)",
    )

    parser.add_argument(
        "--list-commodities",
        action="store_true",
        help="List available CMM commodity names and HS codes",
    )

    args = parser.parse_args()

    # list commodities if requested
    if args.list_commodities:
        print("\nAvailable CMM Commodities:")
        print("-" * 60)
        for name, code in CMM_HS_CODES.items():
            print(f"  {name:25s}  HS Code: {code}")
        print()
        return

    # Validate required arguments
    if not args.commodity and not args.commodity_name:
        parser.error("Must provide either --commodity or --commodity-name")

    if not args.reporter:
        parser.error("--reporter is required")

    if not args.partner:
        parser.error("--partner is required")

    if not args.year:
        parser.error("--year is required")

    # Initialize query object (API key only needed for non-preview queries)
    query = ComtradeQuery(api_key=args.api_key)

    # Execute query
    try:
        if args.commodity_name:
            df = query.query_cmm_commodity(
                commodity_name=args.commodity_name,
                reporter=args.reporter,
                partner=args.partner,
                year=args.year,
                trade_flow=args.flow,
                preview=args.preview,
            )
        else:
            df = query.query_trade_data(
                reporter=args.reporter,
                partner=args.partner,
                commodity_code=args.commodity,
                year=args.year,
                trade_flow=args.flow,
                preview=args.preview,
            )

        if df.empty:
            print("No data returned from query.")
            sys.exit(1)

        # Display results
        print(f"\nQuery Results ({len(df)} records):")
        print("=" * 80)
        print(df.head(20).to_string())
        if len(df) > 20:
            print(f"\n... and {len(df) - 20} more records")
        print()

        # Save to file if requested
        if args.output:
            query.save_results(df, args.output)
            print(f"Results saved to: {args.output}")

    except Exception as e:
        print(f"Error executing query: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
