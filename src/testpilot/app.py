import argparse
import os
import subprocess
import sys
from functools import lru_cache
from importlib.metadata import version
from subprocess import CalledProcessError
from typing import List

import toml
from toml import TomlDecodeError


def log(message: str) -> None:
    print(f"testpilot=> {message}")


def run(debug: bool, cmd, *args, **kwargs):
    if debug:
        log(f"Running {cmd if isinstance(cmd, str) else ' '.join(cmd)}")

    return subprocess.run(cmd, *args, check=True, **kwargs)


class StandardProject:
    """
    The default project class.

    Used if the current project doesn't have a specific subclass below.
    """

    run_pycodestyle = True

    def __init__(self, tox, debug):
        self.debug = debug
        self.run = Run(tox, debug)

    @property
    @lru_cache()
    def main_branch(self) -> str:
        """Return the name of the project's main git branch."""

        branches = (
            run(
                self.debug,
                [
                    "git",
                    "branch",
                    "--format",
                    "%(refname:lstrip=-1)",
                    "-l",
                    "main",
                    "master",
                ],
                stdout=subprocess.PIPE,
            )
            .stdout.decode("utf8")
            .split()
        )

        if "main" in branches:
            main_branch = "main"
        elif "master" in branches:
            main_branch = "master"
        else:
            raise ValueError(
                "The project doesn't appear to have either a 'main' or a 'master' branch"
            )

        if self.debug:
            log(f"Project's main branch: '{main_branch}'")

        return main_branch

    @lru_cache()
    def is_python_file(self, filename: str) -> bool:  # pylint:disable=no-self-use
        """Return True if `filename` looks like a Python file name."""
        return filename.endswith(".py")

    @lru_cache()
    def is_src_file(self, filename: str) -> bool:
        """Return True if `filename` looks like a source file name (as opposed to a test file)."""
        return not self.is_test_file(filename)

    @lru_cache()
    def is_test_file(self, filename: str) -> bool:  # pylint:disable=no-self-use
        """Return True if `filename` looks like a test file name."""
        return filename.startswith("tests/")

    @lru_cache()
    def is_unit_test_file(self, filename: str) -> bool:  # pylint:disable=no-self-use
        """Return True if `filename` looks like a unit test file name."""
        return filename.startswith("tests/unit")

    @lru_cache()
    def is_functest_file(self, filename: str) -> bool:  # pylint:disable=no-self-use
        """Return True if `filename` looks like a functional test file name."""
        return filename.startswith("tests/functional")

    @lru_cache()
    def test_filename(self, src_filename: str) -> str:  # pylint:disable=no-self-use
        """
        Return the test filename for the given source filename.

        This doesn't check that the returned test filename actually exists: it
        just returns the path to where the test file *should* be according to
        the project's file layout conventions.
        """
        return "tests/unit/" + os.path.splitext(src_filename)[0] + "_test.py"

    @lru_cache()
    def src_filename(self, test_filename: str) -> str:  # pylint:disable=no-self-use
        """
        Return the source filename for the given test filename.

        This doesn't check that the returned source filename actually exists:
        it just returns the path to where the source file *should* be according
        to the project's file layout conventions.
        """
        return test_filename[len("tests/unit/") :][: -len("_test.py")] + ".py"

    @property
    @lru_cache()
    def files(self) -> List[str]:
        """
        Return all files modified on this branch compared to main.

        Includes both modified and newly added files.
        Inclues committed and uncommitted, staged and unstaged changes.

        If a source file has been modified then its corresponding unit test
        file will be included even if the unit test file itself hasn't been
        modified, and vice-versa.

        Files that have been deleted on this branch will *not* be included
        (since you can't format, lint or test a file that doesn't exist) but
        the corresponding source or test files of deleted files *will* be
        included (if they still exist).
        """
        # Find all modified, added or deleted files on this branch compared to main.
        # Note: some of these files might not exist on the filesystem
        # (if they're files that've been deleted on this branch).
        modified_files = set(
            run(
                self.debug,
                ["git", "diff", f"origin/{self.main_branch}", "--name-only"],
                stdout=subprocess.PIPE,
            )
            .stdout.decode("utf8")
            .split()
        )

        # Find all untracked files.
        untracked_files = set(
            run(
                self.debug,
                ["git", "ls-files", "--others", "--exclude-standard"],
                stdout=subprocess.PIPE,
            )
            .stdout.decode("utf8")
            .split()
        )

        files = modified_files.union(untracked_files)

        # For each modified, added, deleted or untracked source file find its
        # corresponding unit test file and vice-versa.
        for modified_file in modified_files:
            if self.is_src_file(modified_file):
                test_filename = self.test_filename(modified_file)
                if os.path.exists(test_filename):
                    files.add(test_filename)
            elif self.is_unit_test_file(modified_file):
                src_filename = self.src_filename(modified_file)
                if os.path.exists(src_filename):
                    files.add(src_filename)

        # We can't format, lint or test files that don't exist so (now that
        # we've found their corresponding source or test files) remove deleted
        # files from the list.
        files = [f for f in files if os.path.isfile(f)]

        return sorted(files)

    @property
    @lru_cache()
    def python_files(self) -> List[str]:
        """Return all Python files modified on this branch compared to main."""
        return [f for f in self.files if self.is_python_file(f)]

    @property
    @lru_cache()
    def src_files(self) -> List[str]:
        """Return all source files modified on this branch compared to main."""
        return [f for f in self.python_files if self.is_src_file(f)]

    @property
    @lru_cache()
    def test_files(self) -> List[str]:
        """Return all test files modified on this branch compared to main."""
        return [f for f in self.python_files if self.is_test_file(f)]

    @property
    @lru_cache()
    def unit_test_files(self) -> List[str]:
        """Return all unit test files modified on this branch compared to main."""
        return [f for f in self.python_files if self.is_unit_test_file(f)]

    @property
    @lru_cache()
    def func_test_files(self) -> List[str]:
        """Return all functional test files modified on this branch compared to main."""
        return [f for f in self.python_files if self.is_functest_file(f)]

    def install_python(self) -> None:
        """Install the project's Python version(s) if they aren't already installed."""

        # Run bin/install-python (if it exists) to make sure that the project's
        # version(s) of Python are installed in pyenv (and that tox is
        # installed in each version of Python).
        if os.path.isfile("bin/install-python"):
            run(self.debug, ["bin/install-python"])
        else:
            # Some projects don't have bin/install-python because it was moved
            # to `hdev/install-python`.
            run(self.debug, ["hdev", "install-python"])

    def format(self) -> None:
        """Run the code formatters on all modified files."""
        if not self.python_files:
            return

        log("Formatting")
        self.run("format", "black --quiet", self.python_files)
        self.run("format", "isort --quiet --atomic", self.python_files)

    def lint(self) -> None:
        """Run the linters on all modified files."""

        if any([self.src_files, self.test_files, self.python_files]):
            log("Linting")
        else:
            return

        if self.src_files:
            self.run("lint", "pylint", self.src_files)

        if self.test_files:
            self.run("lint", "pylint", self.test_files, "--rcfile=tests/.pylintrc")

        if self.python_files:
            if self.run_pycodestyle:
                self.run("lint", "pycodestyle", self.python_files)

            self.run("lint", "pydocstyle", self.python_files)

    def run_unit_tests(self) -> None:
        """Run the unit tests for all modified files."""

        if self.unit_test_files:
            log("Running unit tests")
            self.run("tests", "coverage run -m pytest --quiet", self.unit_test_files)

            log("Printing coverage report")
            self.run("tests", "coverage combine --quiet", [])
            self.run(
                "tests",
                "coverage report",
                [],
                "--fail-under=0 --no-skip-covered --include "
                + ",".join(self.python_files),
            )

    def run_functional_tests(self) -> None:
        """Run all modified functional test files."""
        if self.func_test_files:
            log("Running functional tests")
            self.run("functests", "pytest --quiet", self.func_test_files)

    def run_all(self) -> None:
        """Run all the checks for all the modified files."""
        self.install_python()
        self.format()
        self.lint()
        self.run_unit_tests()
        self.run_functional_tests()


