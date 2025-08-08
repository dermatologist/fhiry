# import pytest
# from pkg_resources import resource_filename
# import google.auth.exceptions

# @pytest.fixture
# def f():
#     from src.fhiry.bqsearch import BQsearch
#     try:
#         _f = BQsearch()
#     except:
#         with pytest.raises(Exception) as e:
#             _f = BQsearch()
#     return _f


# def test_process_bq(f, capsys):
#     try:
#         f.search()
#         print(f.df.shape[0])  # 20
#         captured = capsys.readouterr()
#         assert '20' in captured.out
#     except:
#         with pytest.raises(Exception) as e:
#             f.search()
