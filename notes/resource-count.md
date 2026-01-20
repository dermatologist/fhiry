# Resource Count Display Feature

## Overview

FHIRy now automatically displays a summary of FHIR resources processed after completing import operations. This feature provides immediate visibility into the composition of imported healthcare data.

## Affected Operations

The resource count summary is displayed after completing the following import operations:

1. **Import FHIR Bundles (JSON) from Folder** - `Fhiry.process_source()`
2. **Import NDJSON from Folder** - `Fhirndjson.process_source()`
3. **Import FHIR Search Results** - `Fhirsearch.search()`

## Output Format

After processing completes, FHIRy displays a formatted summary to the console:

```
==================================================
FHIR Resource Summary
==================================================
  AllergyIntolerance: 14
  CarePlan: 9
  Condition: 27
  Device: 3
  Observation: 748
  Patient: 25
  Procedure: 829
--------------------------------------------------
  Total resources processed: 1655
==================================================
```

### Key Features

- **Alphabetically sorted** - Resource types are listed in alphabetical order for easy scanning
- **Clear formatting** - Uses consistent separators and indentation
- **Total count** - Displays the overall number of resources processed
- **Automatic display** - No additional configuration required

## Implementation Details

### New Methods in BaseFhiry

#### `get_resource_counts()`

Returns a dictionary mapping FHIR resource types to their counts.

```python
from src.fhiry import Fhiry

f = Fhiry()
f.folder = "/path/to/fhir/bundles"
f.process_source()

counts = f.get_resource_counts()
# Returns: {'Patient': 25, 'Observation': 748, ...}
```

**Returns:**
- `dict[str, int]`: Dictionary with resource type names as keys and counts as values
- Empty dict if dataframe is empty or resourceType column not found

#### `display_resource_counts()`

Displays the resource count summary to the console.

```python
from src.fhiry import Fhiry

f = Fhiry()
f.filename = "/path/to/bundle.json"
f.process_source()

# Resource counts are automatically displayed
# You can also call manually:
f.display_resource_counts()
```

This method:
- Retrieves counts using `get_resource_counts()`
- Formats and prints the summary to stdout
- Returns nothing if no resources are found

### Integration Points

The `display_resource_counts()` method is called automatically at the end of:

1. **Fhiry.process_source()** - After processing file or folder of FHIR bundles
2. **Fhirndjson.process_source()** - After processing folder of NDJSON files
3. **Fhirsearch.search()** - After retrieving all search results from FHIR server

## Use Cases

### Data Quality Validation

Quickly verify that the expected types and quantities of resources were imported:

```python
from src.fhiry import Fhiry

f = Fhiry()
f.folder = "/data/patient-cohort"
f.process_source()

# Console output shows:
# Patient: 100
# Observation: 2500
# Condition: 350
# etc.
```

### Debugging Import Issues

Identify missing or unexpected resource types:

```python
from src.fhiry import Fhirndjson

f = Fhirndjson()
f.folder = "/data/bulk-export"
f.process_source()

# If you expected Medications but see none in the summary,
# you know to investigate the source data
```

### Data Pipeline Monitoring

Track resource counts across different data sources:

```python
from src.fhiry.fhirsearch import Fhirsearch

fs = Fhirsearch(fhir_base_url="https://fhir.server/api")
df = fs.search(resource_type="Patient", search_parameters={"status": "active"})

# Summary automatically displayed showing active patient count
```

## Programmatic Access

For automated workflows, use `get_resource_counts()` to access the data programmatically:

```python
from src.fhiry import Fhiry

f = Fhiry()
f.folder = "/data/import"
f.process_source()

counts = f.get_resource_counts()

# Check if minimum resources were imported
if counts.get("Patient", 0) < 10:
    raise ValueError("Expected at least 10 patients")

# Log to monitoring system
import logging
logging.info(f"Processed {sum(counts.values())} total resources")
```

## Technical Notes

### Resource Type Detection

The feature detects the resource type column automatically:
- Checks for `resourceType` column (after processing removes "resource." prefix)
- Falls back to `resource.resourceType` if prefix removal hasn't occurred
- Returns empty dict if neither column exists

### Performance

The counting operation uses pandas `value_counts()` which is optimized for large datasets. There is minimal performance impact even with hundreds of thousands of resources.

### Testing

Comprehensive test coverage includes:
- Unit tests for `get_resource_counts()` method
- Unit tests for `display_resource_counts()` method  
- Integration tests verifying counts are displayed during import operations
- Tests for all three import types (Bundle, NDJSON, Search)

See `tests/test_fhiry.py`, `tests/test_fhirndjson.py`, and `tests/test_fhirsearch.py` for test examples.

## Future Enhancements

Potential improvements for future versions:

1. **Configurable output** - Option to suppress or customize the display format
2. **Export to file** - Save resource count summary to JSON or CSV
3. **Detailed statistics** - Include min/max/average values for numeric fields by resource type
4. **Comparison mode** - Compare resource counts across multiple imports
5. **Warning thresholds** - Alert when resource counts fall outside expected ranges

## Related Documentation

- [columns.md](columns.md) - Column naming and transformation
- [dataframe.md](dataframe.md) - DataFrame structure and operations
- [ndjson-columns.md](ndjson-columns.md) - NDJSON-specific column handling
