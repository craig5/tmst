"""
Some shared stuff.
"""
# core python libraries
import logging
# third party libraries
# custom libraries
# import tmst.config


class BadCommandException(Exception):
    pass


class ConfigException(Exception):
    pass


class BaseObject(object):

    def init_logger(self):
        logger_name = '.'.join([
            self.base_logger_name,
            self.__class__.__name__
            ])
        self.logger = logging.getLogger(logger_name)
