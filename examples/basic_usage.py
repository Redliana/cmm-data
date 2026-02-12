#!/usr/bin/env python3
"""
Basic usage examples for cmm_data package.
"""

import cmm_data

# =============================================================================
# 1. DATA CATALOG
# =============================================================================

print("=" * 60)
print("1. Data Catalog")
print("=" * 60)

# View all available datasets
catalog = cmm_data.get_data_catalog()
print(catalog[['dataset', 'name', 'available']])

# List commodity codes
commodities = cmm_data.list_commodities()
print(f"\nAvailable commodities ({len(commodities)}): {commodities[:5]}...")

# List critical minerals
critical = cmm_data.list_critical_minerals()
print(f"Critical minerals ({len(critical)}): {critical[:5]}...")


# =============================================================================
# 2. USGS COMMODITY DATA
# =============================================================================

print("\n" + "=" * 60)
print("2. USGS Commodity Data")
print("=" * 60)

# Load world production data (convenience function)
lithium_world = cmm_data.load_usgs_commodity("lithi", "world")
print("\nLithium World Production:")
print(lithium_world[['Country', 'Prod_t_est_2022', 'Reserves_t']].head())

# Load salient statistics (convenience function)
lithium_salient = cmm_data.load_usgs_commodity("lithi", "salient")
print("\nLithium U.S. Salient Statistics:")
print(lithium_salient)

# Using the loader class directly
loader = cmm_data.USGSCommodityLoader()

# Get top producers
print("\nTop 5 Cobalt Producers:")
top_cobalt = loader.get_top_producers("cobal", top_n=5)
print(top_cobalt[['Country', 'Prod_t_est_2022']])

# Get commodity name from code
print(f"\n'raree' = {loader.get_commodity_name('raree')}")
print(f"'lithi' = {loader.get_commodity_name('lithi')}")


# =============================================================================
# 3. USGS ORE DEPOSITS
# =============================================================================

print("\n" + "=" * 60)
print("3. USGS Ore Deposits")
print("=" * 60)

ore_loader = cmm_data.USGSOreDepositsLoader()

# List available tables
tables = ore_loader.list_available()
print(f"Available tables: {tables}")

# Load geology data
try:
    geology = ore_loader.load_geology()
    print(f"\nGeology table: {len(geology)} deposits")
    print(f"Columns: {list(geology.columns)[:5]}...")
except Exception as e:
    print(f"Error loading geology: {e}")

# Get REE samples
try:
    ree = ore_loader.get_ree_samples()
    print(f"\nREE samples: {len(ree)} records")
except Exception as e:
    print(f"Error loading REE samples: {e}")


# =============================================================================
# 4. PREPROCESSED CORPUS
# =============================================================================

print("\n" + "=" * 60)
print("4. Preprocessed Corpus")
print("=" * 60)

corpus_loader = cmm_data.PreprocessedCorpusLoader()

try:
    # Get statistics
    stats = corpus_loader.get_corpus_stats()
    print(f"Total documents: {stats.get('total_documents', 'N/A')}")

    # Search
    results = corpus_loader.search("lithium", limit=3)
    print(f"\nSearch results for 'lithium': {len(results)} documents")
except Exception as e:
    print(f"Corpus not available: {e}")


# =============================================================================
# 5. OECD SUPPLY CHAIN
# =============================================================================

print("\n" + "=" * 60)
print("5. OECD Supply Chain Data")
print("=" * 60)

oecd_loader = cmm_data.OECDSupplyChainLoader()

# List available data
available = oecd_loader.list_available()
print(f"Available datasets: {available}")

# Get minerals coverage info
coverage = oecd_loader.get_minerals_coverage()
for name, info in coverage.items():
    print(f"\n{name}:")
    print(f"  {info['description']}")

# Get PDF reports
try:
    pdfs = oecd_loader.get_export_restrictions_reports()
    print(f"\nExport Restrictions PDFs: {len(pdfs)} files")
    for pdf in pdfs[:3]:
        print(f"  - {pdf.name}")
except Exception as e:
    print(f"Error: {e}")


# =============================================================================
# 6. CROSS-DATASET SEARCH
# =============================================================================

print("\n" + "=" * 60)
print("6. Cross-Dataset Search")
print("=" * 60)

from cmm_data.catalog import search_all_datasets

results = search_all_datasets("cobalt")
print(f"Search results for 'cobalt': {len(results)} matches")
print(results)


# =============================================================================
# 7. CONFIGURATION
# =============================================================================

print("\n" + "=" * 60)
print("7. Configuration")
print("=" * 60)

config = cmm_data.get_config()
print(f"Data root: {config.data_root}")
print(f"Cache enabled: {config.cache_enabled}")

# Validate what's available
status = config.validate()
print("\nDataset availability:")
for name, available in status.items():
    print(f"  {'[OK]' if available else '[--]'} {name}")


print("\n" + "=" * 60)
print("Done!")
print("=" * 60)