class HProject(StandardProject):
    """Customizations necessary to make testpilot work with the h project."""

    def is_current_project(self) -> bool:  # pylint:disable=no-self-use
        return os.path.isdir("h")

    @lru_cache()
    def is_unit_test_file(self, filename: str) -> bool:
        return filename.startswith("tests/h")

    @lru_cache()
    def src_filename(self, test_filename: str) -> str:
        return (
            os.path.sep.join(test_filename.split(os.path.sep)[1:])[: -len("_test.py")]
            + ".py"
        )

    @lru_cache()
    def test_filename(self, src_filename: str) -> str:
        return "tests/" + os.path.splitext(src_filename)[0] + "_test.py"


class CheckmateProject(StandardProject):
    """Customizations necessary to make testpilot with Checkmate."""

    run_pycodestyle = False

    def is_current_project(self) -> bool:  # pylint:disable=no-self-use
        return os.path.isdir("checkmate")


class ViaProject(StandardProject):
    """Customizations necessary to make testpilot with Via."""

    run_pycodestyle = False

    def is_current_project(self) -> bool:  # pylint:disable=no-self-use
        return os.path.isdir("via")


class ViaHTMLProject(StandardProject):
    """Customizations necessary to make testpilot with Via HTML."""

    run_pycodestyle = False

    def is_current_project(self) -> bool:  # pylint:disable=no-self-use
        return os.path.isdir("viahtml")


