# Finding 2022 USGS MCS Individual Commodity Item IDs

For 2022 and earlier years, USGS MCS data is organized as individual commodity catalog items. You need to find the ScienceBase catalog item ID for each CMM commodity.

## Steps to Find Item IDs

1. **Visit the 2022 MCS Data Release:**
   - URL: https://www.sciencebase.gov/catalog/item/6197ccbed34eb622f692ee1c

2. **Browse Child Items:**
   - The page shows individual commodity data releases
   - Look for commodities like:
     - LITHIUM
     - COBALT
     - RARE EARTHS
     - GRAPHITE
     - GALLIUM
     - GERMANIUM
     - NICKEL
     - COPPER
     - MANGANESE
     - TITANIUM
     - TUNGSTEN
     - PLATINUM
     - PALLADIUM

3. **Extract Item IDs:**
   - Click on each commodity item
   - The item ID is in the URL: `https://www.sciencebase.gov/catalog/item/{ITEM_ID}`
   - Copy the 24-character hex string (e.g., `6197ccbed34eb622f692ee1c`)

4. **Create Item IDs File:**
   Create a JSON file (`2022_commodity_ids.json`) with this format:

```json
{
  "RARE EARTHS": {
    "item_id": "YOUR_ITEM_ID_HERE",
    "cmm_categories": ["Heavy REE", "Light REE"]
  },
  "COBALT": {
    "item_id": "YOUR_ITEM_ID_HERE",
    "cmm_categories": ["Cobalt"]
  },
  "LITHIUM": {
    "item_id": "YOUR_ITEM_ID_HERE",
    "cmm_categories": ["Lithium"]
  },
  "GALLIUM": {
    "item_id": "YOUR_ITEM_ID_HERE",
    "cmm_categories": ["Gallium"]
  },
  "GRAPHITE": {
    "item_id": "YOUR_ITEM_ID_HERE",
    "cmm_categories": ["Graphite"]
  },
  "NICKEL": {
    "item_id": "YOUR_ITEM_ID_HERE",
    "cmm_categories": ["Nickel"]
  },
  "COPPER": {
    "item_id": "YOUR_ITEM_ID_HERE",
    "cmm_categories": ["Copper"]
  },
  "GERMANIUM": {
    "item_id": "YOUR_ITEM_ID_HERE",
    "cmm_categories": ["Germanium"]
  },
  "MANGANESE": {
    "item_id": "YOUR_ITEM_ID_HERE",
    "cmm_categories": ["Manganese"]
  },
  "TITANIUM": {
    "item_id": "YOUR_ITEM_ID_HERE",
    "cmm_categories": ["Titanium"]
  },
  "TUNGSTEN": {
    "item_id": "YOUR_ITEM_ID_HERE",
    "cmm_categories": ["Tungsten"]
  },
  "PLATINUM": {
    "item_id": "YOUR_ITEM_ID_HERE",
    "cmm_categories": ["Platinum Group Metals"]
  },
  "PALLADIUM": {
    "item_id": "YOUR_ITEM_ID_HERE",
    "cmm_categories": ["Platinum Group Metals"]
  }
}
```

5. **Run the Download Script:**
   ```bash
   python3 download_usgs_mcs_2022_manual.py --item-ids-file 2022_commodity_ids.json
   ```

## Alternative: Update Script Directly

You can also edit `download_usgs_mcs_2022_manual.py` and update the `COMMODITY_ITEM_IDS` dictionary directly with the item IDs you find.

## Notes

- The 2022 release has ~87 individual commodity items
- Each commodity item typically has 1-2 CSV files (salient statistics, world production)
- The script will automatically download all CSV files from each commodity item
- Files are saved to: `usgs_mcs_data/2022/individual_commodities/`

