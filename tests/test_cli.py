import pytest
from src.fhiry.main import cli


def test_main_routine(capsys):
    # assert exit code 0
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        cli()
        captured = capsys.readouterr()
        print(captured.out)
        assert "fhiry" in captured.out
        # assert pytest_wrapped_e.type == SystemExit
        # assert pytest_wrapped_e.value.code == 0
