import json
from pathlib import Path

from src.fhiry.flattenfhir import FlattenFhir


def test_flatten_bundle():
    # Test with Bundle
    jsonfile = open(Path(__file__).parent / "resources" / "flattenfhir" / "bundle.json")
    bundle = json.load(jsonfile)
    flatten_fhir = FlattenFhir(bundle)
    assert flatten_fhir.flattened == "Medication Status: unknown. "


def test_flatten_patient():
    # Test with Patient
    jsonfile = open(
        Path(__file__).parent / "resources" / "flattenfhir" / "patient.json"
    )
    patient = json.load(jsonfile)
    flatten_fhir = FlattenFhir(patient)
    assert "Medical record of a male patient" in flatten_fhir.flattened


def test_flatten_observation():
    # Test with Observation
    jsonfile = open(
        Path(__file__).parent / "resources" / "flattenfhir" / "observation.json"
    )
    observation = json.load(jsonfile)
    flatten_fhir = FlattenFhir(observation)
    assert "RBS recorded" in flatten_fhir.flattened


def test_flatten_medication():
    # Test with Medication
    jsonfile = open(
        Path(__file__).parent / "resources" / "flattenfhir" / "medication.json"
    )
    medication = json.load(jsonfile)
    flatten_fhir = FlattenFhir(medication)
    assert flatten_fhir.flattened == "Prednisone 5mg tablet (Product) Status: active. "


def test_flatten_procedure():
    # Test with Procedure
    jsonfile = open(
        Path(__file__).parent / "resources" / "flattenfhir" / "procedure.json"
    )
    procedure = json.load(jsonfile)
    flatten_fhir = FlattenFhir(procedure)
    assert "Chemotherapy was completed" in flatten_fhir.flattened


def test_flatten_condition():
    # Test with Condition
    jsonfile = open(
        Path(__file__).parent / "resources" / "flattenfhir" / "condition.json"
    )
    condition = json.load(jsonfile)
    flatten_fhir = FlattenFhir(condition)
    assert "Bacterial sepsis was diagnosed" in flatten_fhir.flattened


def test_flatten_allergyintolerance():
    # Test with AllergyIntolerance
    jsonfile = open(
        Path(__file__).parent / "resources" / "flattenfhir" / "allergy_intolerance.json"
    )
    allergyintolerance = json.load(jsonfile)
    flatten_fhir = FlattenFhir(allergyintolerance)
    assert flatten_fhir.flattened == "Penicillin G allergy reported. "


def test_flatten_documentreference():
    # Test with DocumentReference
    jsonfile = open(
        Path(__file__).parent / "resources" / "flattenfhir" / "document_reference.json"
    )
    documentreference = json.load(jsonfile)
    flatten_fhir = FlattenFhir(documentreference)
    assert flatten_fhir.flattened == "Xray report: Normal chest x-ray was created. "
