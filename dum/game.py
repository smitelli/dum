import logging
import re
from dum.models.world import DIRECTIONS
from dum.models.world import world_instance as world
from dum.models.room import NoDoorException

logger = logging.getLogger()


class Game(object):
    def __init__(self, protocol):
        self.protocol = protocol
        self.player = None
        logger.debug('%s instantiated', self.__class__.__name__)

    def initialize(self):
        self.player = world.spawn_player()
        self._log('Welcome to the game!', level='info')

        # With apologies to Frans P. de Vries
        self.protocol.dum_respond(
            "\x1b[2J"  # telnet clear screen sequence
            '\r\n'
            r"         =================     ====          ====   ========  ========" '\r\n'
            r"         \\ . . . . . . .\\   //. \\        // .\\  \\. . .\\// . . //" '\r\n'
            r"         ||. . ._____. . .|| ||. . ||      || . .|| || . . .\/ . . .||" '\r\n'
            r"         || . .||   ||. . || || . .||      ||. . || ||. . . . . . . ||" '\r\n'
            r"         ||. . ||   || . .|| ||. . ||      || . .|| || . | . . . . .||" '\r\n'
            r"         || . .||   ||. _-|| ||-_ .||      ||. _-|| ||-_.|\ . . . . ||" '\r\n'
            r"         ||. . ||   ||-'  || ||  `-||      ||-'  || ||  `|\_ . .|. .||" '\r\n'
            r"         || . _||   ||    || ||    ||      ||    || ||   |\ `-_/| . ||" '\r\n'
            r"         ||_-' ||  .|/    || ||    \|.    .|/    || ||   | \  / |-_.||" '\r\n'
            r"         ||    ||_-'      || ||      `-__-'      || ||   | \  / |  `||" '\r\n'
            r"         ||    `'         || ||                  || ||   | \  / |   ||" '\r\n'
            r"         ||            .===' `===.            .===' /==. |  \/  |   ||" '\r\n'
            r"         ||         .=='   \_|-_ `===.    .===' _-|/   `==  \/  |   ||" '\r\n'
            r"         ||      .=='    _-'    `-_  `===='  _-'   `-_  /|  \/  |   ||" '\r\n'
            r"         ||   .=='    _-'          `-______-'         `' |. /|  |   ||" '\r\n'
            r"         ||.=='    _-'                                    `' |  /==.||" '\r\n'
            r"         =='    _-'                                           \/   `==" '\r\n'
            r"         \   _-'                                               `-_   /" '\r\n'
            r"          `''                                                     ``' " '\r\n'
            '\r\n'
            'Your name is {}. Use `name` to change it.'.format(str(self.player)),
            prompt=None)
        self.look()

    def teardown(self):
        self._log('Tearing down', level='info')
        world.remove_player(self.player)

    def line_received(self, line):
        line = re.sub(r'\s+', ' ', line)

        if not line:
            self.protocol.dum_respond()
            return
        elif line.startswith('name'):
            name = ' '.join(line.split(' ')[1:])
            self.set_name(name)
            return
        elif line == 'look':
            self.look()
            return
        elif line.startswith('walk'):
            noun = ' '.join(line.split(' ')[1:])
            self.walk(noun)
            return
        elif line == 'help':
            self.help()
            return
        elif line in ('quit', 'exit', 'bye'):
            self.quit()
            return

        self._log('Bad command `%s`', line)
        self.protocol.dum_respond("Sorry, I didn't catch that.")

    def set_name(self, name):
        if not name:
            self.protocol.dum_respond('Your name is {}.'.format(self.player.name))
        else:
            self._log('Player %d changes name from `%s` to `%s`')
            self.player.name = name
            self.protocol.dum_respond('Pleased to meet you, {}.'.format(name))

    def look(self):
        self._log('Looking')
        self.protocol.dum_respond(
            'You are in a room. {} {}'.format(
                self._list_doors(), self._list_room_players()))

    def walk(self, noun):
        noun = noun.lower()
        self._log('Walking `%s`', noun)

        if not noun:
            self.protocol.dum_respond('The `walk` command needs a direction.')
            return
        elif 'north'.startswith(noun):
            direction = DIRECTIONS['NORTH']
        elif 'south'.startswith(noun):
            direction = DIRECTIONS['SOUTH']
        elif 'east'.startswith(noun):
            direction = DIRECTIONS['EAST']
        elif 'west'.startswith(noun):
            direction = DIRECTIONS['WEST']
        elif 'up'.startswith(noun):
            self.protocol.dum_respond(
                "You jump with all your might to try to get a peek up into "
                "the dungeon's spacious attic. The ceilings are high, and the "
                "door is very far away, but still you persist. In the dark "
                "recesses of the cavernous loft, you can almost make out the "
                "faint outline of a box of Christmas decorations or "
                "something. Your legs begin to grow tired and you stop, lest "
                "somebody walk into the room and see you hopping up and down "
                "like an idiot.")
            return
        elif 'down'.startswith(noun):
            self.protocol.dum_respond(
                "Using a strange power you did not even know you had, you "
                "suppress the strong nuclear force that up until now had held "
                "the atoms of your body together. You slowly dissolve and "
                "sink, phasing right through the concrete floor of the "
                "dungeon and into the ground below. You are now stuck, fused "
                "into the Earth's crust. You are also dead.", prompt=None)
            self.protocol.dum_close()
            return
        else:
            self._log('Direction `%s` not valid', noun)
            self.protocol.dum_respond(
                'What do you mean by `{}`? Try `north` or `w`.'.format(noun))
            return

        try:
            self.player.move(direction)
            self._log(
                'Move `%s` OK; now at (%d,%d)', direction,
                self.player.room.pos_x, self.player.room.pos_y)
            self.look()
        except NoDoorException:
            self._log('There is no `%s` door', direction)
            self.protocol.dum_respond('There is no door there!')

    def help(self):
        self._log('Helping')
        self.protocol.dum_respond(
            'The following commands are available\r\n'
            '====================================\r\n'
            '  name <str>  Set your name to <str>.\r\n'
            '  look        Look around the room.\r\n'
            '  walk <dir>  Move to a different room. <dir> should be a cardinal direction\r\n'
            '              like `north` or any abbreviation of such a word.\r\n'
            '  help        Show this help.\r\n'
            '  quit        Abandon the game and all progress.')

    def quit(self):
        self._log('Quitting')
        self.protocol.dum_respond(
            "Ya know, next time you come in here I'm gonna toast ya!",
            prompt=None)
        self.protocol.dum_close()

    def _list_doors(self):
        doors = [{
            DIRECTIONS['NORTH']: 'north',
            DIRECTIONS['SOUTH']: 'south',
            DIRECTIONS['EAST']: 'east',
            DIRECTIONS['WEST']: 'west'
        }[direction] for direction in self.player.room.doors.keys()]

        if len(doors) == 0:
            self._log('0 doors')
            return 'There are no doors; you are trapped. Enjoy your new home.'
        elif len(doors) == 1:
            self._log('1 door')
            return 'There is a door to the {}.'.format(*doors)
        else:
            self._log('%d doors', len(doors))
            return 'There are doors to the {} and {}.'.format(
                ', '.join(doors[:-1]), doors[-1])

    def _list_room_players(self):
        names = [str(p) for p in self.player.room.players.values() if p is not self.player]

        if len(names) == 0:
            self._log('no other players in this room')
            return ''
        else:
            self._log('%d other player(s) in this room')
            return 'You are not alone here. Say hello to {}.'.format(
                ', '.join(names))

    def _log(self, *args, **kwargs):
        args = list(args)
        level = kwargs.get('level', 'debug')

        args[0] = 'Game({}): '.format(self.player.uid) + args[0]

        getattr(logger, level)(*args)
