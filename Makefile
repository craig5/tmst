.DEFAULT_GOAL := help

VENV_DIR = venv
BIN_DIR = $(VENV_DIR)/bin
LIB_DIR = lib
TESTS_DIR = tests
#
PIP_CMD = $(BIN_DIR)/pip
PYTHON_CMD = $(BIN_DIR)/python
# TODO remove nose and use pytest
PUR_CMD = $(BIN_DIR)/pur
NOSE_CMD = $(BIN_DIR)/nosetests
FLAKE8_CMD = $(BIN_DIR)/flake8
FLAKE8_ARGS =
ISORT_CMD = $(BIN_DIR)/isort
ISORT_ARGS = --diff --check
# Reset the commands when running with travis.
ifdef TRAVIS
	PIP_CMD = pip
	PYTHON_CMD = python
	NOSE_CMD = nosetests
	FLAKE8_CMD = flake8
endif
# arg lists
NOSE_ARGS =
#
SYS_PYTHON_CMD = python3

_virtualenv:
ifeq ("$(DISABLE_VIRTUAL_ENV)", "true")
	$(warning "Disabling creating virtualenv.. (DISABLE_VIRTUAL_ENV:'$(DISABLE_VIRTUAL_ENV)')")
else
	$(SYS_PYTHON_CMD) -m venv $(VENV_DIR)
endif


_pip_reqs:
	$(PIP_CMD) $(PIP_INSTALL_ARGS) install --upgrade pip
	$(PIP_CMD) $(PIP_INSTALL_ARGS) install --upgrade setuptools wheel
	$(PIP_CMD) install -r requirements.txt

_dev_reqs:
	$(PIP_CMD) $(PIP_INSTALL_ARGS) install --upgrade pur invoke
	$(PIP_CMD) $(PIP_INSTALL_ARGS) install -r dev_requirements.txt

_test_reqs:
	$(PIP_CMD) install -r $(TESTS_DIR)/requirements.txt

_install_self:
	$(PIP_CMD) install -e .

ci-dev: _virtualenv _pip_reqs _test_reqs _install_self

dev: ci-dev _dev_reqs

update-reqs:
	$(PUR_CMD) --force --requirement requirements.txt
	$(PUR_CMD) --force --requirement $(TESTS_DIR)/requirements.txt
	$(PUR_CMD) --force --requirement dev_requirements.txt

test:
	@echo "Using flake8 command: $(FLAKE8_CMD)"
	$(FLAKE8_CMD) $(FLAKE8_ARGS) $(LIB_DIR)
	$(FLAKE8_CMD) $(FLAKE8_ARGS) $(TESTS_DIR)
	$(FLAKE8_CMD) $(FLAKE8_ARGS) setup.py
	#@echo "Usng nose command: $(NOSE_CMD)"
	#@echo "	with args: $(NOSE_ARGS)"
	#$(NOSE_CMD) $(NOSE_ARGS)

ci-test:
	nosetests $(NOSE_ARGS)

clean:
	rm -rf $(VENV_DIR)
	rm -rf build
	rm -rf dist
	rm -rf __pycache__
	# TODO change this to use 'find ... __pycache__ --exec rm {}];'
	rm -rf lib/tmst/__pycache__
	rm -rf lib/tmst.egg-info
	rm -rf tests/__pycache__

help:
	@echo "Choose from the following:"
	@echo "	dev		Create virtualenv for development."
	@echo "	test		Run unit tests using nose (from virtualenv."
	@echo "	ci-test		Run unit tests for CI (Travis)."
	@echo "	clean		Delete various development files and dirs."
	@echo "	help		This message."
# End of file.
