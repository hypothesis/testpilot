Test Pilot
==========

Test Pilot formats, lints and tests the files that have changed on your current
branch compared to main:

```terminal
$ testpilot
testpilot=> Installing Python
testpilot=> Formatting
testpilot=> Linting
testpilot=> Running unit tests
testpilot=> Printing coverage report
...                                                                                                            [100%]
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
