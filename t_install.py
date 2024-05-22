from fhiry.fhirsearch import Fhirsearch
from pkg_resources import resource_filename
from fhir.resources.patient import Patient

fs = Fhirsearch(fhir_base_url = "http://hapi.fhir.org/fhir/baseR4")

my_fhir_search_parameters = {
    "code": "http://snomed.info/sct|39065001",
}

df = fs.search(resource_type = "Condition", search_parameters = my_fhir_search_parameters)

print(df.info())


from fhiry.flattenfhir import FlattenFhir
jsonfile = open(resource_filename(__name__, 'resources') + '/flattenfhir/patient.json')
patient = Patient.parse_raw(jsonfile.read())
flatten_fhir = FlattenFhir(patient)
assert flatten_fhir.flattened == "Medical record of a male patient born 49 years ago. "
