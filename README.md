<a href="https://github.com/hypothesis/testpilot/actions/workflows/ci.yml?query=branch%3Amain"><img src="https://img.shields.io/github/actions/workflow/status/hypothesis/testpilot/ci.yml?branch=main"></a>
<a href="https://pypi.org/project/testpilot/"><img src="https://img.shields.io/pypi/v/testpilot"></a>
<a><img src="https://img.shields.io/badge/python-3.12 | 3.11 | 3.10 | 3.9 | 3.8-success"></a>
<a href="https://github.com/hypothesis/testpilot/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-BSD--2--Clause-success"></a>
<a href="https://github.com/hypothesis/cookiecutters/tree/main/pypackage"><img src="https://img.shields.io/badge/cookiecutter-pypackage-success"></a>
<a href="https://black.readthedocs.io/en/stable/"><img src="https://img.shields.io/badge/code%20style-black-000000"></a>

# Test Pilot

Format, lint and test only the files that have changed on the current branch.

See also: [Test Pilot presentation slides](https://docs.google.com/presentation/d/1zyO8ebsDnz_2j98kBq3JV4oIarhJefCCt8N8qLvuoxw/)

Test Pilot formats, lints and tests the files that have changed on your current
branch compared to main:

```terminal
$ testpilot
testpilot=> Formatting
testpilot=> Linting
testpilot=> Running unit tests
testpilot=> Printing coverage report
...
Name                                       Stmts   Miss Branch BrPart     Cover   Missing
-----------------------------------------------------------------------------------------
lms/app.py                                    44      0      0      0   100.00%
lms/assets.py                                  8      0      0      0   100.00%
lms/new_file_committed_on_this_branch.py       0      0      0      0   100.00%
lms/new_untracked_file.py                      0      0      0      0   100.00%
tests/unit/lms/app_test.py                    15      0      4      0   100.00%
tests/unit/lms/assets_test.py                  5      0      0      0   100.00%
-----------------------------------------------------------------------------------------
TOTAL                                         72      0      4      0   100.00%
testpilot=> Running functional tests
.
```

It compares your branch to main and finds:

* New, modified and deleted files
* Committed, staged and untracked changes
* Source, test and functional test files
* If you've modified a source file (e.g. `src/foo/bar.py`) Test Pilot will find
  its corresponding unit test file (e.g. `tests/unit/foo/bar_test.py`) and will
  run those tests (as well as formatting and linting the test file).
  This also works the other way round: if you modify a unit test file then its
  corresponding source file will be formatted and linted.

This is **much** faster than running `make sure` and produces much less output,
but it'll still catch 99% of problems on your branch. Just run the full `make
sure` once before sending your pull request.

## Only for Hypothesis projects

For now, **Test Pilot only works with Hypothesis projects.**
It uses all sorts of knowledge and assumptions about how the Hypothesis
development environment works, what formatting, testing and linting tools we use,
how we organize our test files, etc.
Test Pilot won't work at all with non-Hypothesis projects unless they happen to
do everything _exactly_ as our projects do.

## Test Pilot bypasses tox

By default Test Pilot bypasses tox and runs commands directly.
For example it runs `.tox/tests/bin/pytest` directly instead of `tox -e tests`.
This is faster but it means tox won't install or update the dependencies
in the virtualenv for you if they aren't already installed and up to date.
Other tox things like setting environment variables etc won't happen either.
If it doesn't seem to be working try running `testpilot` with
`-t` / `--tox` (alias: `-s` / `--slower`) and it'll run all the commands
through tox instead:

```terminal
$ testpilot --tox
```

After doing this once you can usually go back to running `testpilot` without `-t`.

Although `testpilot` without `-t` won't keep the dependencies in your virtualenv
up to date it *will* detect if your virtualenv doesn't exist at all and call tox
to create it.
It'll also detect if the project's version of Python isn't installed and call
pyenv to install it:

```terminal
$ testpilot
testpilot=> Installing Python
Downloading Python-3.8.12.tar.xz...
-> https://www.python.org/ftp/python/3.8.12/Python-3.8.12.tar.xz
Installing Python-3.8.12...
...
Installed Python-3.8.12 to /home/seanh/.pyenv/versions/3.8.12

testpilot=> Formatting
testpilot=> It looks like .tox/format/bin/black doesn't exist, running tox to install it
.tox recreate: /home/seanh/Projects/lms/.tox/.tox
...
```

## Debugging

You can use `-d` / `--debug` to get Test Pilot to print out exactly what
commands it's running and a few other details:

```terminal
$ testpilot --debug
testpilot=> Running git rev-parse --is-inside-work-tree
testpilot=> Project class: <class 'testpilot.app.StandardProject'>
testpilot=> Installing Python
testpilot=> Running bin/install-python
testpilot=> Running git branch --format %(refname:lstrip=-1) -l main master
testpilot=> Project's main branch: 'master'
testpilot=> Running git diff origin/master --name-only
testpilot=> Running git ls-files --others --exclude-standard
testpilot=> Formatting
testpilot=> Running pyenv exec .tox/format/bin/black --quiet lms/app.py lms/assets.py lms/new_file_committed_on_this_branch.py lms/new_untracked_file.py tests/functional/lti_certification/v13/grading/test_assignment_and_grading.py tests/unit/lms/app_test.py tests/unit/lms/assets_test.py
...
```

## Help

See `testpilot --help` for the rest of the command line options:

```terminal
$ testpilot --help
```

## Installing

We recommend using [pipx](https://pypa.github.io/pipx/) to install
Test Pilot.
First [install pipx](https://pypa.github.io/pipx/#install-pipx) then run:

```terminal
pipx install testpilot
```

You now have Test Pilot installed! For some help run:

```
testpilot --help
```

## Upgrading

To upgrade to the latest version run:

```terminal
pipx upgrade testpilot
```

To see what version you have run:

```terminal
testpilot --version
```

## Uninstalling

To uninstall run:

```
pipx uninstall testpilot
```

## Setting up Your Test Pilot Development Environment

First you'll need to install:

* [Git](https://git-scm.com/).
  On Ubuntu: `sudo apt install git`, on macOS: `brew install git`.
* [GNU Make](https://www.gnu.org/software/make/).
  This is probably already installed, run `make --version` to check.
* [pyenv](https://github.com/pyenv/pyenv).
  Follow the instructions in pyenv's README to install it.
  The **Homebrew** method works best on macOS.
  The **Basic GitHub Checkout** method works best on Ubuntu.
  You _don't_ need to set up pyenv's shell integration ("shims"), you can
  [use pyenv without shims](https://github.com/pyenv/pyenv#using-pyenv-without-shims).

Then to set up your development environment:

```terminal
git clone https://github.com/hypothesis/testpilot.git
cd testpilot
make help
```

## Releasing a New Version of the Project

1. First, to get PyPI publishing working you need to go to:
   <https://github.com/organizations/hypothesis/settings/secrets/actions/PYPI_TOKEN>
   and add testpilot to the `PYPI_TOKEN` secret's selected
   repositories.

2. Now that the testpilot project has access to the `PYPI_TOKEN` secret
   you can release a new version by just [creating a new GitHub release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository).
   Publishing a new GitHub release will automatically trigger
   [a GitHub Actions workflow](.github/workflows/pypi.yml)
   that will build the new version of your Python package and upload it to
   <https://pypi.org/project/testpilot/>.

## Changing the Project's Python Versions

To change what versions of Python the project uses:

1. Change the Python versions in the
   [cookiecutter.json](.cookiecutter/cookiecutter.json) file. For example:

   ```json
   "python_versions": "3.10.4, 3.9.12",
   ```

2. Re-run the cookiecutter template:

   ```terminal
   make template
   ```

3. Commit everything to git and send a pull request

## Changing the Project's Python Dependencies

To change the production dependencies in the `setup.cfg` file:

1. Change the dependencies in the [`.cookiecutter/includes/setuptools/install_requires`](.cookiecutter/includes/setuptools/install_requires) file.
   If this file doesn't exist yet create it and add some dependencies to it.
   For example:

   ```
   pyramid
   sqlalchemy
   celery
   ```

2. Re-run the cookiecutter template:

   ```terminal
   make template
   ```

3. Commit everything to git and send a pull request

To change the project's formatting, linting and test dependencies:

1. Change the dependencies in the [`.cookiecutter/includes/tox/deps`](.cookiecutter/includes/tox/deps) file.
   If this file doesn't exist yet create it and add some dependencies to it.
   Use tox's [factor-conditional settings](https://tox.wiki/en/latest/config.html#factors-and-factor-conditional-settings)
   to limit which environment(s) each dependency is used in.
   For example:

   ```
   lint: flake8,
   format: autopep8,
   lint,tests: pytest-faker,
   ```

2. Re-run the cookiecutter template:

   ```terminal
   make template
   ```

3. Commit everything to git and send a pull request
