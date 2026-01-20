from pathlib import Path

import pytest


@pytest.fixture
def f():
    from src.fhiry import Fhiry

    _f = Fhiry(
        '{ "REMOVE": ["resource.text.div"], "RENAME": { "resource.id": "id" }  }'
    )
    return _f


def test_set_file(f, capsys):
    f.filename = str(Path(__file__).parent / "resources" / "afhir.json")
    print(f.get_info())
    captured = capsys.readouterr()
    assert "memory usage" in captured.out


def test_process_file(f, capsys):
    f.filename = str(Path(__file__).parent / "resources" / "afhir.json")
    f.process_source()
    # print(f.df.head(5))
    print(f.df.info())  # 319
    captured = capsys.readouterr()
    assert "319" in captured.out


def test_process_folder(f, capsys):
    f.folder = str(Path(__file__).parent / "resources")
    f.process_source()
    # print(f.df.head(5))
    print(f.df.info())  # 1194
    captured = capsys.readouterr()
    assert "1194" in captured.out


def test_process_parallel(capsys):
    folder = str(Path(__file__).parent / "resources")
    import src.fhiry.parallel as fp

    df = fp.process(folder)
    print(df.info())
    captured = capsys.readouterr()
    assert "1194" in captured.out


def test_get_resource_counts(f):
    """Test that get_resource_counts returns correct counts."""
    f.filename = str(Path(__file__).parent / "resources" / "afhir.json")
    f.process_source()
    
    counts = f.get_resource_counts()
    
    # Verify we get a dictionary
    assert isinstance(counts, dict)
    
    # Verify the total matches the expected number of resources
    total = sum(counts.values())
    assert total == 319
    
    # Verify some expected resource types are present
    assert "Patient" in counts
    assert "Observation" in counts


def test_display_resource_counts(f, capsys):
    """Test that display_resource_counts outputs the correct format."""
    f.filename = str(Path(__file__).parent / "resources" / "afhir.json")
    f.process_source()
    
    captured = capsys.readouterr()
    
    # Verify the output contains expected elements
    assert "FHIR Resource Summary" in captured.out
    assert "Total resources processed: 319" in captured.out
    assert "Patient:" in captured.out
    assert "Observation:" in captured.out
    assert "=" * 50 in captured.out


def test_process_folder_displays_counts(f, capsys):
    """Test that process_source for folder displays resource counts."""
    f.folder = str(Path(__file__).parent / "resources")
    f.process_source()
    
    captured = capsys.readouterr()
    
    # Verify the resource count summary is displayed
    assert "FHIR Resource Summary" in captured.out
    assert "Total resources processed: 1194" in captured.out
    assert "CarePlan:" in captured.out
    assert "Condition:" in captured.out
    assert "Observation:" in captured.out
