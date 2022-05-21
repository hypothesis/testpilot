.PHONY: help
help:
	@echo "make help              Show this help message"
	@echo "make lint              Run the code linter(s) and print any warnings"
	@echo "make format            Correctly format the code"
	@echo "make checkformatting   Crash if the code isn't correctly formatted"
	@echo "make test              Run all unit tests"
	@echo "make coverage          Print the unit test coverage report"
	@echo "make sure              Make sure that the formatter, linter, tests, etc all pass"
	@echo "make requirements      Re-compile all the requirements/*.txt files"
	@echo "make release           Create a new patch release on GitHub"
	@echo "                       Creates a new release from the latest commit on GitHub,"
	@echo "                       not from the contents of your local copy."
	@echo "                       Creating a new GitHub release will trigger the publish"
	@echo "                       workflow on GitHub actions to publish the release to"
	@echo "                       PyPI.org."
	@echo "make clean             Delete development artefacts (cached files, "
	@echo "                       dependencies, etc)"

.PHONY: lint
lint: python
	pyenv exec tox -e lint

.PHONY: format
format: python
	pyenv exec tox -e format

.PHONY: checkformatting
checkformatting: python
	pyenv exec tox -e checkformatting

.PHONY: test
test: python
	pyenv exec tox

.PHONY: coverage
coverage: python
	pyenv exec tox -e coverage

.PHONY: sure
sure: checkformatting lint test coverage

.PHONY: requirements
requirements:
	bin/compile-requirements

.PHONY: release
release:
	bin/create_new_patch_release.py

.PHONY: clean
clean:
	rm -rf build dist .tox
	find . -path '*/__pycache__*' -delete
	find . -path '*.egg-info*' -delete

.PHONY: python
python:
	bin/install-python
