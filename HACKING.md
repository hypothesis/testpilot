Setting up Your Test Pilot Development Environment
==================================================

First you'll need to install:

* [Git](https://git-scm.com/)
* [GNU Make](https://www.gnu.org/software/make/)
  (this is probably already installed, run `which make` to check)
* [pyenv](https://github.com/pyenv/pyenv)
  (you don't need to install pyenv's shell integration, just the `pyenv` command will do.)

Then to set up your development environment and make sure that everything's
working just clone the git repo and run `make sure`:

```
git clone https://github.com/hypothesis/testpilot.git
cd testpilot
make sure
```

`make sure` will run Test Pilot's code formatting, linting and tests.
The first run might take a while because it'll be calling `pyenv` to install
the necessary versions of Python and calling `tox` to install the Python
dependencies into virtualenvs. Subsequent runs will be faster.

Run `make help` to see what other development environment commands are available:

```
make help
```
