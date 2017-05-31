#
DEFAULT: help
.DEFAULT: help

VE_DIR = venv
BIN_DIR = $(VE_DIR)/bin
#
PIP_CMD = $(BIN_DIR)/pip
PYTHON_CMD = $(BIN_DIR)/python
NOSE_CMD = $(BIN_DIR)/nosetests
FLAKE8_CMD = $(BIN_DIR)/flake8
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
SYS_PYTHON = python3

test:
	@echo "Using flake8 command: $(FLAKE8_CMD)"
	$(FLAKE8_CMD)
	@echo "Usng nose command: $(NOSE_CMD)"
	@echo "	with args: $(NOSE_ARGS)"
	$(NOSE_CMD) $(NOSE_ARGS)

ci-test:
	nosetests $(NOSE_ARGS)

_pre_dev:
	wget \
		--quiet \
		--no-clobber \
		--directory-prefix=$(VE_DIR) \
		https://bootstrap.pypa.io/get-pip.py

dev: _pre_dev
	$(SYS_PYTHON) -m venv --without-pip $(VE_DIR)
	$(PYTHON_CMD) $(VE_DIR)/get-pip.py
	$(PIP_CMD) install -r requirements.txt
	$(PIP_CMD) install -r dev_requirements.txt
	$(PIP_CMD) install -r tests/requirements.txt
	$(PYTHON_CMD) setup.py develop

clean:
	rm -rf $(VE_DIR)
	rm -rf build
	rm -rf dist
	rm -rf __pycache__
	# TODO change this to use 'find ... __pycache__ --exec rm {}];'
	rm -rf lib/tmst/__pycache__
	rm -rf lib/tmst.egg-info

help:
	@echo "Choose from the following:"
	@echo "	dev		Create virtualenv for development."
	@echo "	test		Run unit tests using nose (from virtualenv."
	@echo "	ci-test		Run unit tests for CI (Travis)."
	@echo "	clean		Delete various development files and dirs."
	@echo "	help		This message."
# End of file.
