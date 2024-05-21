import pytest
from fhir.resources.bundle import Bundle
from fhir.resources.patient import Patient
from src.fhiry.flattenfhir import FlattenFhir
from pkg_resources import resource_filename

def test_flatten_fhir():
    # Test with Bundle
    jsonfile = open(resource_filename(__name__, 'resources') + '/flattenfhir/bundle.json')
    bundle = Bundle.parse_raw(jsonfile.read())
    flatten_fhir = FlattenFhir(bundle)
    assert flatten_fhir.flattened == "Bundle"

    # Test with Patient
    # patient = Patient()
    # flatten_fhir.fhir_object = patient
    # assert flatten_fhir.flattened == "Patient"
    # assert isinstance(flatten_fhir.fhirobject, Patient)

    # Test with None
    # flatten_fhir.fhir_object = None
    # assert flatten_fhir.flattened == ""
    # assert flatten_fhir.fhirobject is None