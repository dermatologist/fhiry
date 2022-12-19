# :fire: fhiry - FHIR for AI and ML

![Libraries.io SourceRank](https://img.shields.io/librariesio/sourcerank/pypi/fhiry)
[![PyPI download total](https://img.shields.io/pypi/dm/fhiry.svg)](https://pypi.python.org/pypi/fhiry/)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/dermatologist/fhiry)

## About

[Bulk data export using FHIR](https://hl7.org/fhir/uv/bulkdata/export/index.html) may be important if you want to export a cohort for analysis or machine learning.
:fire: **Fhiry** is a python package to facilitate this by converting a folder of [FHIR bundles](https://www.hl7.org/fhir/bundle.html)/ndjson into a [pandas](https://pandas.pydata.org/docs/user_guide/index.html) data frame for analysis and importing
into ML packages such as Tensorflow and PyTorch. Test it with the [synthea sample](https://synthea.mitre.org/downloads) or the downloaded ndjson from the [SMART Bulk data server](https://bulk-data.smarthealthit.org/). Use the 'Discussions' tab above for feature requests.

## Installation

```
pip install fhiry
```

## Usage

### Import FHIR bundles (JSON) from folder to pandas dataframe

```
import fhiry.parallel as fp
df = fp.process('/path/to/fhir/resources')
print(df.info())
```

Example source data set: [Synthea](https://synthea.mitre.org/downloads)

Jupyter notebook example: [`notebooks/synthea.ipynb`](notebooks/synthea.ipynb)

### Import NDJSON from folder to pandas dataframe

```
import fhiry.parallel as fp
df = fp.ndjson('/path/to/fhir/ndjson/files')
print(df.info())
```

Example source data set: [SMART Bulk Data Server](https://bulk-data.smarthealthit.org/) Export

Jupyter notebook example: [`notebooks/ndjson.ipynb`](notebooks/ndjson.ipynb)

### Import FHIR Search results to pandas dataframe

*Warning: Import from FHIR Search API is under development and not well tested yet!*

Import resources from [FHIR Search API](https://www.hl7.org/fhir/search.html) results to pandas dataframe:

For using filter options by `search_parameters` see [FHIR search common parameters for all resource types](https://www.hl7.org/fhir/search.html#standard) and additional FHIR search parameters for certain resource types like [Patient](https://www.hl7.org/fhir/patient.html#search), [Condition](https://www.hl7.org/fhir/condition.html#search), [Observation](https://www.hl7.org/fhir/observation.html#search), ... 

#### Example: Import all Observations

Import all resources (since empty search parameters / no filter) of type Observation
```
from fhiry.fhirsearch import Fhirsearch

fs = Fhirsearch()
fs.fhir_base_url = "http://fhir-server:8080/fhir"
df = fs.search(type = "Observation", search_parameters = {})

print(df.info())
```
#### Example: Import all conditions with a certain code

Import all condition resources with Snomed (Codesystem `http://snomed.info/sct`) Code `39065001` in the FHIR element Condition.code:

```
from fhiry.fhirsearch import Fhirsearch
fs = Fhirsearch()

fs.fhir_base_url = "http://fhir-server:8080/fhir"

my_fhir_search_parameters = {
    "code": "http://snomed.info/sct|39065001",
}

df = fs.search(type = "Condition", search_parameters = my_fhir_search_parameters)

print(df.info())
```

#### Connection settings

To set connection parameters like authentication, SSL certificates, proxies and so on, set or add standard [Python requests](https://requests.readthedocs.io/en/latest/) keyword arguments to the property `requests_kwargs`.

##### Authentication

Authentication is set by [requests parameter `auth`](https://requests.readthedocs.io/en/latest/user/authentication/).

Example using [HTTP Basic Auth](https://requests.readthedocs.io/en/latest/user/authentication/#basic-authentication):
```
from fhiry.fhirsearch import Fhirsearch

fs = Fhirsearch()
fs.fhir_base_url = "http://fhir-server:8080/fhir"

# Set basic auth credentials (https://requests.readthedocs.io/en/latest/user/authentication/#basic-authentication)
fs.requests_kwargs["auth"] = ('myUser', 'myPassword')
```

##### Proxy settings

You can set a HTTP(S)-Proxies by [requests parameter `proxies`](https://requests.readthedocs.io/en/latest/user/advanced/#proxies).

Example:

```
fs.requests_kwargs["proxies"] = {
    'http': 'http://10.10.1.10:3128',
    'https': 'http://10.10.1.10:1080',
}
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
