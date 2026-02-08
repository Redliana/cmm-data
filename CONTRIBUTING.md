# Contributing to CMM LLM Fine-Tuning

Thank you for your interest in contributing to the Critical Minerals and Materials LLM Fine-Tuning project! This document provides guidelines for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Documentation](#documentation)

## Code of Conduct

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to [contact email].

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title** describing the issue
- **Steps to reproduce** the behavior
- **Expected behavior** vs actual behavior
- **Environment details** (Python version, OS, etc.)
- **Error messages** and stack traces if applicable

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:

- **Use case** explaining why this enhancement would be useful
- **Proposed solution** with as much detail as possible
- **Alternatives considered** if any

### Contributing Code

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and validation
5. Commit with clear messages
6. Push to your fork
7. Open a Pull Request

## Development Setup

### Prerequisites

- Python 3.8+
- Git

### Installation

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/CMM-LLM-FineTuning.git
cd CMM-LLM-FineTuning

# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt  # If available
```

### Running Tests

```bash
# Validate corpus integrity
cd Data/preprocessed
python3 validate_corpus.py

# Run unit tests (if available)
python3 -m pytest tests/
```

## Pull Request Process

1. **Update documentation** for any changed functionality
2. **Add tests** for new features
3. **Ensure validation passes** (`python3 validate_corpus.py`)
4. **Update CHANGELOG.md** with your changes
5. **Request review** from maintainers

### PR Title Format

Use conventional commit format:
- `feat: Add new preprocessing for commodity X`
- `fix: Correct parsing of withheld values`
- `docs: Update methodology documentation`
- `refactor: Improve column categorization logic`

## Coding Standards

### Python Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small

### Example Function

```python
def parse_special_value(value: str) -> Dict[str, Any]:
    """
    Parse USGS special value notation into structured representation.

    Args:
        value: Raw string value from CSV (e.g., "W", ">95", "NA")

    Returns:
        Dictionary with 'value' and 'type' keys, plus additional
        context fields based on the value type.

    Examples:
        >>> parse_special_value("W")
        {"value": None, "type": "withheld", "reason": "company proprietary data"}

        >>> parse_special_value(">95")
        {"value": 95, "type": "range", "operator": "greater_than"}
    """
    # Implementation...
```

### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Reference issues when applicable ("Fix #123")

## Documentation

### Updating Documentation

When making changes:

1. Update `README.md` if adding new features
2. Update `METHODOLOGY.md` for preprocessing changes
3. Update `DATA_DICTIONARY.md` for schema changes
4. Add entry to `CHANGELOG.md`

### Documentation Style

- Use clear, concise language
- Include code examples where helpful
- Add tables for structured information
- Keep formatting consistent with existing docs

## Adding New Data Sources

When adding a new data source:

1. Create preprocessing script following existing patterns
2. Handle special values consistently
3. Generate both text and structured_data fields
4. Update DATA_DICTIONARY.md with new fields
5. Add source to METHODOLOGY.md
6. Update corpus_summary.json schema

### Preprocessing Script Template

```python
#!/usr/bin/env python3
"""
Preprocess [Data Source Name] into JSONL format.

Source: [URL or reference]
Output: [output_filename].jsonl
"""

import csv
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

INPUT_DIR = Path("...")
OUTPUT_DIR = Path("...")

def process_data() -> List[Dict]:
    """Process the data source."""
    documents = []
    # Implementation...
    return documents

def main():
    """Main preprocessing function."""
    print("=" * 60)
    print("[Data Source] Preprocessing")
    print("=" * 60)

    documents = process_data()

    # Write output...

if __name__ == "__main__":
    main()
```

## Questions?

Feel free to open an issue for questions or reach out to the maintainers.

Thank you for contributing!
