from importlib.metadata import version

import pytest

from testpilot.cli import cli


def test_it():
    cli([])


def test_help():
    with pytest.raises(SystemExit) as exc_info:
        cli(["--help"])

    assert not exc_info.value.code


def test_version(capsys):
    with pytest.raises(SystemExit) as exc_info:
        cli(["--version"])

    assert capsys.readouterr().out.strip() == version("testpilot")
    assert not exc_info.value.code


@pytest.fixture(autouse=True)
def core(mocker):
    return mocker.patch("testpilot.cli.core", autospec=True)
