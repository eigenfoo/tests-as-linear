.PHONY: help venv
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
	pip install -r requirements.txt; \
	deactivate; \
	)
	@printf "\n\nVirtual environment created! \033[1;34mRun \`source ${VENV_PATH}/bin/activate\` to activate it.\033[0m\n\n\n"

test:  # Run test scripts.
	${SHELL} scripts/test.sh

run:  # Run `tests-as-linear.ipynb` in-place.
	jupyter nbconvert --to notebook --execute tests-as-linear.ipynb
