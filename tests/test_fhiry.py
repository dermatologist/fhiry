import pytest
from pkg_resources import resource_filename


@pytest.fixture
def f():
    from fhiry import Fhiry
    _f = Fhiry()
    return _f


def test_set_file(f, capsys):
    f.filename = resource_filename(__name__, 'resources') + '/afhir.json'
    print(f.get_info())
    captured = capsys.readouterr()
    assert 'memory usage' in captured.out


def test_process_file(f, capsys):
    f.filename = resource_filename(__name__, 'resources') + '/afhir.json'
    f.process_df()
    print(f.df.head(5))
    captured = capsys.readouterr()
    assert '110' in captured.out


def test_process_folder(f, capsys):
    f.folder = resource_filename(__name__, 'resources')
    f.process_df()
    print(f.df.head(5))
    captured = capsys.readouterr()
    assert '98' in captured.out
