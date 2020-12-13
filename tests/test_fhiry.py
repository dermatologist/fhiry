import pytest



# instance of Fhiry as fixture
@pytest.fixture
def f():
    from fhiry import Fhiry
    _f = Fhiry()
    return _f


def test_set_file(f, capsys):
    f.filename = '/gpfs/fs0/scratch/a/archer/beapen/home/scratch/fhiry/data/fhir/Aaafhir.json'
    print(f.get_info())
    captured = capsys.readouterr()
    assert 'memory usage' in captured.out
