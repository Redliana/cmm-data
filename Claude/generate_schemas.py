#!/usr/bin/env python3
"""
Convert geodatabase to CSV and generate comprehensive schema documentation
for all CSV files in the CMM data collection.
"""

from __future__ import annotations

import csv
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(
    "/Users/wash198/Documents/Projects/Science_Projects/MPII_CMM/LLM_Fine_Tuning/Claude"
)


def get_csv_schema(csv_path, sample_rows=5):
    """Extract schema information from a CSV file."""
    schema = {
        "file": str(csv_path.name),
        "path": str(csv_path),
        "columns": [],
        "row_count": 0,
        "sample_data": [],
    }

    try:
        with open(csv_path, encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f)
            headers = next(reader, [])

            schema["columns"] = []
            # Initialize type tracking
            col_types = defaultdict(set)
            col_samples = defaultdict(list)

            rows = []
            for i, row in enumerate(reader):
                schema["row_count"] += 1
                if i < 100:  # Sample first 100 rows for type inference
                    for j, val in enumerate(row):
                        if j < len(headers):
                            col_types[j].add(infer_type(val))
                            if len(col_samples[j]) < 3 and val.strip():
                                col_samples[j].append(val[:50])
                if i < sample_rows:
                    rows.append(row)

            schema["sample_data"] = rows

            for i, header in enumerate(headers):
                types = col_types.get(i, {"unknown"})
                # Simplify type
                if "float" in types:
                    dtype = "numeric"
                elif "int" in types and len(types) == 1:
                    dtype = "integer"
                elif types == {"empty"}:
                    dtype = "empty"
                else:
                    dtype = "text"

                schema["columns"].append(
                    {"name": header, "type": dtype, "samples": col_samples.get(i, [])}
                )
    except Exception as e:
        schema["error"] = str(e)

    return schema


def infer_type(value):
    """Infer the data type of a value."""
    if not value or value.strip() == "":
        return "empty"
    try:
        int(value)
        return "int"
    except:
        pass
    try:
        float(value)
        return "float"
    except:
        pass
    return "str"


def convert_geodatabase_to_csv(gdb_path, output_dir):
    """Convert all layers in a geodatabase to CSV files."""
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    # Get list of layers
    result = subprocess.run(["ogrinfo", str(gdb_path)], capture_output=True, text=True)

    layers = []
    for line in result.stdout.split("\n"):
        if "Layer:" in line:
            # Extract layer name
            match = re.search(r"Layer: (\S+)", line)
            if match:
                layers.append(match.group(1))

    print(f"Found {len(layers)} layers to convert")

    converted = []
    for i, layer in enumerate(layers):
        output_file = output_dir / f"{layer}.csv"
        print(f"[{i + 1}/{len(layers)}] Converting {layer}...", end=" ")

        try:
            result = subprocess.run(
                [
                    "ogr2ogr",
                    "-f",
                    "CSV",
                    str(output_file),
                    str(gdb_path),
                    layer,
                    "-lco",
                    "GEOMETRY=AS_WKT",
                ],
                capture_output=True,
                text=True,
                timeout=60,
            )
            if output_file.exists():
                size = output_file.stat().st_size
                print(f"OK ({size / 1024:.1f} KB)")
                converted.append(layer)
            else:
                print("FAILED (no output)")
        except subprocess.TimeoutExpired:
            print("TIMEOUT")
        except Exception as e:
            print(f"ERROR: {e}")

    return converted


def generate_all_schemas():
    """Generate schemas for all CSV files in the data collection."""
    all_schemas = {}

    # Define data directories
    data_dirs = {
        "LISA_Model": BASE_DIR / "LISA_Model" / "extracted_data",
        "USGS_Mineral_Commodities_Salient": BASE_DIR / "USGS_Data" / "salient",
        "USGS_Mineral_Commodities_World": BASE_DIR / "USGS_Data" / "world",
        "USGS_Industry_Trends": BASE_DIR / "USGS_Data",
        "USGS_Ore_Deposits": BASE_DIR / "USGS_Ore_Deposits",
        "NETL_REE_Coal_Geodatabase": BASE_DIR / "NETL_REE_Coal" / "geodatabase_csv",
    }

    for category, dir_path in data_dirs.items():
        if not dir_path.exists():
            print(f"Skipping {category} - directory not found")
            continue

        print(f"\n=== Processing {category} ===")
        schemas = []

        csv_files = list(dir_path.glob("*.csv"))
        for i, csv_file in enumerate(csv_files):
            if i % 50 == 0:
                print(f"  Processing file {i + 1}/{len(csv_files)}...")
            schema = get_csv_schema(csv_file)
            schemas.append(schema)

        all_schemas[category] = {
            "directory": str(dir_path),
            "file_count": len(schemas),
            "schemas": schemas,
        }
        print(f"  Processed {len(schemas)} files")

    return all_schemas


