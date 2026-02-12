#!/usr/bin/env python3
"""
CMM Data Quick Start Script

Demonstrates basic usage of the cmm_data package.
Run after installation: python scripts/quickstart.py
"""

import cmm_data


def main():
    print("=" * 60)
    print(" CMM Data Quick Start")
    print("=" * 60)

    # Show version
    print(f"\nVersion: {cmm_data.__version__}")

    # 1. Data Catalog
    print("\n" + "-" * 40)
    print("1. Available Datasets")
    print("-" * 40)

    catalog = cmm_data.get_data_catalog()
    for _, row in catalog.iterrows():
        status = "[OK]" if row['available'] else "[--]"
        print(f"  {status} {row['dataset']}: {row['name']}")

    # 2. List Commodities
    print("\n" + "-" * 40)
    print("2. Commodity Codes")
    print("-" * 40)

    commodities = cmm_data.list_commodities()
    print(f"  Total commodities: {len(commodities)}")
    print(f"  Examples: {', '.join(commodities[:10])}...")

    # 3. Critical Minerals
    print("\n" + "-" * 40)
    print("3. DOE Critical Minerals")
    print("-" * 40)

    critical = cmm_data.list_critical_minerals()
    print(f"  Count: {len(critical)}")
    print(f"  List: {', '.join(critical)}")

    # 4. Load Sample Data
    print("\n" + "-" * 40)
    print("4. Sample Data: Lithium World Production")
    print("-" * 40)

    try:
        df = cmm_data.load_usgs_commodity("lithi", "world")
        print(f"\n  Columns: {list(df.columns)}")
        print(f"\n  Data ({len(df)} rows):")
        print(df[['Country', 'Prod_t_est_2022', 'Reserves_t']].head(10).to_string(index=False))
    except Exception as e:
        print(f"  [ERROR] {e}")

    # 5. Top Producers
    print("\n" + "-" * 40)
    print("5. Top Lithium Producers")
    print("-" * 40)

    try:
        loader = cmm_data.USGSCommodityLoader()
        top = loader.get_top_producers("lithi", top_n=5)
        print("\n  Rank  Country         Production (t)")
        print("  " + "-" * 40)
        for i, (_, row) in enumerate(top.iterrows(), 1):
            country = row['Country'][:15]
            prod = row.get('Prod_t_est_2022_clean', row.get('Prod_t_est_2022', 'N/A'))
            if isinstance(prod, (int, float)):
                print(f"  {i:4d}  {country:15s}  {prod:>15,.0f}")
            else:
                print(f"  {i:4d}  {country:15s}  {str(prod):>15s}")
    except Exception as e:
        print(f"  [ERROR] {e}")

    # 6. Salient Statistics
    print("\n" + "-" * 40)
    print("6. U.S. Lithium Statistics (Time Series)")
    print("-" * 40)

    try:
        df = cmm_data.load_usgs_commodity("lithi", "salient")
        print(f"\n  Years: {df['Year'].min()} - {df['Year'].max()}")
        print(f"\n  Latest data ({df['Year'].max()}):")
        latest = df.iloc[-1]
        print(f"    Imports: {latest.get('Imports_t', 'N/A')} t")
        print(f"    Exports: {latest.get('Exports_t', 'N/A')} t")
        print(f"    Net Import Reliance: {latest.get('NIR_pct', 'N/A')}")
    except Exception as e:
        print(f"  [ERROR] {e}")

    print("\n" + "=" * 60)
    print(" Quick Start Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("  - Run the tutorial notebook: examples/cmm_data_tutorial.ipynb")
    print("  - Read the documentation: README.md")
    print("  - Explore the API: help(cmm_data)")


if __name__ == "__main__":
    main()
