import pytest
from fhir.resources.bundle import Bundle
from fhir.resources.patient import Patient
from src.fhiry.flattenfhir import FlattenFhir
from pkg_resources import resource_filename
import datetime

def test_flatten_fhir():
    # Test with Bundle
    jsonfile = open(resource_filename(__name__, 'resources') + '/flattenfhir/bundle.json')
    bundle = Bundle.parse_raw(jsonfile.read())
    flatten_fhir = FlattenFhir(bundle)
    assert flatten_fhir.flattened == "Bundle"

def test_flatten_patient():
    # Test with Patient
    jsonfile = open(resource_filename(__name__, 'resources') + '/flattenfhir/patient.json')
    patient = Patient.parse_raw(jsonfile.read())
    flatten_fhir = FlattenFhir(patient)
    assert flatten_fhir.flattened == "Medical record of a male patient born 49 years ago. "
