import pytest
from pkg_resources import resource_filename


@pytest.fixture
def f():
    from fhiry import Fhirndjson
    _f = Fhirndjson()
    return _f


def test_process_folder(f, capsys):
    f.folder = resource_filename(__name__, 'resources')
    f.process_df()
    print(f.df.columns)
    # print(f.df.head(5))
    print(f.df.info())  # 1194
    # captured = capsys.readouterr()
    # assert '1194' in captured.out
