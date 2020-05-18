import logging

logger = logging.getLogger()


class Player(object):
    def __init__(self, attrs=None):
        if not attrs:
            attrs = {}

        self.uid = attrs.get('uid', 0)
        self.name = 'Player {}'.format(self.uid)
        self.room = attrs.get('room')
        self.room.player_enter(self)

        self._log('Instantiated')

    def __str__(self):
        return self.name

    def move(self, direction):
        old_room = self.room
        new_room = self.room.get_adjacent_room(direction)

        old_room.player_exit(self)
        self.room = new_room
        new_room.player_enter(self)

        self._log('Move `%s` OK', direction)

    def _log(self, *args, **kwargs):
        args = list(args)
        level = kwargs.get('level', 'debug')

        args[0] = 'Player({}): '.format(self.uid) + args[0]

        getattr(logger, level)(*args)
