Contributing
============

Thank you for your interest in contributing to the CMM Data package!

.. contents:: Contents
   :local:
   :depth: 2

Development Setup
-----------------

**1. Clone the repository:**

.. code-block:: bash

   git clone https://github.com/PNNL-CMM/cmm-data.git
   cd cmm-data

**2. Create a virtual environment:**

.. code-block:: bash

   python3 -m venv .venv
   source .venv/bin/activate

**3. Install in development mode:**

.. code-block:: bash

   pip install -e ".[full]"
   pip install pytest pytest-cov ruff sphinx sphinx-rtd-theme

**4. Configure data path:**

.. code-block:: bash

   export CMM_DATA_PATH=/path/to/Globus_Sharing

Code Style
----------

We use `ruff <https://github.com/astral-sh/ruff>`_ for linting:

.. code-block:: bash

   # Check code
   ruff check src/

   # Fix auto-fixable issues
   ruff check --fix src/

   # Format code
   ruff format src/

Testing
-------

**Run tests:**

.. code-block:: bash

   # Basic tests
   pytest tests/ -v

   # With coverage
   pytest tests/ -v --cov=cmm_data --cov-report=html

   # Run comprehensive test script
   python scripts/run_all_tests.py

**Test requirements:**

- All new features must have tests
- Maintain >80% code coverage
- Tests must pass before merging

Adding a New Loader
-------------------

**1. Create a new file in** ``src/cmm_data/loaders/``

**2. Inherit from** ``BaseLoader``

**3. Implement required methods:**

.. code-block:: python

   from .base import BaseLoader

   class NewDatasetLoader(BaseLoader):
       dataset_name = "new_dataset"

       def list_available(self):
           """Return list of available items."""
           pass

       def load(self, **kwargs):
           """Load and return DataFrame."""
           pass

**4. Add to** ``__init__.py`` **exports:**

.. code-block:: python

   # In src/cmm_data/loaders/__init__.py
   from .new_dataset import NewDatasetLoader

   __all__ = [
       ...,
       "NewDatasetLoader",
   ]

**5. Update** ``catalog.py`` **with dataset info:**

.. code-block:: python

   # In src/cmm_data/catalog.py
   DATASETS = {
       ...,
       "new_dataset": {
           "name": "New Dataset",
           "description": "Description of the dataset",
           "path": "path/to/data",
       },
   }

**6. Add tests and documentation**

Documentation
-------------

**Build documentation:**

.. code-block:: bash

   cd docs
   make html

   # View in browser
   open _build/html/index.html

**Documentation style:**

- Use Google-style docstrings
- Include type hints
- Provide usage examples
- Document all public methods

**Example docstring:**

.. code-block:: python

   def load_data(self, commodity: str, data_type: str = "world") -> pd.DataFrame:
       """Load commodity data.

       Args:
           commodity: The commodity code (e.g., "lithi").
           data_type: Type of data ("world" or "salient").

       Returns:
           DataFrame containing the commodity data.

       Raises:
           DataNotFoundError: If the commodity is not available.

       Example:
           >>> loader = USGSCommodityLoader()
           >>> df = loader.load_data("lithi", "world")
           >>> print(df.columns)
       """
       pass

Pull Request Process
--------------------

**1. Fork the repository**

**2. Create a feature branch:**

.. code-block:: bash

   git checkout -b feature/my-feature

**3. Make your changes**

**4. Run tests:**

.. code-block:: bash

   pytest tests/
   ruff check src/

**5. Commit with clear message:**

.. code-block:: bash

   git commit -m "Add: feature description"

**6. Push:**

.. code-block:: bash

   git push origin feature/my-feature

**7. Open a Pull Request**

Commit Messages
---------------

Use clear, descriptive commit messages:

- ``Add: new loader for XYZ dataset``
- ``Fix: handle missing values in USGS data``
- ``Update: improve documentation for visualizations``
- ``Refactor: simplify caching logic``
- ``Test: add tests for OECD loader``
- ``Docs: update API reference``

Reporting Issues
----------------

When reporting issues:

- Use the issue templates
- Include Python version and cmm_data version
- Provide minimal reproducible example
- Include full error traceback

**Example issue:**

.. code-block:: text

   **Description:**
   Loading lithium data fails with KeyError.

   **Environment:**
   - Python: 3.11.4
   - cmm_data: 0.1.0
   - pandas: 2.1.0

   **Reproducible example:**
   ```python
   import cmm_data
   df = cmm_data.load_usgs_commodity("lithi", "world")
   # KeyError: 'Prod_t_2022'
   ```

   **Expected behavior:**
   Should load lithium world production data.

   **Traceback:**
   [Full traceback here]

Questions?
----------

Contact the CMM team at PNNL:

- **GitHub Issues:** https://github.com/PNNL-CMM/cmm-data/issues
- **Email:** cmm@pnnl.gov
