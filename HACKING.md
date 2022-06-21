# Setting up Your Test Pilot Development Environment

First you'll need to install:

* [Git](https://git-scm.com/)
* [GNU Make](https://www.gnu.org/software/make/)
  (this is probably already installed, run `which make` to check)
* [pyenv](https://github.com/pyenv/pyenv)
  (you don't need to install pyenv's shell integration "shims", just the `pyenv` command will do.)

Then to set up your development environment and make sure that everything's
working just clone the git repo and run `make sure`:

```
git clone https://github.com/hypothesis/testpilot.git
cd testpilot
make help
```

Changing the Project's Python Versions
--------------------------------------

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

Changing the Project's Python Dependencies
------------------------------------------

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
