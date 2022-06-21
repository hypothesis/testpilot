from subprocess import run


def test_help():
    """Test the testpilot --help command."""
    run(["testpilot", "--help"], check=True)


def test_version():
    """Test the testpilot --version command."""
    run(["testpilot", "--version"], check=True)
