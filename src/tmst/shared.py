"""Some shared stuff."""
import logging


class BadCommandException(Exception):
    pass


class ConfigException(Exception):
    pass


def create_logger(cls):
    logger_name = cls.__class__.__name__
    return logging.getLogger(logger_name)
