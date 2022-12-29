import pytest
from pkg_resources import resource_filename


@pytest.fixture
def f():
    from src.fhiry import Fhiry
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
    # print(f.df.head(5))
    print(f.df.info()) # 319
    captured = capsys.readouterr()
    assert '319' in captured.out


def test_process_folder(f, capsys):
    f.folder = resource_filename(__name__, 'resources')
    f.process_df()
    # print(f.df.head(5))
    print(f.df.info())  # 1194
    captured = capsys.readouterr()
    assert '1194' in captured.out


def test_process_parallel(capsys):
    folder = resource_filename(__name__, 'resources')
    import src.fhiry.parallel as fp
    df = fp.process(folder)
    print(df.info())
    captured = capsys.readouterr()
    assert '1194' in captured.out


def test_mappings_fhirpath_to_column(f, capsys):

    # set a mapping to extract the Snomed Code (of a condition) by Fhir path to a new column "code_snomed"
    f.mappings_fhirpath_to_column = {
      "code.coding.where(system = 'http://snomed.info/sct').code": 'code_snomed',
    }

    f.filename = resource_filename(__name__, 'resources') + '/afhir.json'
    f.process_df()

    # filter df by the resource id of a condition
    testcondition = f.df[f.df['resource.id'] == "5dcd2d71-207e-46e9-b948-f5c9121580dd"]
    assert len(testcondition) == 1
    # since the condition yet has the index number from the filtered bundle
    # reset the index so the (only) condition/row in the filtered dataframe
    # can be accessed by index number 0
    testcondition = testcondition.reset_index(drop=True)
    # is there a new column "code_snomed" in which the right Snomed code
    # of this condition was extracted by the mapped fhir path?
    assert testcondition.at[0, 'code_snomed'] == ['162864005']
