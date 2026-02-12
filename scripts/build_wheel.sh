#!/bin/bash
# Build wheel package for cmm_data distribution
#
# Usage: ./scripts/build_wheel.sh
#
# Output: dist/cmm_data-0.1.0-py3-none-any.whl

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "============================================================"
echo " Building cmm_data wheel package"
echo "============================================================"
echo ""
echo "Project directory: $PROJECT_DIR"
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] python3 not found"
    exit 1
fi

echo "Python version: $(python3 --version)"
echo ""

# Install build tools if needed
echo "1. Installing build tools..."
python3 -m pip install --upgrade pip build wheel setuptools --quiet

# Clean previous builds
echo "2. Cleaning previous builds..."
rm -rf dist/ build/ src/*.egg-info *.egg-info

# Build the package
echo "3. Building wheel and sdist..."
python3 -m build

echo ""
echo "============================================================"
echo " Build complete!"
echo "============================================================"
echo ""
echo "Generated files:"
ls -la dist/
echo ""
echo "To install the wheel:"
echo "  pip install dist/cmm_data-0.1.0-py3-none-any.whl"
echo ""
echo "To share with collaborators:"
echo "  - Send the .whl file from dist/"
echo "  - They install with: pip install cmm_data-0.1.0-py3-none-any.whl"
echo "  - They also need access to the Globus_Sharing data directory"
