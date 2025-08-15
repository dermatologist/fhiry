# 🔥 fhiry — FHIR to Pandas DataFrame for Data Analytics, AI, and ML

[![Release](https://img.shields.io/github/v/release/dermatologist/fhiry)](https://img.shields.io/github/v/release/dermatologist/fhiry)
[![Build status](https://img.shields.io/github/actions/workflow/status/dermatologist/fhiry/main.yml?branch=main)](https://github.com/dermatologist/fhiry/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/dermatologist/fhiry/branch/main/graph/badge.svg)](https://codecov.io/gh/dermatologist/fhiry)
[![Commit activity](https://img.shields.io/github/commit-activity/m/dermatologist/fhiry)](https://img.shields.io/github/commit-activity/m/dermatologist/fhiry)
[![License](https://img.shields.io/github/license/dermatologist/fhiry)](https://img.shields.io/github/license/dermatologist/fhiry)
[![Downloads](https://img.shields.io/pypi/dm/fhiry)](https://pypi.org/project/fhiry)
[![Documentation](https://badgen.net/badge/icon/documentation?icon=libraries&label)](https://dermatologist.github.io/fhiry/)

**FHIRy** is a [Python](https://www.python.org/) package that simplifies health data analytics and machine learning by converting [FHIR bundles](https://www.hl7.org/fhir/bundle.html) or NDJSON files from [bulk data export](https://hl7.org/fhir/uv/bulkdata/export/index.html) into [pandas](https://pandas.pydata.org/docs/user_guide/index.html) DataFrames. These DataFrames can be used directly with ML libraries such as TensorFlow and PyTorch.
FHIRy also supports FHIR server search and FHIR tables on BigQuery.

---

## ✨ Features

- **Flatten FHIR Bundles/NDJSON** to DataFrames for analytics and ML
- **Import from FHIR Server** via FHIR Search API
- **Query FHIR Data on Google BigQuery**
- **LLM-based Natural Language Queries** (see [examples/llm_example.py](examples/llm_example.py))
- **Flexible Filtering and Column Selection**

---

## 🔧 Quick Start

### Installation

**Stable release:**
```sh
pip install fhiry
```

**Latest development version:**
```sh
pip install git+https://github.com/dermatologist/fhiry.git
```

**LLM support:**
```sh
pip install fhiry[llm]
```

---

## Usage

### 1. Import FHIR Bundles (JSON) from Folder

```python
import fhiry.parallel as fp
df = fp.process('/path/to/fhir/resources')
print(df.info())
```
Example dataset: [Synthea](https://synthea.mitre.org/downloads)
Notebook: [`notebooks/synthea.ipynb`](notebooks/synthea.ipynb)

---

### 2. Import NDJSON from Folder

```python
import fhiry.parallel as fp
df = fp.ndjson('/path/to/fhir/ndjson/files')
print(df.info())
```
Example dataset: [SMART Bulk Data Server](https://bulk-data.smarthealthit.org/)
Notebook: [`notebooks/ndjson.ipynb`](notebooks/ndjson.ipynb)

---

### 3. Import FHIR Search Results

Fetch resources from a FHIR server using the [FHIR Search API](https://www.hl7.org/fhir/search.html):

```python
from fhiry.fhirsearch import Fhirsearch

fs = Fhirsearch(fhir_base_url="http://fhir-server:8080/fhir")
params = {"code": "http://snomed.info/sct|39065001"}
df = fs.search(resource_type="Condition", search_parameters=params)
print(df.info())
```
See [`fhir-search.md`](fhir-search.md) for details.

---

### 4. Import from Google BigQuery FHIR Dataset

```python
from fhiry.bqsearch import BQsearch
bqs = BQsearch()
df = bqs.search("SELECT * FROM `bigquery-public-data.fhir_synthea.patient` LIMIT 20")
```

---

### 🚀 5. LLM-based Natural Language Queries

FHIRy supports natural language queries over FHIR bundles/NDJSON using [llama-index](examples/llm_example.py):

```sh
pip install fhiry[llm]
```
See usage: [`examples/llm_example.py`](examples/llm_example.py)

---

### 🚀 6. Convert FHIR Bundles/Resources to Text for LLMs

Convert a FHIR Bundle or resource to a textual representation for LLMs:

```python
from fhiry import FlattenFhir
import json

bundle = json.load(open('bundle.json'))
flatten_fhir = FlattenFhir(bundle)
print(flatten_fhir.flattened)
```

---

## Filters and Column Selection

You can pass a config JSON to any constructor to remove or rename columns:

```python
df = fp.process('/path/to/fhir/resources', config_json='{ "REMOVE": ["resource.text.div"], "RENAME": { "resource.id": "id" } }')
fs = Fhirsearch(fhir_base_url="http://fhir-server:8080/fhir", config_json='{ "REMOVE": ["resource.text.div"], "RENAME": { "resource.id": "id" } }')
bqs = BQsearch('{ "REMOVE": ["resource.text.div"], "RENAME": { "resource.id": "id" } }')
```

See `df.columns` for available columns.
Example columns:
```
patientId
fullUrl
resource.resourceType
resource.id
resource.name
resource.telecom
resource.gender
...
```

---

## Command Line Interface (CLI)

See [CLI examples](examples/cli.md):

```sh
fhiry --help
```

---

## Documentation

Full documentation: [https://dermatologist.github.io/fhiry/](https://dermatologist.github.io/fhiry/)

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Give Us a Star ⭐️

If you find this project useful, please give us a star to help others discover it.

---

## Contributors

- [Bell Eapen](https://nuchange.ca) [![Twitter Follow](https://img.shields.io/twitter/follow/beapen?style=social)](https://twitter.com/beapen)
- [Markus Mandalka](https://github.com/Mandalka)
- PRs welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)