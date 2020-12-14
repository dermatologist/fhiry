import pytest
from pkg_resources import resource_filename

# if pkg_resources.resource_isdir(__name__, 'guest'):
#     return pkg_resources.resource_filename(__name__, 'guest')

# instance of Fhiry as fixture


@pytest.fixture
def f():
    from fhiry import Fhiry
    _f = Fhiry()
    return _f


def test_set_file(f, capsys):
    f.filename = resource_filename('fhiry.resources.fhir', 'afhir.json')
    print(f.get_info())
    captured = capsys.readouterr()
    assert 'memory usage' in captured.out
