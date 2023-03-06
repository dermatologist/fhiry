import pytest
from pkg_resources import resource_filename


@pytest.fixture
def f():
    from src.fhiry.bqsearch import BQsearch
    _f = BQsearch()
    return _f




def test_process_bq(f, capsys):
    f.search()
    # print(f.df.head(5))
    print(f.df.info())  # 319
    captured = capsys.readouterr()
    assert '319' in captured.out
