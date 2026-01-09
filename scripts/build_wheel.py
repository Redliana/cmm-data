#!/usr/bin/env python3
"""
Build wheel package for cmm_data distribution.

Usage: python scripts/build_wheel.py

Output: dist/cmm_data-0.1.0-py3-none-any.whl
"""

import subprocess
import sys
import shutil
from pathlib import Path


def main():
    print("=" * 60)
    print(" Building cmm_data wheel package")
    print("=" * 60)
    print()

    # Get project directory
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent

    print(f"Project directory: {project_dir}")
    print(f"Python version: {sys.version}")
    print()

    # Change to project directory
    import os
    os.chdir(project_dir)

    # Step 1: Install build tools
    print("1. Installing build tools...")
    subprocess.run([
        sys.executable, "-m", "pip", "install",
        "--upgrade", "pip", "build", "wheel", "setuptools", "--quiet"
    ], check=True)
    print("   Done.")

    # Step 2: Clean previous builds
    print("2. Cleaning previous builds...")
    for dir_name in ["dist", "build"]:
        dir_path = project_dir / dir_name
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"   Removed {dir_name}/")

    # Clean egg-info
    for egg_info in project_dir.glob("*.egg-info"):
        shutil.rmtree(egg_info)
        print(f"   Removed {egg_info.name}")
    for egg_info in (project_dir / "src").glob("*.egg-info"):
        shutil.rmtree(egg_info)
        print(f"   Removed src/{egg_info.name}")
    print("   Done.")

    # Step 3: Build the package
    print("3. Building wheel and sdist...")
    result = subprocess.run([sys.executable, "-m", "build"], check=True)
    print("   Done.")

    # Show results
    print()
    print("=" * 60)
    print(" Build complete!")
    print("=" * 60)
    print()

    dist_dir = project_dir / "dist"
    if dist_dir.exists():
        print("Generated files:")
        for f in sorted(dist_dir.iterdir()):
            size_mb = f.stat().st_size / (1024 * 1024)
            print(f"  {f.name} ({size_mb:.2f} MB)")

        # Find wheel file
        wheel_files = list(dist_dir.glob("*.whl"))
        if wheel_files:
            wheel_file = wheel_files[0]
            print()
            print("To install the wheel:")
            print(f"  pip install {wheel_file}")
            print()
            print("To share with collaborators:")
            print(f"  1. Send them: {wheel_file.name}")
            print("  2. They install: pip install cmm_data-*.whl")
            print("  3. They need access to Globus_Sharing data directory")
    else:
        print("[ERROR] dist/ directory not found")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
