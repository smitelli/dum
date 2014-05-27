import logging

logger = logging.getLogger()


class Player(object):
    def __init__(self, attrs=None):
        if not attrs:
            attrs = {}

        self.uid = attrs.get('uid', 0)
        self.room = attrs.get('room')
        self.items = attrs.get('items', [])

        self._log('Instantiated')

    def move(self, direction):
        self.room = self.room.get_adjacent_room(direction)
        self._log('Move `%s` OK', direction)

    def _log(self, *args, **kwargs):
        args = list(args)
        level = kwargs.get('level', 'debug')

        args[0] = 'Player({}): '.format(self.uid) + args[0]

        getattr(logger, level)(*args)
