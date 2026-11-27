import pytest


@pytest.fixture
def bundle():
    return {
        "resourceType": "Bundle",
        "type": "collection",
        "entry": [
            {
                "resource": {
                    "resourceType": "Observation",
                    "id": "o1",
                    "status": "final",
                    "code": {"coding": [{"system": "http://loinc.org", "code": "15074-8", "display": "Glucose"}]},
                    "subject": {"reference": "Patient/p1", "display": "Amy V. Shaw"},
                }
            }
        ],
    }


def test_reference_display_is_kept(bundle):
    from src.fhiry import Fhiry

    df = Fhiry().process_bundle_dict(bundle)

    assert df["subject.display"].tolist() == ["Amy V. Shaw"]
    assert "subject.display.display" not in df.columns
    assert df["code.coding.codes"].tolist() == ["15074-8"]
