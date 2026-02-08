"""
USGS MCS Individual Commodity Finder and Downloader

Uses sciencebasepy to automatically find CMM commodity item IDs for pre-2023 years
and download the data.

Based on: https://code.usgs.gov/sas/sdm/sciencebasepy
"""

import os
import sys
import json
import requests
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import time

try:
    from sciencebasepy import SbSession
except ImportError:
    print("Error: sciencebasepy not installed. Install with: pip install sciencebasepy")
    sys.exit(1)

# CMM Commodities from methodology (Section 2.2)
CMM_COMMODITIES = {
    'RARE EARTHS': {
        'keywords': ['RARE EARTH', 'REE'],
        'cmm_categories': ['Heavy REE', 'Light REE']
    },
    'COBALT': {
        'keywords': ['COBALT'],
        'cmm_categories': ['Cobalt']
    },
    'LITHIUM': {
        'keywords': ['LITHIUM'],
        'cmm_categories': ['Lithium']
    },
    'GALLIUM': {
        'keywords': ['GALLIUM'],
        'cmm_categories': ['Gallium']
    },
    'GRAPHITE': {
        'keywords': ['GRAPHITE'],
        'cmm_categories': ['Graphite']
    },
    'NICKEL': {
        'keywords': ['NICKEL'],
        'cmm_categories': ['Nickel']
    },
    'COPPER': {
        'keywords': ['COPPER'],
        'cmm_categories': ['Copper']
    },
    'GERMANIUM': {
        'keywords': ['GERMANIUM'],
        'cmm_categories': ['Germanium']
    },
    'MANGANESE': {
        'keywords': ['MANGANESE'],
        'cmm_categories': ['Manganese']
    },
    'TITANIUM': {
        'keywords': ['TITANIUM'],
        'cmm_categories': ['Titanium']
    },
    'TUNGSTEN': {
        'keywords': ['TUNGSTEN'],
        'cmm_categories': ['Tungsten']
    },
    'PLATINUM': {
        'keywords': ['PLATINUM', 'PLATINUM-GROUP'],
        'cmm_categories': ['Platinum Group Metals']
    },
    'PALLADIUM': {
        'keywords': ['PALLADIUM', 'PLATINUM-GROUP'],
        'cmm_categories': ['Platinum Group Metals']
    },
}


