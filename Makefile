.PHONY: help
help:
	@echo "make help              Show this help message"
	@echo "make shell             Launch a Python shell in the project's virtualenv"
	@echo "make lint              Run the code linter(s) and print any warnings"
	@echo "make format            Correctly format the code"
	@echo "make checkformatting   Crash if the code isn't correctly formatted"
	@echo "make test              Run the unit tests"
	@echo "make coverage          Print the unit test coverage report"
	@echo "make sure              Make sure that the formatter, linter, tests, etc all pass"
	@echo "make clean             Delete development artefacts (cached files, "
	@echo "                       dependencies, etc)"

.PHONY: shell
shell: python
	@pyenv exec tox -qe dev

.PHONY: lint
lint: python
	@pyenv exec tox -qe lint

.PHONY: format
format: python
	@pyenv exec tox -qe format

.PHONY: checkformatting
checkformatting: python
	@pyenv exec tox -qe checkformatting

.PHONY: test
test: python
	@pyenv exec tox -q

.PHONY: coverage
coverage: python
	@pyenv exec tox -qe coverage

.PHONY: sure
sure: python
	@pyenv exec tox --parallel -qe 'checkformatting,lint,tests,py{39,38}-tests,coverage'

.PHONY: clean
clean:
	@rm -rf build dist .tox
	@find . -path '*/__pycache__*' -delete
	@find . -path '*.egg-info*' -delete

.PHONY: python
python:
	@bin/make_python
