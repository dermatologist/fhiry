import pytest
from pkg_resources import resource_filename


@pytest.fixture
def f():
    from src.fhiry.bqsearch import BQsearch
    _f = BQsearch()
    return _f




def test_process_bq(f, capsys):
    f.search()
    print(f.df.shape[0])  # 20
    captured = capsys.readouterr()
    assert '20' in captured.out
