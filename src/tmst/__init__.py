"""Main package."""
import json
import os
import subprocess
import tempfile

import tmst.config
import tmst.item
import tmst.shared


class DuplicateItemException(Exception):
    pass


class UnknownItemIdException(Exception):
    pass


# TODO remove this inheritance crap and use composition
class TodoItems(tmst.config.GlobalConfig):

    def __init__(self):
        super().__init__()
        self.logger = tmst.shared.create_logger(self)
        self.__init_vars()

    def __init_vars(self):
        self._items = {}
        self.cli_args = None

    def load_all_items(self):
        self.logger.debug('Loading all items: %s', self.items_dir)
        if not os.path.exists(self.items_dir):
            self.logger.debug('Items dir is missing: %s', self.items_dir)
            if not os.path.exists(self.data_dir):
                self.logger.debug('Creating data dir: %s', self.data_dir)
                # TODO check for error creating data dir
                os.mkdir(self.data_dir)
            if not os.path.exists(self.items_dir):
                self.logger.debug('Creating items dir: %s', self.items_dir)
                # TODO check for exception creaing items_dir
                os.mkdir(self.items_dir)
        ok_item_ext = '.json'
        for cur_file in os.listdir(self.items_dir):
            full = os.path.join(self.items_dir, cur_file)
            # Skip any temp files.
            if cur_file.startswith('.'):
                continue
            if not cur_file.endswith(ok_item_ext):
                self.logger.error('Not a json file: %s', full)
                continue
            cur_id = cur_file[:-(len(ok_item_ext))]
            self.logger.debug('Found item id: %s', cur_id)
            with open(full, 'r', encoding='utf-8') as fp:
                raw_json = json.load(fp)
                new_item = tmst.item.Item(item_id=cur_id, data=raw_json)
                self.add_item(new_item)

    def add_item(self, item):
        new_id = item.item_id
        if new_id in self._items:
            msg = f'Duplicate ID: {new_id}'
            msg = self.logger.fatal(msg)
            raise DuplicateItemException(msg)
        self._items[new_id] = item

    @property
    def items(self):
        for item_id in sorted(self._items.keys()):
            yield self._items[item_id]

    @property
    def item_count(self):
        """
        Return the number of todo items.
        """
        return len(self._items)

    def config_main(self):
        """Handle the config.. just view for now..."""
        output = 'Config:\n'
        output += f'\tconfig dir: {self.config_dir}\n'
        output += f'\titems dir: {self.items_dir}\n'
        print(output.rstrip('\n'))

    def edit_main(self):
        """Main routine for editing items."""
        item_id = str(self.cli_args.item_id)
        self.logger.debug('Edit item: %s', item_id)
        print(self._items)
        try:
            cur_item = self._items[item_id]
            self.logger.debug('Editing item: %s', cur_item)
        except KeyError as e:
            self.logger.fatal('Unknown id: %s', item_id)
            raise UnknownItemIdException(e)  # pylint: disable=W0707

    def list_items(self, only_active=False):
        if only_active is True:
            self.logger.debug('Listing active items.')
            for item in self.items:
                if item.is_active():
                    item.show_single_line()
        else:
            self.logger.debug('Listing all items.')
            for item in self.items:
                item.show_single_line()

    def list_active_items(self):
        self.list_items(only_active=True)

    def create_item(self):
        self.logger.debug('Creating item.')
        t_args = {'suffix': '.tmp.yaml', 'delete': False}
        with tempfile.NamedTemporaryFile(**t_args) as tmp:
            init_string = b'Summary: \n'
            init_string += b'Created: \n'
            init_string += b'Status: \n'
            init_string += b'Tags: \n'
            tmp.write(init_string)
            tmp.flush()
            tmp.seek(0)
            subprocess.call(f'vim {tmp.name}', shell=True)
            print(tmp.name)
            contents = tmp.read()
        print(contents)

    def main(self, command):
        self.logger.debug('Running command: %s', command)
        self.load_config()
        self.load_all_items()
        if command is None:
            command = 'list'
        func_name = self.command_map.get(command, None)
        if func_name is None:
            raise tmst.shared.BadCommandException(f'Command not found: {command}')
        if hasattr(self, func_name) is False:
            raise tmst.shared.BadCommandException(f'Method missing: {func_name}')
        func = getattr(self, func_name)
        func()