class PythonPackageProject(StandardProject):
    """Customizations to make testpilot with our Python packages (as opposed to web apps)."""

    run_pycodestyle = False

    def is_current_project(self) -> bool:  # pylint:disable=no-self-use
        """
        Return True if the current project is a Python package.

        Return True if the current working directory contains a pyproject.toml
        file with a [tool.hdev].project_type setting whose value is "library".
        """
        try:
            toml_dict = toml.load("pyproject.toml")
        except FileNotFoundError:
            return False
        except TomlDecodeError as err:
            raise ValueError(
                "testpilot't parse your project's pyproject.toml file"
            ) from err

        try:
            project_type = toml_dict["tool"]["hdev"]["project_type"]
        except (KeyError, TypeError):
            return False

        return project_type == "library"

    @lru_cache()
    def src_filename(self, test_filename: str) -> str:
        return "src/" + super().src_filename(test_filename)

    @lru_cache()
    def test_filename(self, src_filename: str) -> str:
        # Remove the leading src.
        filename = os.path.sep.join(src_filename.split(os.path.sep)[1:])

        return "tests/unit/" + os.path.splitext(filename)[0] + "_test.py"


class Run:
    def __init__(self, tox, debug):
        self.tox = tox
        self.debug = debug

    def __call__(self, env, cmd, files, options=""):
        files = " ".join(files)

        executable = f".tox/{env}/bin/{cmd.split()[0]}"
        executable_exists = True

        if not os.path.exists(executable):
            log(f"It looks like {executable} doesn't exist, running tox to install it")
            executable_exists = False

        if executable_exists and not self.tox:
            fmt = "pyenv exec .tox/{env}/bin/{cmd} {args}"
        else:
            fmt = "pyenv exec tox -e {env} --run-command '{cmd} {args}'"

        if options:
            args = [options, files]
        else:
            args = [files]

        cmd = fmt.format(env=env, cmd=cmd, args=" ".join(args))

        run(self.debug, cmd, shell=True)


def entry_point():
    parser = argparse.ArgumentParser(
        description="Format, lint and test only the files that have changed on this branch.",
    )
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("-v", "--version", action="store_true")
    parser.add_argument(
        "-t",
        "-s",
        "--tox",
        "--slower",
        action="store_true",
        help="run all commands in tox instead of directly",
    )

    args = parser.parse_args()

    if args.version:
        print(version("testpilot"))
        sys.exit()

    try:
        run(
            args.debug,
            ["git", "rev-parse", "--is-inside-work-tree"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )
    except CalledProcessError:
        sys.exit("It looks like you aren't in a git repo")

    current_project = StandardProject(args.tox, args.debug)

    for project_class in [
        HProject,
        CheckmateProject,
        ViaProject,
        ViaHTMLProject,
        PythonPackageProject,
    ]:
        project = project_class(args.tox, args.debug)
        if project.is_current_project():
            current_project = project
            break

    if args.debug:
        log(f"Project class: {type(current_project)}")

    current_project.run_all()
