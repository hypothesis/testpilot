.PHONY: help
help:
	@echo "make help              Show this help message"
	@echo "make shell             Launch a Python shell in the project's virtualenv"
	@echo "make lint              Run the code linter(s) and print any warnings"
	@echo "make format            Correctly format the code"
	@echo "make checkformatting   Crash if the code isn't correctly formatted"
	@echo "make test              Run the unit tests"
	@echo "make coverage          Print the unit test coverage report"
	@echo "make functests         Run the functional tests"
	@echo "make sure              Make sure that the formatter, linter, tests, etc all pass"
	@echo "make template          Update the project with the latest from the cookiecutter"
	@echo "make clean             Delete development artefacts (cached files, "
	@echo "                       dependencies, etc)"

.PHONY: shell
shell: python
	@pyenv exec tox -qe dev

.PHONY: lint
lint: lint-backend lint-frontend

.PHONY: lint-backend
lint-backend: python
	@pyenv exec tox -qe lint

.PHONY: lint-frontend
lint-frontend:

.PHONY: format
format: format-backend format-frontend

.PHONY: format-backend
format-backend: python
	@pyenv exec tox -qe format

.PHONY: format-frontend
format-frontend:

.PHONY: checkformatting
checkformatting: checkformatting-backend checkformatting-frontend

.PHONY: checkformatting-backend
checkformatting-backend: python
	@pyenv exec tox -qe checkformatting

.PHONY: checkformatting-frontend
checkformatting-frontend:

.PHONY: test
test: test-backend test-frontend

.PHONY: test-backend
test-backend: python
	@pyenv exec tox -q

.PHONY: test-frontend
test-frontend:

.PHONY: coverage
coverage: python
	@pyenv exec tox -qe coverage

.PHONY: functests
functests: python
	@pyenv exec tox -qe functests

.PHONY: sure
sure: python checkformatting-frontend lint-frontend test-frontend
	@pyenv exec tox --parallel -qe 'checkformatting,lint,tests,py{39,38}-tests,coverage,functests'

.PHONY: template
template:
	@pyenv exec tox -e template -- $(cookiecutter)

.PHONY: clean
clean:
	@rm -rf build dist .tox
	@find . -path '*/__pycache__*' -delete
	@find . -path '*.egg-info*' -delete

.PHONY: python
python:
	@bin/make_python

