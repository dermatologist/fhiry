from fhiry.fhirsearch import Fhirsearch
from pkg_resources import resource_filename
import json

fs = Fhirsearch(fhir_base_url="http://hapi.fhir.org/baseR4")

my_fhir_search_parameters = {
    "code": "http://snomed.info/sct|39065001",
}

# df = fs.search(resource_type = "Condition", search_parameters = my_fhir_search_parameters)

# print(df.info())


from fhiry.flattenfhir import FlattenFhir

jsonfile = open(
    resource_filename(__name__, "tests/resources") + "/flattenfhir/patient.json"
)
flatten_fhir = FlattenFhir(json.loads(jsonfile.read()))
assert "Medical record of a male patient" in flatten_fhir.flattened
