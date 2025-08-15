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
