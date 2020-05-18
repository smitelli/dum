import logging

logger = logging.getLogger()


class NoDoorException(Exception):
    pass


class RoomPlaceholder(object):
    pass


class Room(object):
    def __init__(self, attrs=None):
        if not attrs:
            attrs = {}

        self.pos_x = attrs.get('pos_x', 0)
        self.pos_y = attrs.get('pos_y', 0)
        self.doors = attrs.get('doors', {})
        self.players = attrs.get('players', {})

        self._log('Instantiated')

    def get_adjacent_room(self, direction):
        # Avoid circular import
        from .world import world_instance as world

        try:
            room = self.doors[direction]
        except KeyError:
            self._log('No door to `%s`', direction)
            raise NoDoorException

        self._log('Found door to `%s`', direction)

        if isinstance(room, RoomPlaceholder):
            room = world.generate_room(src_room=self, direction=direction)
            self._log('New room to `%s` generated OK', direction)

        return room

    def player_enter(self, player):
        self.players[player.uid] = player

    def player_exit(self, player):
        try:
            self.players.pop(player.uid)
        except KeyError:
            self._log(
                'Tried to pop player %d who is not in room', player.uid,
                level='error')

    def _log(self, *args, **kwargs):
        args = list(args)
        level = kwargs.get('level', 'debug')

        args[0] = 'Room({},{}): '.format(self.pos_x, self.pos_y) + args[0]

        getattr(logger, level)(*args)
