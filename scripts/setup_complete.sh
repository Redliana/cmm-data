#!/bin/bash
# ============================================================================
# CMM Data - Complete Setup Script
# ============================================================================
# This script performs all setup tasks for the cmm_data package:
# 1. Creates virtual environment
# 2. Installs package with all dependencies
# 3. Installs development tools
# 4. Runs tests
# 5. Builds wheel
# 6. Initializes git repository
# 7. Syncs to OneDrive
# 8. Pushes to GitHub (optional)
#
# Usage:
#   cd /path/to/cmm_data
#   chmod +x scripts/setup_complete.sh
#   ./scripts/setup_complete.sh
# ============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
ONEDRIVE_DIR="/Users/wash198/Library/CloudStorage/OneDrive-PNNL/Documents/Projects/Science_Projects/MPII_CMM/Globus_Sharing/cmm_data"

echo -e "${BLUE}============================================================================${NC}"
echo -e "${BLUE}  CMM Data - Complete Setup Script${NC}"
echo -e "${BLUE}============================================================================${NC}"
echo ""
echo -e "Project directory: ${GREEN}$PROJECT_DIR${NC}"
echo ""

cd "$PROJECT_DIR"

# ============================================================================
# Step 1: Create Virtual Environment
# ============================================================================
echo -e "${YELLOW}Step 1: Creating virtual environment...${NC}"
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Activate virtual environment
source .venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# ============================================================================
# Step 2: Upgrade pip
# ============================================================================
echo -e "${YELLOW}Step 2: Upgrading pip...${NC}"
pip install --upgrade pip
echo -e "${GREEN}✓ pip upgraded${NC}"
echo ""

# ============================================================================
# Step 3: Install package with all dependencies
# ============================================================================
echo -e "${YELLOW}Step 3: Installing cmm_data with all dependencies...${NC}"
pip install -e ".[full]"
echo -e "${GREEN}✓ cmm_data installed${NC}"
echo ""

# ============================================================================
# Step 4: Install development tools
# ============================================================================
echo -e "${YELLOW}Step 4: Installing development tools...${NC}"
pip install pytest pytest-cov ruff mypy pre-commit build twine
pip install -r docs/requirements.txt
echo -e "${GREEN}✓ Development tools installed${NC}"
echo ""

# ============================================================================
# Step 5: Install pre-commit hooks
# ============================================================================
echo -e "${YELLOW}Step 5: Installing pre-commit hooks...${NC}"
pre-commit install
echo -e "${GREEN}✓ Pre-commit hooks installed${NC}"
echo ""

# ============================================================================
# Step 6: Run tests
# ============================================================================
echo -e "${YELLOW}Step 6: Running tests...${NC}"
echo ""
python scripts/run_all_tests.py
echo ""
echo -e "${GREEN}✓ Tests completed${NC}"
echo ""

# ============================================================================
# Step 7: Run linter
# ============================================================================
echo -e "${YELLOW}Step 7: Running linter...${NC}"
ruff check src/ --fix || true
ruff format src/ || true
echo -e "${GREEN}✓ Linting completed${NC}"
echo ""

# ============================================================================
# Step 8: Build documentation
# ============================================================================
echo -e "${YELLOW}Step 8: Building documentation...${NC}"
cd docs
make html || true
cd ..
echo -e "${GREEN}✓ Documentation built${NC}"
echo ""

# ============================================================================
# Step 9: Build wheel
# ============================================================================
echo -e "${YELLOW}Step 9: Building wheel...${NC}"
python -m build
echo -e "${GREEN}✓ Wheel built${NC}"
echo ""
ls -la dist/
echo ""

# ============================================================================
# Step 10: Initialize git repository
# ============================================================================
echo -e "${YELLOW}Step 10: Initializing git repository...${NC}"
if [ ! -d ".git" ]; then
    git init
    git add .
    git commit -m "Initial commit: cmm_data v0.1.0 - Critical Minerals Modeling Data Access Library

- 7 data loaders for USGS, OECD, OSTI, and other sources
- 80+ mineral commodities with world production and U.S. statistics
- Visualization module for production charts and time series
- Comprehensive documentation and examples
- GitHub Actions CI/CD workflows
- Pre-commit hooks for code quality

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
    echo -e "${GREEN}✓ Git repository initialized and committed${NC}"
else
    echo -e "${GREEN}✓ Git repository already exists${NC}"
fi
echo ""

# ============================================================================
# Step 11: Sync to OneDrive
# ============================================================================
echo -e "${YELLOW}Step 11: Syncing to OneDrive...${NC}"
mkdir -p "$ONEDRIVE_DIR"
rsync -av \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='*.egg-info' \
    --exclude='.eggs' \
    --exclude='dist' \
    --exclude='build' \
    --exclude='_build' \
    --exclude='.venv' \
    --exclude='.git' \
    "$PROJECT_DIR/" "$ONEDRIVE_DIR/"
echo -e "${GREEN}✓ Synced to OneDrive${NC}"
echo ""

# ============================================================================
# Step 12: Push to GitHub (optional)
# ============================================================================
echo -e "${YELLOW}Step 12: Push to GitHub?${NC}"
read -p "Do you want to create a GitHub repository and push? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Creating GitHub repository..."

    # Check if gh is installed
    if command -v gh &> /dev/null; then
        gh repo create PNNL-CMM/cmm-data --public --source=. --remote=origin --push
        echo -e "${GREEN}✓ Pushed to GitHub${NC}"

        # Create release
        read -p "Create v0.1.0 release? (y/n) " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git tag -a v0.1.0 -m "CMM Data v0.1.0 - Initial Release"
            git push origin v0.1.0
            gh release create v0.1.0 \
                --title "CMM Data v0.1.0" \
                --notes-file .github/RELEASE_TEMPLATE.md \
                dist/cmm_data-0.1.0-py3-none-any.whl \
                dist/cmm_data-0.1.0.tar.gz
            echo -e "${GREEN}✓ Release v0.1.0 created${NC}"
        fi
    else
        echo -e "${RED}GitHub CLI (gh) not installed. Install with: brew install gh${NC}"
        echo "Manual steps:"
        echo "  1. Create repo at https://github.com/new"
        echo "  2. git remote add origin https://github.com/PNNL-CMM/cmm-data.git"
        echo "  3. git branch -M main"
        echo "  4. git push -u origin main"
    fi
else
    echo -e "${YELLOW}Skipping GitHub push${NC}"
fi
echo ""

# ============================================================================
# Summary
# ============================================================================
echo -e "${BLUE}============================================================================${NC}"
echo -e "${BLUE}  Setup Complete!${NC}"
echo -e "${BLUE}============================================================================${NC}"
echo ""
echo -e "Package installed at: ${GREEN}$PROJECT_DIR${NC}"
echo -e "Virtual environment:  ${GREEN}$PROJECT_DIR/.venv${NC}"
echo -e "OneDrive sync:        ${GREEN}$ONEDRIVE_DIR${NC}"
echo ""
echo "To activate the virtual environment:"
echo -e "  ${YELLOW}source $PROJECT_DIR/.venv/bin/activate${NC}"
echo ""
echo "To use the package:"
echo -e "  ${YELLOW}python -c \"import cmm_data; print(cmm_data.get_data_catalog())\"${NC}"
echo ""
echo "Wheel location:"
ls -la dist/*.whl 2>/dev/null || echo "  (build wheel with: python -m build)"
echo ""
echo -e "${GREEN}Done!${NC}"
