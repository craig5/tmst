"""Individual todo items."""
import time

import tmst.config
import tmst.shared

_DATA_KEYS = [
    {'name': 'summary'},
    {'name': 'created_epoch'}
]


# TODO move config to a composition and not inherited
class Item(tmst.config.GlobalConfig):  # pylint: disable=R0902

    def __init__(self, item_id=None, data=None):
        super().__init__()
        self.logger = tmst.shared.create_logger(self)
        self.item_id = item_id
        self.__init_vars()
        self.__load_data(data)

    def __init_vars(self):
        self.summary = None
        self.created_epoch = None
        self.details = None
        self.created_epoch = None
        self.deleted_epoch = None
        self.moodified_epoch = None
        self.due_epoch = None
        self.remind_epoch = None
        self.priority = None
        self.status = None
        self.category = None
        self.tags = []

    def __load_data(self, data):
        # TODO figure out how to use _DATA_KEYS and getattr
        self.summary = data.get('summary', None)
        self.created_epoch = data.get('created_epoch', None)
        self.details = data.get('details', None)
        self.status = data.get('status', None)

    @property
    def summary(self):
        return self._summary

    @summary.setter
    def summary(self, value):
        self._summary = value

    @property
    def created_epoch(self):
        return self._created_epoch

    @created_epoch.setter
    def created_epoch(self, value):
        self._created_epoch = value

    @property
    def details(self):
        return self._details

    @details.setter
    def details(self, value):
        self._details = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    def is_active(self):
        if self.status == 'active':
            return True
        return False

    def get_short_output(self):
        data = {
            'id': self.item_id,
            'summary': self.summary
        }
        out_string = '{id:>3}: {summary}'.format(**data)
        created_human = time.strftime(
            '%Y-%m-%d %H:%M:%S',
            time.localtime(self.created_epoch))
        out_string += f' ({created_human})'
        return out_string

    def show_single_line(self):
        print(self)

    def __str__(self):
        out = self.get_short_output()
        deets = self.details
        if deets is not None:
            dlines = deets.split('\n')
            for add_me in dlines:
                out += f'\n\t{add_me}'
        return out
