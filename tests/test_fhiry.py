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
