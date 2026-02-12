#!/usr/bin/env python3
"""
Demo script for recording a GIF/video of cmm_data usage.

This script demonstrates key features of the cmm_data package with
visual output suitable for recording with tools like:
- asciinema (https://asciinema.org/)
- terminalizer (https://terminalizer.com/)
- VHS (https://github.com/charmbracelet/vhs)

Usage:
    # Record with asciinema
    asciinema rec demo.cast -c "python scripts/demo_recording.py"

    # Convert to GIF with agg
    agg demo.cast demo.gif

    # Or record with VHS (create demo.tape first)
    vhs demo.tape

    # Or just run directly
    python scripts/demo_recording.py
"""

from __future__ import annotations

import sys
import time


# Typing effect for commands
def type_command(text, delay=0.03):
    """Simulate typing a command."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def print_slow(text, delay=0.01):
    """Print text with slight delay for readability."""
    for line in text.split("\n"):
        print(line)
        time.sleep(delay)


def section_pause():
    """Pause between sections."""
    time.sleep(1.5)


def main():
    print("\033[1;36m" + "=" * 60 + "\033[0m")
    print("\033[1;36m  CMM Data - Critical Minerals Modeling Data Access Library\033[0m")
    print("\033[1;36m" + "=" * 60 + "\033[0m")
    print()
    time.sleep(2)

    # Import
    print("\033[1;33m>>> \033[0m", end="")
    type_command("import cmm_data")
    import cmm_data

    print("\033[32m✓ Package imported successfully\033[0m")
    section_pause()

    # Version
    print("\033[1;33m>>> \033[0m", end="")
    type_command(f'print(f"Version: {{cmm_data.__version__}}")')
    print(f"Version: {cmm_data.__version__}")
    section_pause()

    # Data catalog
    print("\n\033[1;35m── Data Catalog ──\033[0m")
    print("\033[1;33m>>> \033[0m", end="")
    type_command("catalog = cmm_data.get_data_catalog()")
    catalog = cmm_data.get_data_catalog()

    print("\033[1;33m>>> \033[0m", end="")
    type_command("print(catalog)")
    print(catalog.to_string())
    section_pause()

    # list commodities
    print("\n\033[1;35m── Available Commodities ──\033[0m")
    print("\033[1;33m>>> \033[0m", end="")
    type_command("commodities = cmm_data.list_commodities()")
    commodities = cmm_data.list_commodities()

    print("\033[1;33m>>> \033[0m", end="")
    type_command(f'print(f"Total commodities: {{len(commodities)}}")')
    print(f"Total commodities: {len(commodities)}")

    print("\033[1;33m>>> \033[0m", end="")
    type_command("print(commodities[:10])")
    print(commodities[:10])
    section_pause()

    # Critical minerals
    print("\n\033[1;35m── Critical Minerals ──\033[0m")
    print("\033[1;33m>>> \033[0m", end="")
    type_command("critical = cmm_data.list_critical_minerals()")
    critical = cmm_data.list_critical_minerals()

    print("\033[1;33m>>> \033[0m", end="")
    type_command(f'print(f"Critical minerals: {{len(critical)}}")')
    print(f"Critical minerals: {len(critical)}")

    print("\033[1;33m>>> \033[0m", end="")
    type_command("print(critical[:10])")
    print(critical[:10])
    section_pause()

    # Load lithium data
    print("\n\033[1;35m── Load Lithium World Production ──\033[0m")
    print("\033[1;33m>>> \033[0m", end="")
    type_command('df = cmm_data.load_usgs_commodity("lithi", "world")')

    try:
        df = cmm_data.load_usgs_commodity("lithi", "world")
        print("\033[1;33m>>> \033[0m", end="")
        type_command("print(df[['Country', 'Prod_t_est_2022', 'Reserves_t']].head(8))")
        print(df[["Country", "Prod_t_est_2022", "Reserves_t"]].head(8).to_string())
    except (OSError, ValueError) as e:
        print(f"\033[33m[Data not available: {e}]\033[0m")
    section_pause()

    # USGS Loader
    print("\n\033[1;35m── USGS Commodity Loader ──\033[0m")
    print("\033[1;33m>>> \033[0m", end="")
    type_command("loader = cmm_data.USGSCommodityLoader()")
    loader = cmm_data.USGSCommodityLoader()

    print("\033[1;33m>>> \033[0m", end="")
    type_command('print(loader.get_commodity_name("lithi"))')
    print(loader.get_commodity_name("lithi"))

    print("\033[1;33m>>> \033[0m", end="")
    type_command('print(loader.get_commodity_name("cobal"))')
    print(loader.get_commodity_name("cobal"))

    print("\033[1;33m>>> \033[0m", end="")
    type_command('print(loader.get_commodity_name("raree"))')
    print(loader.get_commodity_name("raree"))
    section_pause()

    # OECD Loader
    print("\n\033[1;35m── OECD Supply Chain Loader ──\033[0m")
    print("\033[1;33m>>> \033[0m", end="")
    type_command("oecd = cmm_data.OECDSupplyChainLoader()")
    oecd = cmm_data.OECDSupplyChainLoader()

    print("\033[1;33m>>> \033[0m", end="")
    type_command("print(oecd.get_download_urls())")
    urls = oecd.get_download_urls()
    for name, url in urls.items():
        print(f"  {name}: {url[:50]}...")
    section_pause()

    # Configuration
    print("\n\033[1;35m── Configuration ──\033[0m")
    print("\033[1;33m>>> \033[0m", end="")
    type_command("config = cmm_data.get_config()")
    config = cmm_data.get_config()

    print("\033[1;33m>>> \033[0m", end="")
    type_command('print(f"Data root: {config.data_root}")')
    print(f"Data root: {config.data_root}")

    print("\033[1;33m>>> \033[0m", end="")
    type_command('print(f"Cache enabled: {config.cache_enabled}")')
    print(f"Cache enabled: {config.cache_enabled}")
    section_pause()

    # Done
    print("\n" + "=" * 60)
    print("\033[1;32m✓ CMM Data demo complete!\033[0m")
    print("=" * 60)
    print()
    print("For more information:")
    print("  • Documentation: https://pnnl-cmm.github.io/cmm-data/")
    print("  • GitHub: https://github.com/PNNL-CMM/cmm-data")
    print()
    time.sleep(3)


if __name__ == "__main__":
    main()
