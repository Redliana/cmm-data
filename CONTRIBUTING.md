# Contributing to CMM Data

Thank you for your interest in contributing to the CMM Data package!

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/PNNL-CMM/cmm-data.git
   cd cmm-data
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install in development mode**
   ```bash
   pip install -e ".[full]"
   pip install pytest pytest-cov ruff pre-commit
   ```

4. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

5. **Configure data path**
   ```bash
   export CMM_DATA_PATH=/path/to/Globus_Sharing
   ```

## Pre-commit Hooks

We use [pre-commit](https://pre-commit.com/) to run code quality checks before each commit.

**Installed hooks:**
- **ruff**: Linting and formatting
- **mypy**: Type checking
- **bandit**: Security checks
- **codespell**: Spell checking
- **pydocstyle**: Docstring style
- **rstcheck**: RST documentation syntax
- Various file checks (YAML, TOML, trailing whitespace, etc.)

**Usage:**
```bash
# Run all hooks on all files
pre-commit run --all-files

# Run specific hook
pre-commit run ruff --all-files

# Update hooks to latest versions
pre-commit autoupdate

# Skip hooks temporarily (not recommended)
git commit --no-verify -m "message"
```

## Code Style

We use [ruff](https://github.com/astral-sh/ruff) for linting and formatting:

```bash
# Check code
ruff check src/

# Fix auto-fixable issues
ruff check --fix src/

# Format code
ruff format src/

# Check formatting without changing
ruff format --check src/
```

**Style guidelines:**
- Line length: 100 characters
- Quote style: double quotes
- Import sorting: isort-compatible (handled by ruff)
- Docstrings: Google style

## Testing

```bash
# Run tests
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=cmm_data
```

## Adding a New Loader

1. Create a new file in `src/cmm_data/loaders/`
2. Inherit from `BaseLoader`
3. Implement required methods:
   - `load(**kwargs) -> pd.DataFrame`
   - `list_available() -> List[str]`
4. Add to `__init__.py` exports
5. Update `catalog.py` with dataset info
6. Add tests and documentation

Example:
```python
from .base import BaseLoader

class NewDatasetLoader(BaseLoader):
    dataset_name = "new_dataset"

    def list_available(self):
        # Return list of available items
        pass

    def load(self, **kwargs):
        # Load and return DataFrame
        pass
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run tests: `pytest tests/`
5. Run linter: `ruff check src/`
6. Commit with clear message: `git commit -m "Add feature X"`
7. Push: `git push origin feature/my-feature`
8. Open a Pull Request

## Commit Messages

Use clear, descriptive commit messages:
- `Add: new loader for XYZ dataset`
- `Fix: handle missing values in USGS data`
- `Update: improve documentation for visualizations`
- `Refactor: simplify caching logic`

## Reporting Issues

- Use the issue templates
- Include Python version and cmm_data version
- Provide minimal reproducible example
- Include full error traceback

## Questions?

Contact the CMM team at PNNL.
