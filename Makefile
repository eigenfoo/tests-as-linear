.PHONY: help venv lint-black lint-pylint lint test check black publish clean
.DEFAULT_GOAL = help

PYTHON = python3
SHELL = bash
VENV_PATH = venv

help:
	@echo "Usage:"
	@grep -E '^[a-zA-Z_-]+:.*?# .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[1;34mmake %-10s\033[0m%s\n", $$1, $$2}'

venv:  # Set up Python virtual environment.
	@printf "Creating Python virtual environment...\n"
	rm -rf ${VENV_PATH}
	( \
	python -m venv ${VENV_PATH}; \
	source ${VENV_PATH}/bin/activate; \
	pip install -U pip; \
	pip install -r requirements-dev.txt; \
	deactivate; \
	)
	@printf "\n\nVirtual environment created! \033[1;34mRun \`source ${VENV_PATH}/bin/activate\` to activate it.\033[0m\n\n\n"

lint-black:
	@printf "Checking code style with black...\n"
	black tests_as_linear/ --check --target-version=py36
	@printf "\033[1;34mBlack passes!\033[0m\n\n"

lint-pylint:
	@printf "Checking code style with pylint...\n"
	pylint tests_as_linear/ --rcfile=.pylintrc
	@printf "\033[1;34mPylint passes!\033[0m\n\n"

lint: lint-black lint-pylint  # Check code style with black and pylint.

test: clean  # Run test scripts.
	@printf "Running test script...\n"
	${SHELL} scripts/test.sh
	@printf "\033[1;34mTests pass!\033[0m\n\n"

check: clean lint test  # Alias for `make clean lint test`.

black:  # Format code in-place with black.
	black tests_as_linear/ --target-version=py36

publish:  # Run notebook in-place and generate HTML files.
	jupyter nbconvert --to notebook --inplace --execute tests-as-linear.ipynb
	jupyter nbconvert --to html tests-as-linear.ipynb
	sh scripts/process-html.sh
	rm tests-as-linear.html

clean:  # Clean directory.
	rm -rf _site/ __pycache__/
	find tests_as_linear/ -type d -name "__pycache__" -exec rm -rf {} +
	find tests_as_linear/ -type d -name "__pycache__" -delete
	find tests_as_linear/ -type f -name "*.pyc" -delete