class USGSMCSAutoDownloader:
    """Automatically find and download CMM commodities using sciencebasepy."""
    
    def __init__(self, output_dir: str = 'usgs_mcs_data'):
        """
        Initialize downloader.
        
        Args:
            output_dir: Directory to save downloaded data
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.sb = SbSession()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; CMM-Data-Collector/1.0)'
        })
    
    def find_cmm_commodities(self, release_id: str, year: int) -> Dict[str, Dict]:
        """
        Find CMM commodity item IDs from a release catalog.
        
        Args:
            release_id: ScienceBase catalog item ID for the year's data release
            year: Year (for matching in titles)
        
        Returns:
            Dictionary mapping commodity names to item info
        """
        print(f"\nFinding CMM commodities in {year} release...")
        print("="*80)
        
        # Get child item IDs
        print(f"Getting child items from catalog {release_id}...")
        child_ids = self.sb.get_child_ids(release_id)
        print(f"Found {len(child_ids)} child items")
        
        # Get full item info for each child
        print("Fetching child item details...")
        children = []
        for i, child_id in enumerate(child_ids, 1):
            try:
                child = self.sb.get_item(child_id)
                children.append(child)
                if i % 20 == 0:
                    print(f"  Fetched {i}/{len(child_ids)} items...")
            except Exception as e:
                print(f"  Warning: Error fetching {child_id}: {e}")
                continue
        
        print(f"Retrieved {len(children)} child items\n")
        
        # Match CMM commodities
        found = {}
        for child in children:
            title = child.get('title', '').upper()
            
            # Check if this is a data release for the correct year
            if str(year) not in title or 'DATA RELEASE' not in title:
                continue
            
            # Check against CMM commodities
            for commodity_name, info in CMM_COMMODITIES.items():
                keywords = info['keywords']
                for keyword in keywords:
                    if keyword in title:
                        # Found a match
                        if commodity_name not in found:
                            found[commodity_name] = {
                                'item_id': child.get('id'),
                                'title': child.get('title'),
                                'cmm_categories': info['cmm_categories']
                            }
                            print(f"  ✓ {commodity_name}: {child.get('title')}")
                            print(f"    ID: {child.get('id')}")
                        break
        
        print(f"\nFound {len(found)}/{len(CMM_COMMODITIES)} CMM commodities")
        return found
    
    def download_commodity_files(self, item_id: str, commodity_name: str, year: int) -> List[Path]:
        """
        Download all CSV files from a commodity catalog item.
        
        Args:
            item_id: ScienceBase catalog item ID
            commodity_name: Name of the commodity
            year: Year of the data
        
        Returns:
            List of downloaded file paths
        """
        item_info = self.sb.get_item(item_id)
        if not item_info:
            print(f"  ✗ Could not fetch item {item_id}")
            return []
        
        year_dir = self.output_dir / str(year) / 'individual_commodities'
        year_dir.mkdir(parents=True, exist_ok=True)
        
        downloaded_files = []
        
        # Get attached files
        if 'files' in item_info:
            for file_info in item_info['files']:
                url = file_info.get('url') or file_info.get('downloadUri') or file_info.get('downloadURL')
                if not url:
                    # Try constructing URL
                    filename = file_info.get('name', '')
                    url = f"https://www.sciencebase.gov/catalog/file/get/{item_id}?name={filename}"
                
                filename = file_info.get('name', url.split('/')[-1].split('?')[0])
                
                # Only download CSV files
                if filename.endswith('.csv'):
                    filepath = year_dir / f"{commodity_name.lower().replace(' ', '_')}_{filename}"
                    
                    try:
                        print(f"    Downloading: {filename}")
                        response = self.session.get(url, stream=True, timeout=60)
                        response.raise_for_status()
                        
                        with open(filepath, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                f.write(chunk)
                        
                        downloaded_files.append(filepath)
                        print(f"      ✓ Downloaded {filepath.stat().st_size / 1024:.1f} KB")
                        time.sleep(0.5)  # Rate limiting
                    except Exception as e:
                        print(f"      ✗ Error: {e}")
        
        return downloaded_files
    
    def download_year(self, release_id: str, year: int) -> Dict:
        """
        Find and download all CMM commodities for a year.
        
        Args:
            release_id: ScienceBase catalog item ID for the year's data release
            year: Year to download
        
        Returns:
            Summary of downloads
        """
        print(f"\n{'='*80}")
        print(f"USGS MCS {year} Individual Commodity Data")
        print(f"{'='*80}")
        
        # Find commodities
        commodities = self.find_cmm_commodities(release_id, year)
        
        if not commodities:
            print(f"\n⚠ No CMM commodities found for {year}")
            return {
                'year': year,
                'status': 'no_commodities_found',
                'commodities_downloaded': {},
                'total_files': 0
            }
        
        # Download each commodity
        summary = {
            'year': year,
            'commodities_downloaded': {},
            'total_files': 0,
            'status': 'incomplete'
        }
        
        print(f"\n{'='*80}")
        print(f"Downloading {len(commodities)} commodities...")
        print(f"{'='*80}\n")
        
        for commodity_name, info in commodities.items():
            print(f"{commodity_name} (ID: {info['item_id']}):")
            files = self.download_commodity_files(
                info['item_id'],
                commodity_name,
                year
            )
            
            if files:
                cmm_categories = info['cmm_categories']
                for cmm_cat in cmm_categories:
                    if cmm_cat not in summary['commodities_downloaded']:
                        summary['commodities_downloaded'][cmm_cat] = []
                    summary['commodities_downloaded'][cmm_cat].extend([str(f) for f in files])
                
                summary['total_files'] += len(files)
                print(f"  ✓ Downloaded {len(files)} files\n")
            else:
                print(f"  ✗ No files downloaded\n")
        
        summary['status'] = 'complete' if summary['total_files'] > 0 else 'failed'
        
        # Save summary
        summary_file = self.output_dir / f'{year}_auto_download_summary.json'
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Save commodity IDs for future reference
        ids_file = self.output_dir / f'{year}_commodity_ids.json'
        ids_data = {
            commodity: {
                'item_id': info['item_id'],
                'cmm_categories': info['cmm_categories']
            }
            for commodity, info in commodities.items()
        }
        with open(ids_file, 'w') as f:
            json.dump(ids_data, f, indent=2)
        
        print(f"{'='*80}")
        print("Download Summary")
        print(f"{'='*80}")
        print(f"Year: {summary['year']}")
        print(f"Status: {summary['status']}")
        print(f"Total files: {summary['total_files']}")
        print(f"Commodities: {len(summary['commodities_downloaded'])}")
        print(f"Summary saved to: {summary_file}")
        print(f"Item IDs saved to: {ids_file}")
        print(f"{'='*80}\n")
        
        return summary


def main():
    """Main function for command-line interface."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Automatically find and download USGS MCS individual commodity data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download 2022 data
  python find_and_download_usgs_mcs.py --year 2022 --release-id 6197ccbed34eb622f692ee1c
  
  # Download 2021 data (once you have the release ID)
  python find_and_download_usgs_mcs.py --year 2021 --release-id <RELEASE_ID>
        """
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='usgs_mcs_data',
        help='Output directory for downloaded data'
    )
    
    parser.add_argument(
        '--year',
        type=int,
        required=True,
        help='Year to download (2020-2022)'
    )
    
    parser.add_argument(
        '--release-id',
        type=str,
        required=True,
        help='ScienceBase catalog item ID for the year data release'
    )
    
    args = parser.parse_args()
    
    downloader = USGSMCSAutoDownloader(output_dir=args.output_dir)
    summary = downloader.download_year(args.release_id, args.year)


if __name__ == '__main__':
    main()

