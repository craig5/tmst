import logging
import os
import unittest

import tmst

logging.basicConfig()


class TestItem(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger(__name__)
        level = logging.INFO
        verbose = os.environ.get('VERBOSE', None)
        if verbose == '0' or verbose == 0:  # pylint: disable=R1714
            level = logging.WARN
        elif verbose:
            level = logging.DEBUG
            self.logger.debug('Logging reset to debug.')
        self.logger.setLevel(level)
        this_file = os.path.abspath(__file__)
        self.tests_dir = os.path.dirname(this_file)
        self.base_dir = os.path.dirname(self.tests_dir)
        self.cases_dir = os.path.join(self.tests_dir, 'cases')

    def tearDown(self):
        pass

    def test_read_simple_items(self):
        """Test the sample data can be loaded and parsed."""
        simple_dir = os.path.join(self.cases_dir, 'simple')
        simple_data_dir = os.path.join(simple_dir, 'data')
        config_dir = os.path.join(simple_dir, 'config')
        tmst.config.GlobalConfig.config_dir = config_dir
        #
        todo = tmst.TodoItems()
        todo.data_dir = simple_data_dir
        #
        self.logger.debug('Data dir: %s', todo.data_dir)
        self.logger.debug('Items dir: %s', todo.items_dir)
        self.logger.debug('Metadata file: %s', todo.metadata_file)
        self.logger.debug('Config file: %s', todo.config_file)
        todo.load_config()
        todo.load_all_items()
        self.assertEqual(todo.item_count, 1)


if __name__ == '__main__':
    unittest.main()
