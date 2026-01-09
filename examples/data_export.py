#!/usr/bin/env python3
"""
Data export examples for cmm_data package.

Shows how to export CMM data to various formats.
"""

import cmm_data
import pandas as pd
from pathlib import Path


def export_critical_minerals_summary(output_dir: Path):
    """Export summary of all critical minerals to CSV."""
    print("Exporting: Critical Minerals Summary")

    loader = cmm_data.USGSCommodityLoader()
    critical = cmm_data.list_critical_minerals()

    summary_data = []

    for code in critical:
        try:
            # World production
            world = loader.load_world_production(code)
            world_total = world[world['Country'].str.contains('World', case=False, na=False)]

            # Salient statistics
            salient = loader.load_salient_statistics(code)
            latest = salient.iloc[-1] if not salient.empty else {}

            # Top producer
            top = loader.get_top_producers(code, top_n=1)
            top_country = top.iloc[0]['Country'] if not top.empty else 'N/A'

            summary_data.append({
                'commodity_code': code,
                'commodity_name': loader.get_commodity_name(code),
                'top_producer': top_country,
                'world_production_2022': world_total.iloc[0].get('Prod_t_est_2022', 'N/A') if not world_total.empty else 'N/A',
                'world_reserves': world_total.iloc[0].get('Reserves_t', 'N/A') if not world_total.empty else 'N/A',
                'us_imports_2022': latest.get('Imports_t', 'N/A'),
                'us_exports_2022': latest.get('Exports_t', 'N/A'),
                'net_import_reliance': latest.get('NIR_pct', 'N/A'),
            })
        except Exception as e:
            print(f"  Warning: Error processing {code}: {e}")
            continue

    df = pd.DataFrame(summary_data)
    output_file = output_dir / "critical_minerals_summary.csv"
    df.to_csv(output_file, index=False)
    print(f"  Saved: {output_file}")

    return df


def export_world_production_all(output_dir: Path):
    """Export world production data for all commodities."""
    print("\nExporting: World Production (All Commodities)")

    loader = cmm_data.USGSCommodityLoader()
    commodities = loader.list_available()

    all_data = []

    for code in commodities:
        try:
            df = loader.load_world_production(code)
            df['commodity_code'] = code
            df['commodity_name'] = loader.get_commodity_name(code)
            all_data.append(df)
        except Exception:
            continue

    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        output_file = output_dir / "world_production_all.csv"
        combined.to_csv(output_file, index=False)
        print(f"  Saved: {output_file} ({len(combined)} rows)")


def export_salient_statistics_all(output_dir: Path):
    """Export salient statistics for all commodities."""
    print("\nExporting: Salient Statistics (All Commodities)")

    loader = cmm_data.USGSCommodityLoader()
    commodities = loader.list_available()

    all_data = []

    for code in commodities:
        try:
            df = loader.load_salient_statistics(code)
            df['commodity_code'] = code
            df['commodity_name'] = loader.get_commodity_name(code)
            all_data.append(df)
        except Exception:
            continue

    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        output_file = output_dir / "salient_statistics_all.csv"
        combined.to_csv(output_file, index=False)
        print(f"  Saved: {output_file} ({len(combined)} rows)")


def export_ore_deposits(output_dir: Path):
    """Export ore deposits data."""
    print("\nExporting: Ore Deposits Data")

    loader = cmm_data.USGSOreDepositsLoader()

    try:
        # Data dictionary
        data_dict = loader.load_data_dictionary()
        output_file = output_dir / "ore_deposits_data_dictionary.csv"
        data_dict.to_csv(output_file, index=False)
        print(f"  Saved: {output_file}")

        # Geology
        geology = loader.load_geology()
        output_file = output_dir / "ore_deposits_geology.csv"
        geology.to_csv(output_file, index=False)
        print(f"  Saved: {output_file} ({len(geology)} rows)")

    except Exception as e:
        print(f"  Error: {e}")


def export_to_excel(output_dir: Path):
    """Export summary data to Excel workbook."""
    print("\nExporting: Excel Workbook")

    try:
        import openpyxl
    except ImportError:
        print("  Skipped: openpyxl not installed (pip install openpyxl)")
        return

    loader = cmm_data.USGSCommodityLoader()

    output_file = output_dir / "cmm_data_export.xlsx"

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Critical minerals summary
        critical = cmm_data.list_critical_minerals()
        summary_data = []
        for code in critical[:10]:  # First 10 for demo
            try:
                df = loader.load_world_production(code)
                top = df[~df['Country'].str.contains('World|total', case=False, na=False)].head(5)
                top['commodity'] = loader.get_commodity_name(code)
                summary_data.append(top[['commodity', 'Country', 'Prod_t_est_2022', 'Reserves_t']])
            except Exception:
                continue

        if summary_data:
            combined = pd.concat(summary_data, ignore_index=True)
            combined.to_excel(writer, sheet_name='Top Producers', index=False)

        # Commodity list
        commodities_df = pd.DataFrame([
            {'code': c, 'name': loader.get_commodity_name(c), 'is_critical': c in critical}
            for c in loader.list_available()
        ])
        commodities_df.to_excel(writer, sheet_name='Commodities', index=False)

        # Data catalog
        catalog = cmm_data.get_data_catalog()
        catalog.to_excel(writer, sheet_name='Data Catalog', index=False)

    print(f"  Saved: {output_file}")


def main():
    print("=" * 60)
    print(" CMM Data Export Examples")
    print("=" * 60)

    # Create output directory
    output_dir = Path("cmm_exports")
    output_dir.mkdir(exist_ok=True)
    print(f"\nOutput directory: {output_dir.absolute()}")

    # Run exports
    export_critical_minerals_summary(output_dir)
    export_world_production_all(output_dir)
    export_salient_statistics_all(output_dir)
    export_ore_deposits(output_dir)
    export_to_excel(output_dir)

    print("\n" + "=" * 60)
    print(" Export complete!")
    print("=" * 60)
    print(f"\nFiles saved to: {output_dir.absolute()}")


if __name__ == "__main__":
    main()
