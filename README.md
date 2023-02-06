# :fire: fhiry - FHIR to pandas dataframe for data analysis, AI and ML

![Libraries.io SourceRank](https://img.shields.io/librariesio/sourcerank/pypi/fhiry)
[![PyPI download total](https://img.shields.io/pypi/dm/fhiry.svg)](https://pypi.python.org/pypi/fhiry/)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/dermatologist/fhiry)

## Open Source Python library for import of FHIR resources to pandas dataframe

[Bulk data export using FHIR](https://hl7.org/fhir/uv/bulkdata/export/index.html) may be important if you want to export a cohort for analysis or machine learning.
:fire: **Fhiry** is a [python](https://www.python.org/) package to facilitate this by converting a folder of [FHIR bundles](https://www.hl7.org/fhir/bundle.html)/ndjson into a [pandas](https://pandas.pydata.org/docs/user_guide/index.html) data frame for analysis and importing
into ML packages such as Tensorflow and PyTorch. Test it with the [synthea sample](https://synthea.mitre.org/downloads) or the downloaded ndjson from the [SMART Bulk data server](https://bulk-data.smarthealthit.org/). Use the 'Discussions' tab above for feature requests.

## Installation

```shell
pip install fhiry
```

## Usage

### Import FHIR bundles (JSON) from folder to pandas dataframe

```python
import fhiry.parallel as fp
df = fp.process('/path/to/fhir/resources')
print(df.info())
```

Example source data set: [Synthea](https://synthea.mitre.org/downloads)

Jupyter notebook example: [`notebooks/synthea.ipynb`](notebooks/synthea.ipynb)

### Import NDJSON from folder to pandas dataframe

```python
import fhiry.parallel as fp
df = fp.ndjson('/path/to/fhir/ndjson/files')
print(df.info())
```

Example source data set: [SMART Bulk Data Server](https://bulk-data.smarthealthit.org/) Export

Jupyter notebook example: [`notebooks/ndjson.ipynb`](notebooks/ndjson.ipynb)

### Import FHIR Search results to pandas dataframe

Fetch and import resources from [FHIR Search API](https://www.hl7.org/fhir/search.html) results to pandas dataframe.

Documentation: [`fhir-search.md`](fhir-search.md)

#### Example: Import all conditions with a certain code from FHIR Server

Fetch and import all condition resources with Snomed (Codesystem `http://snomed.info/sct`) Code `39065001` in the FHIR element `Condition.code` ([resource type specific FHIR search parameter `code`](https://www.hl7.org/fhir/condition.html#search)) to a pandas dataframe:

```python
from fhiry.fhirsearch import Fhirsearch

fs = Fhirsearch(fhir_base_url = "http://fhir-server:8080/fhir")

my_fhir_search_parameters = {
    "code": "http://snomed.info/sct|39065001",
}

df = fs.search(resource_type = "Condition", search_parameters = my_fhir_search_parameters)

print(df.info())
```

## Columns
* see df.columns

```
patientId
fullUrl
resource.resourceType
resource.id
resource.name
resource.telecom
resource.gender
...
...
...
```

### [Documentation](https://dermatologist.github.io/fhiry/)

## Contributors

* [Bell Eapen](https://nuchange.ca) | [![Twitter Follow](https://img.shields.io/twitter/follow/beapen?style=social)](https://twitter.com/beapen)
* [Markus Mandalka](https://github.com/Mandalka)
* WIP, PR welcome, please see CONTRIBUTING.md
* [![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg) using CC](https://computecanada.ca)
