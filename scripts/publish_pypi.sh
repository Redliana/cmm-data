#!/bin/bash
# ============================================================================
# CMM Data - Publish to PyPI
# ============================================================================
# This script publishes the cmm_data package to PyPI.
#
# Prerequisites:
#   1. PyPI account (https://pypi.org/account/register/)
#   2. PyPI API token (https://pypi.org/manage/account/token/)
#   3. Store token in ~/.pypirc or use environment variable
#
# Usage:
#   cd /path/to/cmm_data
#   chmod +x scripts/publish_pypi.sh
#   ./scripts/publish_pypi.sh
#
# For Test PyPI first:
#   ./scripts/publish_pypi.sh --test
# ============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo -e "${BLUE}============================================================================${NC}"
echo -e "${BLUE}  CMM Data - Publish to PyPI${NC}"
echo -e "${BLUE}============================================================================${NC}"
echo ""

# Check for --test flag
USE_TEST_PYPI=false
if [[ "$1" == "--test" ]]; then
    USE_TEST_PYPI=true
    echo -e "${YELLOW}Publishing to Test PyPI${NC}"
else
    echo -e "${YELLOW}Publishing to PyPI (production)${NC}"
fi
echo ""

# ============================================================================
# Step 1: Activate virtual environment
# ============================================================================
echo -e "${YELLOW}Step 1: Activating virtual environment...${NC}"
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo -e "${GREEN}✓ Virtual environment activated${NC}"
else
    echo -e "${RED}No virtual environment found. Creating one...${NC}"
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
fi
echo ""

# ============================================================================
# Step 2: Install build tools
# ============================================================================
echo -e "${YELLOW}Step 2: Installing build tools...${NC}"
pip install --upgrade build twine
echo -e "${GREEN}✓ Build tools installed${NC}"
echo ""

# ============================================================================
# Step 3: Clean previous builds
# ============================================================================
echo -e "${YELLOW}Step 3: Cleaning previous builds...${NC}"
rm -rf dist/ build/ src/*.egg-info/
echo -e "${GREEN}✓ Cleaned${NC}"
echo ""

# ============================================================================
# Step 4: Run tests
# ============================================================================
echo -e "${YELLOW}Step 4: Running tests...${NC}"
pip install -e . > /dev/null 2>&1
python scripts/run_all_tests.py
if [ $? -ne 0 ]; then
    echo -e "${RED}Tests failed! Fix issues before publishing.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Tests passed${NC}"
echo ""

# ============================================================================
# Step 5: Build package
# ============================================================================
echo -e "${YELLOW}Step 5: Building package...${NC}"
python -m build
echo -e "${GREEN}✓ Package built${NC}"
echo ""

echo "Built files:"
ls -la dist/
echo ""

# ============================================================================
# Step 6: Check package
# ============================================================================
echo -e "${YELLOW}Step 6: Checking package with twine...${NC}"
twine check dist/*
echo -e "${GREEN}✓ Package check passed${NC}"
echo ""

# ============================================================================
# Step 7: Upload to PyPI
# ============================================================================
echo -e "${YELLOW}Step 7: Uploading to PyPI...${NC}"
echo ""

if [ "$USE_TEST_PYPI" = true ]; then
    echo -e "${BLUE}Uploading to Test PyPI...${NC}"
    echo "You can test installation with:"
    echo "  pip install -i https://test.pypi.org/simple/ cmm-data"
    echo ""
    twine upload --repository testpypi dist/*
    echo ""
    echo -e "${GREEN}✓ Published to Test PyPI!${NC}"
    echo ""
    echo "Install from Test PyPI:"
    echo -e "  ${YELLOW}pip install -i https://test.pypi.org/simple/ cmm-data${NC}"
else
    echo -e "${BLUE}Uploading to PyPI (production)...${NC}"
    echo ""
    read -p "Are you sure you want to publish to production PyPI? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        twine upload dist/*
        echo ""
        echo -e "${GREEN}✓ Published to PyPI!${NC}"
        echo ""
        echo "Install with:"
        echo -e "  ${YELLOW}pip install cmm-data${NC}"
    else
        echo -e "${YELLOW}Aborted.${NC}"
        exit 0
    fi
fi

echo ""
echo -e "${BLUE}============================================================================${NC}"
echo -e "${GREEN}  Publication Complete!${NC}"
echo -e "${BLUE}============================================================================${NC}"
echo ""
echo "Package: cmm-data"
echo "Version: 0.1.0"
echo ""
if [ "$USE_TEST_PYPI" = true ]; then
    echo "Test PyPI: https://test.pypi.org/project/cmm-data/"
else
    echo "PyPI: https://pypi.org/project/cmm-data/"
fi
echo ""
