"""
UN Comtrade Data Collection Script for CMM Gold Q&A Methodology

This script systematically pulls trade flow data from UN Comtrade API
based on the requirements from CMM_LLM_Baseline_Gold_QA_Methodology.md

Focus: Trade Flow questions (Q-TF sub-domain) - 10 questions total
Years: 2020-2024 (covers both Stratum A and Stratum B temporal requirements)
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import dict, list, tuple

import pandas as pd

# Import the ComtradeQuery class
from un_comtrade_query import CMM_HS_CODES, COUNTRY_CODES, ComtradeQuery

# Additional HS codes (some may be in main file, these are for reference)
# Note: Nickel and Copper codes should be in un_comtrade_query.py
ADDITIONAL_HS_CODES = {
    "Nickel_unwrought": "7502",  # Unwrought nickel (refined, battery-grade)
    "Nickel_matte": "7501",  # Nickel mattes
    "Copper_refined": "7402",  # Refined copper
}

# Merge with existing codes
ALL_CMM_CODES = {**CMM_HS_CODES, **ADDITIONAL_HS_CODES}

# Gold Q&A Methodology Requirements
# Based on CMM_LLM_Baseline_Gold_QA_Methodology.md Section 4.2

COMMODITY_TRADE_FLOW_REQUIREMENTS = {
    "Heavy REE": {
        "hs_codes": ["2846", "280530"],  # REE compounds and metals
        "q_tf_questions": 1,
        "key_countries": ["USA", "CHN"],
        "description": "Heavy REE (Dy, Tb) trade flows",
    },
    "Cobalt": {
        "hs_codes": ["8105", "282200"],  # Cobalt and oxides
        "q_tf_questions": 2,
        "key_countries": ["USA", "CHN", "COD"],  # COD = DRC
        "description": "Cobalt trade flows (DRC mining, China refining)",
    },
    "Lithium": {
        "hs_codes": ["253090", "283691", "282520"],  # Ores, carbonate, hydroxide
        "q_tf_questions": 1,
        "key_countries": ["USA", "CHN", "AUS"],  # Australia is major producer
        "description": "Lithium trade flows",
    },
    "Gallium": {
        "hs_codes": ["811292"],  # Shared with Germanium
        "q_tf_questions": 1,
        "key_countries": ["USA", "CHN"],
        "description": "Gallium trade flows (2023 export controls)",
    },
    "Graphite": {
        "hs_codes": ["250410", "380110"],  # Natural and artificial
        "q_tf_questions": 1,
        "key_countries": ["USA", "CHN"],
        "description": "Graphite trade flows (processing chokepoint)",
    },
    "Light REE": {
        "hs_codes": ["2846", "280530"],  # Same as Heavy REE but different focus
        "q_tf_questions": 1,
        "key_countries": ["USA", "CHN"],
        "description": "Light REE (Nd, Pr) trade flows",
    },
    "Nickel": {
        "hs_codes": ["7502", "7501"],  # Unwrought nickel (refined), mattes
        "q_tf_questions": 1,
        "key_countries": ["USA", "CHN", "IDN"],  # Indonesia is major producer
        "description": "Nickel trade flows (Class 1 battery-grade)",
    },
    "Copper": {
        "hs_codes": ["7402", "7403"],  # Refined and unrefined unwrought copper
        "q_tf_questions": 1,
        "key_countries": ["USA", "CHN"],
        "description": "Copper trade flows",
    },
    "Germanium": {
        "hs_codes": ["811292"],  # Shared with Gallium
        "q_tf_questions": 0,  # Not in Q-TF sub-domain per methodology
        "key_countries": ["USA", "CHN"],
        "description": "Germanium trade flows (2023 export controls)",
    },
    "Other": {
        "hs_codes": [],  # Mn, Ti, PGM, W - to be specified
        "q_tf_questions": 1,
        "key_countries": ["USA", "CHN"],
        "description": "Other CMM trade flows",
    },
}

# Key country pairs based on methodology examples and supply chain relationships
KEY_COUNTRY_PAIRS = [
    ("USA", "CHN"),  # Primary bilateral relationship
    ("CHN", "USA"),  # Reverse direction
    ("USA", "ALL"),  # USA imports from all partners
    ("CHN", "ALL"),  # China exports to all partners
    ("AUS", "CHN"),  # Australia exports to China (lithium)
    ("COD", "CHN"),  # DRC exports to China (cobalt)
    ("IDN", "CHN"),  # Indonesia exports to China (nickel)
]

# Years to query (covers both Stratum A and Stratum B requirements)
YEARS = [2020, 2021, 2022, 2023, 2024]


class GoldQADataCollector:
    """Collect UN Comtrade data for Gold Q&A methodology requirements."""

    def __init__(self, api_key: str | None = None, output_dir: str = "gold_qa_data"):
        """
        Initialize data collector.

        Args:
            api_key: UN Comtrade API key (or set UN_COMTRADE_API_KEY env var)
            output_dir: Directory to save collected data
        """
        self.query = ComtradeQuery(api_key=api_key)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Track queries to avoid duplicates
        self.query_log = []
        self.collected_data = {}

    def _load_existing_data(self, commodity_name: str) -> pd.DataFrame:
        """Load existing data for a commodity if it exists."""
        filename = f"{commodity_name.lower().replace(' ', '_')}_trade_data.csv"
        filepath = self.output_dir / filename

        if filepath.exists():
            try:
                df = pd.read_csv(filepath)
                return df
            except (OSError, ValueError) as e:
                print(f"  Warning: Could not load existing data: {e}")
                return pd.DataFrame()
        return pd.DataFrame()

    def _check_data_exists(
        self,
        existing_df: pd.DataFrame,
        hs_code: str,
        reporter: str,
        partner: str,
        year: int,
        flow_code: str,
    ) -> bool:
        """Check if data already exists for this specific query."""
        if existing_df.empty:
            return False

        # Convert country codes
        reporter_code = COUNTRY_CODES.get(reporter, reporter)
        partner_code = COUNTRY_CODES.get(partner, partner)

        # Check if we have data for this combination
        mask = (
            (existing_df["cmdCode"].astype(str) == str(hs_code))
            & (existing_df["reporterCode"].astype(str) == str(reporter_code))
            & (existing_df["partnerCode"].astype(str) == str(partner_code))
            & (existing_df["period"].astype(str) == str(year))
            & (existing_df["flowCode"] == flow_code)
        )

        return mask.any()

    def pull_commodity_trade_data(
        self,
        commodity_name: str,
        hs_codes: list[str],
        countries: list[tuple[str, str]],
        years: list[int],
        trade_flow: str = "both",
    ) -> dict:
        """
        Pull trade data for a commodity across multiple HS codes and country pairs.
        Skips data that already exists in the output directory.

        Args:
            commodity_name: Name of commodity (e.g., 'Cobalt')
            hs_codes: list of HS codes for this commodity
            countries: list of (reporter, partner) tuples
            years: list of years to query
            trade_flow: 'import', 'export', or 'both'

        Returns:
            Dictionary with collected data and metadata
        """
        print(f"\n{'=' * 80}")
        print(f"Collecting data for: {commodity_name}")
        print(f"HS Codes: {hs_codes}")
        print(f"Country pairs: {countries}")
        print(f"Years: {years}")
        print(f"{'=' * 80}\n")

        # Load existing data
        existing_df = self._load_existing_data(commodity_name)
        if not existing_df.empty:
            print(f"  Found existing data: {len(existing_df)} records")

        all_results = []
        query_count = 0
        skipped_count = 0

        # Map flow codes
        flow_map = {"1": "M", "2": "X", "import": "M", "export": "X"}
        flows_to_query = []
        if trade_flow == "both":
            flows_to_query = ["M", "X"]
        elif trade_flow == "import":
            flows_to_query = ["M"]
        elif trade_flow == "export":
            flows_to_query = ["X"]

        for hs_code in hs_codes:
            for reporter, partner in countries:
                for year in years:
                    for flow_code in flows_to_query:
                        # Create query identifier
                        query_id = (
                            f"{commodity_name}_{hs_code}_{reporter}_{partner}_{year}_{flow_code}"
                        )

                        # Skip if already queried in this session
                        if query_id in self.query_log:
                            skipped_count += 1
                            continue

                        # Check if data already exists
                        if self._check_data_exists(
                            existing_df, hs_code, reporter, partner, year, flow_code
                        ):
                            skipped_count += 1
                            continue

                        try:
                            print(
                                f"  Querying: {hs_code} | {reporter} -> {partner} | {year} | {flow_code}"
                            )

                            # Query single flow
                            flow_for_query = "import" if flow_code == "M" else "export"
                            df = self.query.query_trade_data(
                                reporter=reporter,
                                partner=partner,
                                commodity_code=hs_code,
                                year=year,
                                trade_flow=flow_for_query,
                            )

                            if not df.empty:
                                # Filter to the specific flow we want
                                df_filtered = df[df["flowCode"] == flow_code].copy()
                                if not df_filtered.empty:
                                    # Add metadata columns
                                    df_filtered["commodity_name"] = commodity_name
                                    df_filtered["hs_code"] = hs_code
                                    df_filtered["query_year"] = year
                                    all_results.append(df_filtered)
                                    query_count += 1
                                    print(f"    ✓ Retrieved {len(df_filtered)} records")
                                else:
                                    print(f"    ✗ No data for flow {flow_code}")
                            else:
                                print(f"    ✗ No data returned")

                            # Rate limiting: respect API limits (500 calls/day with key)
                            time.sleep(0.5)  # Small delay between queries

                            self.query_log.append(query_id)

                        except (ValueError, KeyError, OSError) as e:
                            print(f"    ✗ Error: {e}")
                            continue

        # Combine with existing data if any
        if all_results:
            new_df = pd.concat(all_results, ignore_index=True)

            # Merge with existing data
            if not existing_df.empty:
                # Combine and remove duplicates
                combined_df = pd.concat([existing_df, new_df], ignore_index=True)
                # Remove duplicates based on key columns
                key_cols = ["cmdCode", "reporterCode", "partnerCode", "period", "flowCode"]
                if all(col in combined_df.columns for col in key_cols):
                    combined_df = combined_df.drop_duplicates(subset=key_cols, keep="first")
            else:
                combined_df = new_df

            # Save to file
            filename = f"{commodity_name.lower().replace(' ', '_')}_trade_data.csv"
            filepath = self.output_dir / filename
            combined_df.to_csv(filepath, index=False)

            new_records = len(new_df) if all_results else 0
            total_records = len(combined_df)
            print(f"\n  ✓ Added {new_records} new records")
            print(f"  ✓ Total records: {total_records} (saved to {filepath})")
            if skipped_count > 0:
                print(f"  ✓ Skipped {skipped_count} queries (data already exists)")

            return {
                "commodity": commodity_name,
                "total_records": total_records,
                "new_records": new_records,
                "filepath": str(filepath),
                "queries_executed": query_count,
                "skipped": skipped_count,
                "dataframe": combined_df,
            }
        else:
            if not existing_df.empty:
                print(f"\n  ✓ No new data needed - {len(existing_df)} records already exist")
                return {
                    "commodity": commodity_name,
                    "total_records": len(existing_df),
                    "new_records": 0,
                    "filepath": str(
                        self.output_dir
                        / f"{commodity_name.lower().replace(' ', '_')}_trade_data.csv"
                    ),
                    "queries_executed": 0,
                    "skipped": skipped_count,
                    "dataframe": existing_df,
                }
            else:
                print(f"\n  ✗ No data collected for {commodity_name}")
                return {
                    "commodity": commodity_name,
                    "total_records": 0,
                    "new_records": 0,
                    "filepath": None,
                    "queries_executed": query_count,
                    "skipped": skipped_count,
                    "dataframe": pd.DataFrame(),
                }

    def pull_all_gold_qa_data(self, use_preview: bool = False):
        """
        Pull all trade flow data required for Gold Q&A methodology.

        Args:
            use_preview: If True, use preview mode (no API key, 500 records max)
        """
        print("\n" + "=" * 80)
        print("UN Comtrade Data Collection for CMM Gold Q&A Methodology")
        print("=" * 80)
        print(f"Output directory: {self.output_dir}")
        print(f"Preview mode: {use_preview}")
        print(f"Years: {YEARS}")
        print("=" * 80)

        summary = []

        # Iterate through commodities with Q-TF questions
        for commodity_name, config in COMMODITY_TRADE_FLOW_REQUIREMENTS.items():
            if config["q_tf_questions"] == 0:
                print(f"\nSkipping {commodity_name}: No Q-TF questions in methodology")
                continue

            hs_codes = config["hs_codes"]
            if not hs_codes:
                print(f"\nSkipping {commodity_name}: No HS codes defined")
                continue

            # Determine country pairs for this commodity
            key_countries = config.get("key_countries", ["USA", "CHN"])
            countries = self._get_country_pairs_for_commodity(key_countries)

            # Pull data
            result = self.pull_commodity_trade_data(
                commodity_name=commodity_name,
                hs_codes=hs_codes,
                countries=countries,
                years=YEARS,
                trade_flow="both",
            )

            summary.append(result)

        # Save summary
        self._save_summary(summary)

        return summary

    def _get_country_pairs_for_commodity(self, key_countries: list[str]) -> list[tuple[str, str]]:
        """
        Generate country pairs for a commodity based on key countries.

        Args:
            key_countries: list of key countries for this commodity

        Returns:
            list of (reporter, partner) tuples
        """
        pairs = []

        # Always include USA-CHN bidirectional
        if "USA" in key_countries and "CHN" in key_countries:
            pairs.extend([("USA", "CHN"), ("CHN", "USA")])

        # Add country-specific pairs
        if "AUS" in key_countries and "CHN" in key_countries:
            pairs.append(("AUS", "CHN"))  # Australia exports to China

        if "COD" in key_countries and "CHN" in key_countries:
            pairs.append(("COD", "CHN"))  # DRC exports to China

        if "IDN" in key_countries and "CHN" in key_countries:
            pairs.append(("IDN", "CHN"))  # Indonesia exports to China

        # Add 'ALL' partner queries for major importers/exporters
        if "USA" in key_countries:
            pairs.append(("USA", "ALL"))  # USA imports from all

        if "CHN" in key_countries:
            pairs.append(("CHN", "ALL"))  # China exports to all

        return list(set(pairs))  # Remove duplicates

    def _save_summary(self, summary: list[dict]):
        """Save collection summary to JSON file."""
        summary_data = {
            "collection_date": datetime.now().isoformat(),
            "methodology_document": "CMM_LLM_Baseline_Gold_QA_Methodology.md",
            "focus": "Trade Flow questions (Q-TF sub-domain)",
            "years_queried": YEARS,
            "commodities": [],
        }

        for item in summary:
            summary_data["commodities"].append(
                {
                    "name": item["commodity"],
                    "total_records": item["total_records"],
                    "filepath": item["filepath"],
                    "queries_executed": item["queries_executed"],
                }
            )

        summary_file = self.output_dir / "collection_summary.json"
        with open(summary_file, "w") as f:
            json.dump(summary_data, f, indent=2)

        print(f"\n{'=' * 80}")
        print("Collection Summary")
        print(f"{'=' * 80}")
        print(f"Total commodities processed: {len(summary)}")
        print(f"Total records collected: {sum([s['total_records'] for s in summary])}")
        print(f"Summary saved to: {summary_file}")
        print(f"{'=' * 80}\n")


def main():
    """Main function for command-line interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Collect UN Comtrade data for CMM Gold Q&A Methodology",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Collect all data (requires API key)
  python pull_gold_qa_data.py --output-dir gold_qa_data
  
  # Preview mode (no API key, limited data)
  python pull_gold_qa_data.py --preview --output-dir gold_qa_data_preview
  
  # Specify custom API key
  python pull_gold_qa_data.py --api-key YOUR_KEY --output-dir gold_qa_data
        """,
    )

    parser.add_argument(
        "--api-key", type=str, help="UN Comtrade API key (or set UN_COMTRADE_API_KEY env var)"
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="gold_qa_data",
        help="Output directory for collected data (default: gold_qa_data)",
    )

    parser.add_argument(
        "--preview",
        action="store_true",
        help="Use preview mode (no API key needed, 500 records max per query)",
    )

    args = parser.parse_args()

    # Initialize collector
    collector = GoldQADataCollector(api_key=args.api_key, output_dir=args.output_dir)

    # Note: Preview mode would need to be passed through the query methods
    # For now, if preview is requested, the user should use preview mode manually
    if args.preview:
        print("\nNote: Preview mode requires modifying the query calls.")
        print("Consider using the main query script with --preview flag for testing.\n")

    # Collect all data
    try:
        summary = collector.pull_all_gold_qa_data(use_preview=args.preview)

        print("\n✓ Data collection complete!")
        print(f"Check {args.output_dir} for results.")

    except KeyboardInterrupt:
        print("\n\nCollection interrupted by user.")
        sys.exit(1)
    except Exception as e:  # noqa: BLE001
        print(f"\n✗ Error during collection: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
