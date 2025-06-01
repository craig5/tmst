import logging
import os
import unittest

logging.basicConfig()
_LOGGER = logging.getLogger(__name__)
_LOGGER_LEVEL = logging.DEBUG
_VERBOSE = os.environ.get('VERBOSE', None)
if _VERBOSE == 0:
    _LOGGER_LEVEL = logging.WARN
_LOGGER.setLevel(_LOGGER_LEVEL)


class SimpleTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple(self):
        """Simple test to verify nose is working."""
        _LOGGER.debug('Debug messing in test_simple.')
        ugh = True
        self.assertTrue(ugh)


if __name__ == '__main__':
    unittest.main()
