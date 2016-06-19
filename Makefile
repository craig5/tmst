#
DEFAULT: help
.DEFAULT: help

VE_DIR = venv
BIN_DIR = $(VE_DIR)/bin
PIP_CMD = $(BIN_DIR)/pip
PYTHON_CMD = $(BIN_DIR)/python
#
SYS_PYTHON = python3

help:
	@echo "Choose from the following:"
	@echo "	dev		Create virtualenv for development."
	@echo "	clean		Delete various development files and dirs."
	@echo "	help		This message."

dev:
	virtualenv -p $(SYS_PYTHON) $(VE_DIR)
	$(PIP_CMD) install -r requirements.txt
	$(PYTHON_CMD) setup.py develop

clean:
	rm -rf $(VE_DIR)
	rm -rf build
	rm -rf dist

# End of file.
