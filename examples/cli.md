# command line interface (CLI) examples

* Download [100 Sample Synthetic Patient Records, FHIR R4: 36 MB](https://synthetichealth.github.io/synthea-sample-data/downloads/latest/synthea_sample_data_fhir_latest.zip)

* Unzip the file to a directory of your choice, e.g., `~/synthea-sample-data-fhir`
```bash
unzip synthea_sample_data_fhir_latest.zip -d ~/synthea-sample-data-fhir
```

* convert the fhir resources to xlsx extract the `Condition` and `Patient` resources:
```bash
fhiry -i ~/synthea-sample-data-fhir -o ~/synthea-sample-data-fhir/output.xlsx --resource-types=Condition,Patient
```

### All rows have a patientId column which is the FHIR resource id of the Patient resource.

* You can load a config file to specify the resource types and other options:
```bash
fhiry -i ~/synthea-sample-data-fhir -o ~/synthea-sample-data-fhir/output.xlsx --config-file ~/synthea-sample-data-fhir/config.json --resource-types=Condition,Patient
```

Config file example (`config.json`):
```json
{
    "REMOVE": ["text.div", "meta"],
    "RENAME": {}
}