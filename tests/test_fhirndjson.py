from pathlib import Path

import pytest


@pytest.fixture
def f():
    from src.fhiry import Fhirndjson

    _f = Fhirndjson()
    return _f


def test_process_folder(f, capsys):
    f.folder = str(Path(__file__).parent / "resources")
    f.process_source()
    print(f.df.info())  # 839
    captured = capsys.readouterr()
    assert "839" in captured.out


def test_process_parallel(capsys):
    folder = str(Path(__file__).parent / "resources")
    import src.fhiry.parallel as fp

    df = fp.ndjson(folder)
    print(df.info())
    captured = capsys.readouterr()
    assert "839" in captured.out


def test_get_resource_counts(f):
    """Test that get_resource_counts returns correct counts for NDJSON."""
    f.folder = str(Path(__file__).parent / "resources")
    f.process_source()
    
    counts = f.get_resource_counts()
    
    # Verify we get a dictionary
    assert isinstance(counts, dict)
    
    # Verify the total matches the expected number of resources
    total = sum(counts.values())
    assert total == 839
    
    # Verify some expected resource types are present
    assert "Patient" in counts
    assert "Procedure" in counts
    assert counts["Patient"] == 25
    assert counts["Procedure"] == 799


def test_display_resource_counts(f, capsys):
    """Test that display_resource_counts outputs the correct format for NDJSON."""
    f.folder = str(Path(__file__).parent / "resources")
    f.process_source()
    
    captured = capsys.readouterr()
    
    # Verify the output contains expected elements
    assert "FHIR Resource Summary" in captured.out
    assert "Total resources processed: 839" in captured.out
    assert "Patient:" in captured.out
    assert "Procedure:" in captured.out
    assert "=" * 50 in captured.out
