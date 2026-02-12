#!/usr/bin/env python3
"""
Visualization examples for cmm_data package.

Requires: pip install cmm-data[viz]
"""

from __future__ import annotations

import cmm_data

# Check for matplotlib
try:
    import matplotlib.pyplot as plt

    VIZ_AVAILABLE = True
except ImportError:
    print("Visualization requires matplotlib.")
    print("Install with: pip install cmm-data[viz]")
    VIZ_AVAILABLE = False
    exit(1)


def example_world_production():
    """Plot world production bar chart."""
    from cmm_data.visualizations.commodity import plot_world_production

    print("Generating: World Production Charts")

    # Lithium
    df = cmm_data.load_usgs_commodity("lithi", "world")
    fig = plot_world_production(df, "Lithium", top_n=8)
    fig.savefig("lithium_production.png", dpi=150, bbox_inches="tight")
    print("  Saved: lithium_production.png")

    # Cobalt
    df = cmm_data.load_usgs_commodity("cobal", "world")
    fig = plot_world_production(df, "Cobalt", top_n=8)
    fig.savefig("cobalt_production.png", dpi=150, bbox_inches="tight")
    print("  Saved: cobalt_production.png")

    # Rare Earths
    df = cmm_data.load_usgs_commodity("raree", "world")
    fig = plot_world_production(df, "Rare Earths", top_n=8)
    fig.savefig("rare_earths_production.png", dpi=150, bbox_inches="tight")
    print("  Saved: rare_earths_production.png")

    plt.close("all")


def example_time_series():
    """Plot time series charts."""
    from cmm_data.visualizations.commodity import plot_production_timeseries

    print("\nGenerating: Time Series Charts")

    # Lithium
    df = cmm_data.load_usgs_commodity("lithi", "salient")
    fig = plot_production_timeseries(df, "Lithium")
    fig.savefig("lithium_timeseries.png", dpi=150, bbox_inches="tight")
    print("  Saved: lithium_timeseries.png")

    # Cobalt
    df = cmm_data.load_usgs_commodity("cobal", "salient")
    fig = plot_production_timeseries(df, "Cobalt")
    fig.savefig("cobalt_timeseries.png", dpi=150, bbox_inches="tight")
    print("  Saved: cobalt_timeseries.png")

    plt.close("all")


def example_import_reliance():
    """Plot import reliance charts."""
    from cmm_data.visualizations.commodity import plot_import_reliance

    print("\nGenerating: Import Reliance Charts")

    for code, name in [("cobal", "Cobalt"), ("lithi", "Lithium"), ("raree", "Rare Earths")]:
        try:
            df = cmm_data.load_usgs_commodity(code, "salient")
            fig = plot_import_reliance(df, name)
            filename = f"{code}_import_reliance.png"
            fig.savefig(filename, dpi=150, bbox_inches="tight")
            print(f"  Saved: {filename}")
        except (OSError, ValueError) as e:
            print(f"  Error for {name}: {e}")

    plt.close("all")


def example_critical_minerals_comparison():
    """Compare multiple critical minerals."""
    from cmm_data.visualizations.timeseries import plot_critical_minerals_comparison

    print("\nGenerating: Critical Minerals Comparison")

    fig = plot_critical_minerals_comparison(metric="Imports_t", top_n=12)
    fig.savefig("critical_minerals_imports.png", dpi=150, bbox_inches="tight")
    print("  Saved: critical_minerals_imports.png")

    plt.close("all")


def example_custom_chart():
    """Create a custom chart combining multiple commodities."""
    print("\nGenerating: Custom Multi-Commodity Chart")

    loader = cmm_data.USGSCommodityLoader()

    # Get top producer for multiple critical minerals
    minerals = ["lithi", "cobal", "nicke", "graph", "raree"]
    data = []

    for code in minerals:
        try:
            top = loader.get_top_producers(code, top_n=1)
            if not top.empty:
                row = top.iloc[0]
                prod = row.get("Prod_t_est_2022_clean", row.get("Prod_t_est_2022", 0))
                data.append(
                    {
                        "mineral": loader.get_commodity_name(code),
                        "top_producer": row["Country"],
                        "production": prod if isinstance(prod, (int, float)) else 0,
                    }
                )
        except (OSError, ValueError):
            continue

    if data:
        import pandas as pd

        df = pd.DataFrame(data)

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(df["mineral"], df["production"], color="steelblue")

        # Add country labels on bars
        for bar, country in zip(bars, df["top_producer"]):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                country,
                ha="center",
                va="bottom",
                fontsize=9,
                rotation=45,
            )

        ax.set_xlabel("Mineral")
        ax.set_ylabel("Production (metric tons)")
        ax.set_title("Top Producer by Critical Mineral (2022)")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        fig.savefig("top_producers_comparison.png", dpi=150, bbox_inches="tight")
        print("  Saved: top_producers_comparison.png")

    plt.close("all")


def main():
    print("=" * 60)
    print(" CMM Data Visualization Examples")
    print("=" * 60)

    example_world_production()
    example_time_series()
    example_import_reliance()
    example_critical_minerals_comparison()
    example_custom_chart()

    print("\n" + "=" * 60)
    print(" All visualizations generated!")
    print("=" * 60)


if __name__ == "__main__":
    main()
