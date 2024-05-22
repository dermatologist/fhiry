import pytest
from fhir.resources.bundle import Bundle
from fhir.resources.patient import Patient
from fhir.resources.observation import Observation
from fhir.resources.medication import Medication
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

def test_flatten_observation():
    # Test with Observation
    jsonfile = open(resource_filename(__name__, 'resources') + '/flattenfhir/observation.json')
    observation = Observation.parse_raw(jsonfile.read())
    flatten_fhir = FlattenFhir(observation)
    assert flatten_fhir.flattened == "RBS recorded 11 years ago was Value: 6.3 mmol/l. "

def test_flatten_medication():
    # Test with Medication
    jsonfile = open(resource_filename(__name__, 'resources') + '/flattenfhir/medication.json')
    medication = Medication.parse_raw(jsonfile.read())
    flatten_fhir = FlattenFhir(medication)
    assert flatten_fhir.flattened == "Prednisone 5mg tablet (Product) Status: active. "