"""CLI routines."""
import argparse
import logging

import tmst
import tmst.config

_EXIT_CODE = {
    'bad_item_id': 11
}


class CommandLine(tmst.config.GlobalConfig):
    logger_level = logging.WARN

    def __init__(self):
        super().__init__()
        self._init_logger()
        #
        self.item_id = None
        self.command = None
        self.args = None
        #
        self._init_cli()

    def _init_logger(self):
        logger_name = self.base_logger_name
        logger_level = self.logger_level
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logger_level)
        format_str = ''
        format_str += '%(asctime)s'
        format_str += ' [%(levelname)-8s]'
        format_str += ' %(name)s(%(lineno)d)'
        format_str += ' %(message)s'
        formatter = logging.Formatter(format_str, "%H:%M:%S")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.debug('Logger initialized: %s', logger_name)

    def _init_cli(self):
        self.cli = argparse.ArgumentParser()
        self.cli.add_argument(
            '--verbose',
            action='store_true',
            help='More output (debug logging)'
            )
        #
        # Init subparsers.
        subparsers = self.cli.add_subparsers(
            dest='command',
            help='Command choices'
            )
        # edit
        edit_parser = subparsers.add_parser(
            'edit',
            help='Edit help.'
            )
        edit_parser.add_argument(
            'item_id',
            type=int,
            help='Item id to edit.'
            )
        # create
        create_parser = subparsers.add_parser(  # noqa:F841 pylint: disable=W0612
            'create',
            help='Create help.'
            )
        # list
        list_parser = subparsers.add_parser(
            'list',
            help='List help.'
            )
        list_parser.add_argument(
            '--all',
            action='store_true',
            help='List all items.'
            )
        # config
        config_parser = subparsers.add_parser(  # noqa:F841 pylint: disable=W0612
            'config',
            help='Config help.'
            )

    def parse_args(self):
        self.args = self.cli.parse_args()
        if self.args.verbose:
            self.logger.debug('Debug mode.')
            debug = logging.DEBUG
            self.logger_level = logging.DEBUG
            self.logger.setLevel(debug)
            for h in self.logger.handlers:
                h.setLevel(debug)
            self.logger.debug('Logging level reset to debug.')
        self.command = self.args.command
        if 'item_id' in self.args:
            self.item_id = self.args.item_id

    def main(self):
        self.logger.debug('Inside main.')
        self.parse_args()
        todo_items = tmst.TodoItems()
        todo_items.cli_args = self.args
        try:
            todo_items.main(self.command)
        except tmst.UnknownItemIdException:
            raise SystemExit(_EXIT_CODE['bad_item_id'])  # pylint: disable=W0707


def cli():
    cmd_line = CommandLine()
    cmd_line.main()