def write_schema_documentation(schemas, output_file):
    """Write schema documentation to a JSON file."""
    with open(output_file, "w") as f:
        json.dump(schemas, f, indent=2)
    print(f"\nSchema documentation written to {output_file}")


def write_schema_csv_summary(schemas, output_file):
    """Write a CSV summary of all schemas."""
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Category", "File", "Rows", "Columns", "Column_Names"])

        for category, data in schemas.items():
            for schema in data["schemas"]:
                col_names = "; ".join([c["name"] for c in schema.get("columns", [])])
                writer.writerow(
                    [
                        category,
                        schema.get("file", ""),
                        schema.get("row_count", 0),
                        len(schema.get("columns", [])),
                        col_names[:500],  # Truncate if too long
                    ]
                )
    print(f"Schema summary CSV written to {output_file}")


def write_schema_markdown(schemas, output_file):
    """Write schema documentation as markdown."""
    with open(output_file, "w") as f:
        f.write("# CMM Supply Chain Data Schema Reference\n\n")
        f.write(
            "This document describes the schema for all CSV data files in the CMM supply chain data collection.\n\n"
        )
        f.write("## Table of Contents\n\n")

        for category in schemas.keys():
            f.write(f"- [{category}](#{category.lower().replace('_', '-')})\n")

        f.write("\n---\n\n")

        for category, data in schemas.items():
            f.write(f"## {category}\n\n")
            f.write(f"**Directory:** `{data['directory']}`\n\n")
            f.write(f"**Total Files:** {data['file_count']}\n\n")

            # Group by similar schemas
            if data["file_count"] > 20:
                f.write(
                    "*Note: Showing representative schemas (many files have similar structure)*\n\n"
                )
                # Show first 5 unique column structures
                seen_structures = set()
                shown = 0
                for schema in data["schemas"]:
                    cols = tuple([c["name"] for c in schema.get("columns", [])])
                    if cols not in seen_structures and shown < 10:
                        seen_structures.add(cols)
                        write_single_schema(f, schema)
                        shown += 1
            else:
                for schema in data["schemas"]:
                    write_single_schema(f, schema)

            f.write("\n---\n\n")

    print(f"Schema markdown written to {output_file}")


def write_single_schema(f, schema):
    """Write a single schema to the markdown file."""
    f.write(f"### {schema.get('file', 'Unknown')}\n\n")
    f.write(f"- **Rows:** {schema.get('row_count', 'Unknown')}\n")
    f.write(f"- **Columns:** {len(schema.get('columns', []))}\n\n")

    if schema.get("columns"):
        f.write("| Column | type | Sample Values |\n")
        f.write("|--------|------|---------------|\n")
        for col in schema["columns"][:30]:  # Limit to 30 columns
            samples = ", ".join(col.get("samples", [])[:2])
            f.write(f"| {col['name']} | {col['type']} | {samples} |\n")
        if len(schema["columns"]) > 30:
            f.write(f"| ... | ... | *({len(schema['columns']) - 30} more columns)* |\n")
    f.write("\n")


def main():
    print("=" * 60)
    print("CMM Data Schema Generator")
    print("=" * 60)

    # Convert geodatabase to CSV
    gdb_path = BASE_DIR / "NETL_REE_Coal" / "ree-and-coal-open-geodatabase.gdb"
    csv_output = BASE_DIR / "NETL_REE_Coal" / "geodatabase_csv"

    if gdb_path.exists():
        print(f"\n1. Converting geodatabase to CSV...")
        converted = convert_geodatabase_to_csv(gdb_path, csv_output)
        print(f"   Converted {len(converted)} layers")
    else:
        print(f"Geodatabase not found at {gdb_path}")

    # Generate schemas
    print(f"\n2. Generating schemas for all CSV files...")
    schemas = generate_all_schemas()

    # Write outputs
    print(f"\n3. Writing schema documentation...")
    schema_dir = BASE_DIR / "schemas"
    schema_dir.mkdir(exist_ok=True)

    write_schema_documentation(schemas, schema_dir / "all_schemas.json")
    write_schema_csv_summary(schemas, schema_dir / "schema_summary.csv")
    write_schema_markdown(schemas, schema_dir / "SCHEMA_REFERENCE.md")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    total_files = sum(d["file_count"] for d in schemas.values())
    total_rows = sum(sum(s.get("row_count", 0) for s in d["schemas"]) for d in schemas.values())
    print(f"Total CSV files documented: {total_files}")
    print(f"Total data rows: {total_rows:,}")
    print(f"\nSchema files created in: {schema_dir}")


if __name__ == "__main__":
    main()
