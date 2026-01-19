# AI Agent Instructions for FHIRy

## Project Overview

FHIRy is a Python package that converts FHIR (Fast Healthcare Interoperability Resources) bundles and NDJSON files into pandas DataFrames for health data analytics, machine learning, and AI applications. It supports FHIR server search, BigQuery integration, and LLM-based natural language queries.

## Development Environment Setup

1. **Python Version**: Requires Python 3.10 or higher (tested on 3.10, 3.11, and 3.12)
2. **Package Manager**: Uses `uv` for fast, reliable dependency management
3. **Setup Commands**:
   ```bash
   uv sync           # Install dependencies from pyproject.toml
   ```

## Project Structure

```
src/fhiry/           # Main source code
├── fhiry.py         # Core FHIR Bundle processor
├── fhirndjson.py    # NDJSON file processor
├── fhirsearch.py    # FHIR server search API integration
├── bqsearch.py      # BigQuery FHIR dataset queries
├── flattenfhir.py   # FHIR resource flattening logic
├── parallel.py      # Parallel processing utilities
├── base_fhiry.py    # Base class for FHIR processors
└── main.py          # CLI entry point

tests/               # Test suite with pytest
docs/                # MkDocs documentation
examples/            # Usage examples
```

## Code Style and Conventions

### Python Style
- **Formatter**: Ruff (enforced via pre-commit hooks)
- **Line Length**: 120 characters maximum
- **Type Hints**: Required for all function signatures (enforced by mypy)
- **Docstrings**: Use Google-style docstrings for classes and public methods
- **Import Organization**: Handled automatically by ruff (isort-compatible)

### Type Checking
- All functions must have type hints
- No implicit optional types
- Check untyped definitions
- Return type annotations are required
- Add `# type: ignore` comments only when necessary, with justification in code comments


## Testing

### Test Framework
- **Framework**: pytest with coverage reporting
- **Coverage**: Tracks coverage for `src.fhiry` module
- **Location**: All tests in `tests/` directory
- **Test Resources**: Sample FHIR bundles in `tests/resources/`

### Running Tests
```bash
uv run pytest --cov=src/fhiry tests/   # Run all tests with coverage
uv run pytest tests/                     # Run tests without coverage
uv run pytest tests/test_specific.py     # Run specific test file
```

### Test Conventions
- Test files must start with `test_`
- Test functions must start with `test_`
- Use fixtures from `tests/conftest.py`
- Maintain high test coverage (aim for >70%)

## Build and Development Workflow

## FHIR Domain-Specific Context

### FHIR Resources
- **FHIR**: Fast Healthcare Interoperability Resources (HL7 standard)
- **Bundles**: Collections of FHIR resources (e.g., Patient, Observation, Condition)
- **NDJSON**: Newline-delimited JSON format used for bulk FHIR data export

### Key FHIR Concepts
- Resources have nested structures that need flattening for DataFrame conversion
- Resource types include: Patient, Observation, Condition, Medication, Procedure, etc.
- FHIR Search API uses RESTful queries with specific parameters
- BigQuery has native FHIR dataset support

### Data Processing
- Flatten nested FHIR structures into tabular format
- Extract coding systems (SNOMED, LOINC, ICD-10) from CodeableConcept
- Handle references between resources (e.g., Patient references in Observations)
- Support column filtering and renaming via config JSON

## Dependencies

### Core Dependencies
- `pandas`: DataFrame operations
- `google-cloud-bigquery`: BigQuery integration
- `tqdm`: Progress bars for long operations
- `click`: CLI framework
- `numpy`: Numerical operations support
- `timeago`: Timestamp formatting
- `prodict`: Dictionary to object conversion
- `responses`: HTTP request mocking for tests
- `openpyxl`: Excel file support

### Optional Dependencies
- `llm` extra: Adds llama-index, langchain for LLM-based queries

### Adding Dependencies
- Add to `dependencies` in `pyproject.toml`
- Run `uv sync` to update lock file
- Check for obsolete deps with `make check` (uses deptry)

## Common Tasks

### Adding a New FHIR Resource Processor
1. Add processing logic in appropriate module (fhiry.py, fhirsearch.py, etc.)
2. Follow existing patterns for resource flattening
3. Add type hints for all methods
4. Write tests with sample FHIR resources
5. Update documentation if adding public API

### Modifying DataFrame Output
- Changes to column extraction logic should be in `base_fhiry.py` or specific processor
- Test with various FHIR resource types
- Verify config JSON filtering still works

### Adding CLI Commands
- Modify `src/fhiry/main.py`
- Use Click decorators for command definition
- Add tests in `tests/test_cli.py`

## Key Files to Check Before Changes

- `pyproject.toml`: Dependencies, tool configuration, project metadata
- `Makefile`: Build, test, and development commands
- `.pre-commit-config.yaml`: Formatting and linting configuration
- `CONTRIBUTING.md`: Contribution guidelines
- `README.md`: Public API and usage examples

## Tips for AI Coding Agents

1. **Always run tests**: `uv run pytest` before submitting changes
2. **Respect FHIR standards**: Consult HL7 FHIR specification when handling resources
4. **Preserve test coverage**: Add tests for new functionality
5. **Use type hints**: Required by mypy configuration
6. **Follow existing patterns**: Check similar code before implementing new features
7. **Target develop branch**: Never push directly to main
8. **Keep dependencies minimal**: Only add if absolutely necessary
9. **Document public APIs**: Update docstrings and README for user-facing changes
10. **Test with real FHIR data**: Use samples in `tests/resources/`
