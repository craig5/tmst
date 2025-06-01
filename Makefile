.DEFAULT_GOAL := help

VENV_DIR = venv
INVOKE_CMD = $(VENV_DIR)/bin/invoke

bootstrap:
	@python3 bootstrap.py

dev: bootstrap
	@$(INVOKE_CMD) install

update-reqs: bootstrap
	@$(INVOKE_CMD) update-reqs

info: bootstrap
	@$(INVOKE_CMD) info

test: bootstrap
	@$(INVOKE_CMD) test

clean:
	rm -rf $(VENV_DIR)
	rm -rf build
	rm -rf dist
	find . -depth -type d -name __pycache__ -exec rm -rf {} \;

help:
	@echo "Choose from the following:"
	@echo "	bootstrap	Create virtualenv and install 'core' packages."
	@echo "	dev		Create virtualenv for development."
	@echo "	update-reqs	Update the various requirements files."
	@echo "	info		Show basic info about this package."
	@echo "	test		Run unit tests using nose (from virtualenv."
	@echo "	clean		Delete various development files and dirs."
	@echo "	help		This message."
# End of file.
