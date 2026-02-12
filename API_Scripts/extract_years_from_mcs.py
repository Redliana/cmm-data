"""
Extract data for specific years from USGS MCS releases.

Since MCS releases contain 5 years of historical data, we can extract
2020 and 2021 data from the 2022, 2023, and 2024 releases.
"""

import pandas as pd
from pathlib import Path
from typing import List, Dict
import json


def extract_years_from_release(release_year: int, target_years: List[int], output_dir: Path):
    """
    Extract data for target years from a release.

    Args:
        release_year: Year of the MCS release (e.g., 2022)
        target_years: Years to extract (e.g., [2020, 2021])
        output_dir: Output directory for extracted data
    """
    print(f"\nExtracting {target_years} data from {release_year} release...")
    print("=" * 80)

    # Find data files
    if release_year == 2022:
        data_dir = Path(f"usgs_mcs_data/{release_year}/individual_commodities")
    else:
        data_dir = Path(f"usgs_mcs_data/cmm_extracted/{release_year}")

    if not data_dir.exists():
        print(f"  ✗ Data directory not found: {data_dir}")
        return {}

    # Find all CSV files
    csv_files = list(data_dir.glob("*.csv"))
    print(f"  Found {len(csv_files)} CSV files")

    extracted = {}

    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)

            if "Year" not in df.columns:
                continue

            # Filter for target years
            df_filtered = df[df["Year"].isin(target_years)].copy()

            if not df_filtered.empty:
                # Determine commodity name from filename
                filename = csv_file.stem
                # Remove year prefix if present
                if filename.startswith(f"mcs{release_year}"):
                    commodity_part = filename.replace(f"mcs{release_year}-", "").split("_")[0]
                else:
                    commodity_part = filename.split("_")[0]

                # Create output filename
                file_type = "salient" if "salient" in filename else "world"
                output_filename = f"{commodity_part}_{file_type}_{release_year}_release.csv"

                # Ensure output directory exists
                output_dir.mkdir(parents=True, exist_ok=True)
                output_path = output_dir / output_filename
                df_filtered.to_csv(output_path, index=False)

                if commodity_part not in extracted:
                    extracted[commodity_part] = {}
                extracted[commodity_part][file_type] = {
                    "file": str(output_path),
                    "rows": len(df_filtered),
                    "years": sorted(df_filtered["Year"].unique().tolist()),
                }

                print(f"  ✓ {commodity_part} {file_type}: {len(df_filtered)} rows")

        except Exception as e:
            print(f"  ✗ Error processing {csv_file.name}: {e}")
            continue

    return extracted


def main():
    """Extract 2020 and 2021 data from available releases."""
    import argparse

    parser = argparse.ArgumentParser(description="Extract specific years from USGS MCS releases")
    parser.add_argument(
        "--target-years",
        type=int,
        nargs="+",
        default=[2020, 2021],
        help="Years to extract (default: 2020 2021)",
    )
    parser.add_argument(
        "--release-years",
        type=int,
        nargs="+",
        default=[2022, 2023, 2024],
        help="Release years to extract from (default: 2022 2023 2024)",
    )
    parser.add_argument(
        "--output-dir", type=str, default="usgs_mcs_data/extracted_years", help="Output directory"
    )

    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    all_extracted = {}

    for release_year in args.release_years:
        extracted = extract_years_from_release(
            release_year, args.target_years, output_dir / str(release_year)
        )
        all_extracted[release_year] = extracted

    # Save summary
    summary_file = output_dir / "extraction_summary.json"
    with open(summary_file, "w") as f:
        json.dump(all_extracted, f, indent=2)

    print(f"\n{'=' * 80}")
    print("Extraction Summary")
    print(f"{'=' * 80}")
    print(f"Target years: {args.target_years}")
    print(f"Release years processed: {args.release_years}")
    print(f"Output directory: {output_dir}")
    print(f"Summary saved to: {summary_file}")
    print(f"{'=' * 80}\n")


if __name__ == "__main__":
    main()
