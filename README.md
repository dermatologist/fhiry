# :fire: fhiry - FHIR for AI and ML

![Libraries.io SourceRank](https://img.shields.io/librariesio/sourcerank/pypi/fhiry)
[![PyPI download total](https://img.shields.io/pypi/dm/fhiry.svg)](https://pypi.python.org/pypi/fhiry/)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/dermatologist/fhiry)

## About

[Bulk data export using FHIR](https://hl7.org/fhir/uv/bulkdata/export/index.html) may be important if you want to export a cohort for analysis or machine learning.
:fire: **Fhiry** is a python package to facilitate this by converting a folder of FHIR bundles/ndjson into a pandas data frame for analysis and importing
into ML packages such as Tensorflow and PyTorch. Test it with the [synthea sample](https://synthea.mitre.org/downloads). Use the 'Discussions' tab above for feature requests.

## Installation

```
pip install fhiry
```

## Usage

### Synthea

```
import fhiry.parallel as fp
df = fp.process('/path/to/fhir/resources')
print(df.info())
```

### [SMART Bulk Data Server](https://bulk-data.smarthealthit.org/) Export
```
import fhiry.parallel as fp
df = fp.ndjson('/path/to/fhir/ndjson/files')
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

### [Modules](https://dermatologist.github.io/fhiry/build/html/modules.html)
## Contributors

* [Bell Eapen](https://nuchange.ca) | [![Twitter Follow](https://img.shields.io/twitter/follow/beapen?style=social)](https://twitter.com/beapen)
* WIP, PR welcome, please see CONTRIBUTING.md
* [![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg) using CC](https://computecanada.ca)
