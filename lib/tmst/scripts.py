"""
CLI routines.
"""
# python core libraries
import argparse
import logging
# third party libraries


class CommandLine(object):
    logger_level = logging.WARN

    def __init__(self):
        self.__init_logger()
        self.__init_cli()
        self.__init_vars()

    def __init_logger(self):
        logger_name = self.__class__.__name__
        logger_level = self.logger_level
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logger_level)
        format_str = ''
        format_str += '%(asctime)s'
        format_str += '[%(levelname)s]'
        format_str += ' %(module)s(%(lineno)d)'
        format_str += ' %(message)s'
        formatter = logging.Formatter(format_str)
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.debug('Logger initialized: {}'.format(logger_name))

    def __init_cli(self):
        self.cli = argparse.ArgumentParser()
        self.cli.add_argument(
            '--debug',
            action='store_true',
            help='Set debug. (Including logging.)'
            )

    def __init_vars(self):
        pass

    def parse_args(self):
        args = self.cli.parse_args()
        if args.debug:
            self.logger.debug('Debug mode.')
            debug = logging.DEBUG
            self.logger.setLevel(debug)
            for h in self.logger.handlers:
                h.setLevel(debug)
            self.logger.debug('Logging level reset to debug.')

    def main(self):
        self.logger.debug('Inside main.')
        self.parse_args()


def cli():
    cmd_line = CommandLine()
    cmd_line.main()
# End of file.
