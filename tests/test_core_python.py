"""
Test the core python stuff; e.g. flake8.
"""
# core python libraries
import flake8.engine
import logging
import os
import unittest
# third party libraries
import flake8.main
# custom libraries


_BASE_DIR = os.path.dirname(os.path.dirname(__file__))
logging.basicConfig()
_LOGGER = logging.getLogger(__name__)
_LOGGER_LEVEL = logging.DEBUG
_VERBOSE = os.environ.get('VERBOSE', None)
if _VERBOSE == 0:
    _LOGGER_LEVEL = logging.WARN
_LOGGER.setLevel(_LOGGER_LEVEL)


class NotFlakeAbleFileException(Exception):
    pass


# Disable pending testing running "raw flake8".
# TODO delete this entire file at some point
@unittest.skip("demonstrating skipping")
class TestCorePython(unittest.TestCase):
    base_dir = _BASE_DIR
    logger = _LOGGER

    def setUp(self):
        self.style_guide = flake8.engine.get_style_guide()

    def _run_flake8_on_file(self, dir_name, file_name):
        full = os.path.join(self.base_dir, dir_name, file_name)
        # Skip some files...
        if file_name.startswith('.'):
            msg = 'Skipping dotfile: {}'.format(file_name)
            raise NotFlakeAbleFileException(msg)
        if file_name.endswith('.pyc'):
            msg = 'Skipping pyc file: {}'.format(file_name)
            raise NotFlakeAbleFileException(msg)
        if os.path.isdir(full):
            msg = 'Skipping dir: {}'.format(full)
            raise NotFlakeAbleFileException(msg)
        #
        self.logger.debug('Checking flake8: {}'.format(full))
        report = self.style_guide.check_files([full])
        errors = []
        for cur in report.get_statistics():
            cur_msg = '{0}: {1}'.format(full, cur)
            errors.append(cur_msg)
        return errors

    def _build_error_string(self, errors):
        error_string = '\n'
        for cur_error in errors:
            error_string += cur_error + '\n'
        return error_string

    def test_setup_file(self):
        file_name = os.path.join(_BASE_DIR, 'setup.py')
        all_errors = self._run_flake8_on_file("", file_name)
        error_string = self._build_error_string(all_errors)
        self.assertEqual(len(all_errors), 0, error_string)

    def test_test_files(self):
        start_dir = os.path.join('tests')
        full_path = os.path.join(self.base_dir, start_dir)
        all_errors = []
        for cur_file in os.listdir(full_path):
            try:
                all_errors.extend(
                    self._run_flake8_on_file(start_dir, cur_file))
            except NotFlakeAbleFileException as e:
                self.logger.debug(e)
        error_string = self._build_error_string(all_errors)
        self.assertEqual(len(all_errors), 0, error_string)

    def test_lib_files(self):
        start_dir = os.path.join('lib', 'tmst')
        full_path = os.path.join(self.base_dir, start_dir)
        all_errors = []
        for cur_file in os.listdir(full_path):
            try:
                all_errors.extend(
                    self._run_flake8_on_file(start_dir, cur_file))
            except NotFlakeAbleFileException as e:
                self.logger.debug(e)
        error_string = self._build_error_string(all_errors)
        self.assertEqual(len(all_errors), 0, error_string)


if __name__ == '__main__':
    unittest.main()
