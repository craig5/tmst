"""
Global, shared config.
"""
# core python libraries
import configparser
import logging
import os
# third party libraries
# custom libraries


class GlobalConfig(object):
    package_name = 'tmst'
    base_logger_name = package_name
    logger_level = logging.INFO
    home_dir = os.path.expanduser('~')
    default_items_dir = 'items'
    default_metadata_file = 'metadata.json'
    config_dir = os.path.join(home_dir, '.tmst')
    command_map = {
        'edit': 'edit_main',
        'config': 'config_main',
        'list-all': 'list_items',
        'create': 'create_item',
        'list': 'list_active_items',
    }
    default_command = 'list'

    def init_config_vars(self):
        self._items_dir = None
        self._metadata_file = None
        self._config_file = None
        self.data_dir = None
        self.config = None

    @property
    def items_dir(self):
        if self._items_dir is None:
            self._items_dir = os.path.join(
                self.data_dir, self.default_items_dir)
        self.logger.debug('Items file: {}'.format(self._items_dir))
        return self._items_dir

    @property
    def metadata_file(self):
        if self._metadata_file is None:
            self._metadata_file = os.path.join(
                self.data_dir, self.default_metadata_file)
        self.logger.debug('Metadata file: {}'.format(self._metadata_file))
        return self._metadata_file

    @property
    def config_file(self):
        if self._config_file is None:
            self._config_file = os.path.join(self.config_dir, 'config.ini')
        return self._config_file

    def load_config(self):
        self.logger.debug('Loading config: {}'.format(self.config_file))
        self.config = configparser.ConfigParser()
        # TODO catch an error if the file doesn't exist
        # Prompt to create an empty one for 1st time users
        self.config.read(self.config_file)
        def_section = 'default'
        raw_data_dir = self.config.get(def_section, 'DataDir')
        if raw_data_dir.startswith('/'):
            self.data_dir = raw_data_dir
        else:
            self.data_dir = os.path.join(self.home_dir, raw_data_dir)
        self.logger.debug('Data dir: {}'.format(self.data_dir))
