# VHS Tape file for recording cmm_data demo GIF
# Install: brew install vhs
# Run: vhs demo.tape
# Output: demo.gif

Output demo.gif

Set FontSize 14
Set Width 900
Set Height 600
Set Theme "Dracula"
Set Padding 20
Set TypingSpeed 50ms

# Title
Type "# CMM Data - Demo"
Enter
Sleep 1s

# Start Python
Type "python3"
Enter
Sleep 500ms

# Import
Type "import cmm_data"
Enter
Sleep 500ms

# Version
Type 'print(f"Version: {cmm_data.__version__}")'
Enter
Sleep 1s

# Get catalog
Type "catalog = cmm_data.get_data_catalog()"
Enter
Sleep 300ms

Type "print(catalog)"
Enter
Sleep 2s

# List commodities
Type "commodities = cmm_data.list_commodities()"
Enter
Sleep 300ms

Type 'print(f"Total commodities: {len(commodities)}")'
Enter
Sleep 1s

# Critical minerals
Type "critical = cmm_data.list_critical_minerals()"
Enter
Sleep 300ms

Type 'print(f"Critical minerals: {len(critical)}")'
Enter
Sleep 300ms

Type "print(critical[:10])"
Enter
Sleep 2s

# Load data
Type 'df = cmm_data.load_usgs_commodity("lithi", "world")'
Enter
Sleep 500ms

Type "df[['Country', 'Prod_t_est_2022']].head(5)"
Enter
Sleep 3s

# Loader example
Type "loader = cmm_data.USGSCommodityLoader()"
Enter
Sleep 300ms

Type 'loader.get_commodity_name("lithi")'
Enter
Sleep 1s

Type 'loader.get_commodity_name("cobal")'
Enter
Sleep 1s

# Exit
Type "exit()"
Enter
Sleep 500ms

Type "# Done!"
Enter
Sleep 2s
