from fhiry.fhirsearch import Fhirsearch

fs = Fhirsearch(fhir_base_url = "http://hapi.fhir.org/fhir/baseR4")

my_fhir_search_parameters = {
    "code": "http://snomed.info/sct|39065001",
}

df = fs.search(resource_type = "Condition", search_parameters = my_fhir_search_parameters)

print(df.info())