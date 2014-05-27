import logging
import random
from dum.models.player import Player
from dum.models.room import Room, RoomPlaceholder

DIRECTIONS = {
    'NORTH': 'n',
    'SOUTH': 's',
    'EAST': 'e',
    'WEST': 'w'}

logger = logging.getLogger()


class NoRoomException(Exception):
    pass


class World(object):
    DOOR_PROBABILITY = (50, 100)
    TWO_WAY_DOOR_PROBABILITY = (90, 100)

    def __init__(self):
        self.room_index = {}
        self.player_index = {}
        self.last_player_uid = 0

    def spawn_player(self):
        logger.debug('Spawning a player')

        try:
            origin = self.lookup_room(0, 0)
        except NoRoomException:
            logger.debug('Need to generate origin room')
            origin = self.generate_origin_room()

        self.last_player_uid += 1

        player = self.player_index[self.last_player_uid] = Player({
            'uid': self.last_player_uid,
            'room': origin})

        return player

    def remove_player(self, player):
        del self.player_index[player.uid]

    def generate_origin_room(self):
        room = self.room_index[(0, 0)] = Room({
            'pos_x': 0,
            'pos_y': 0})

        self.populate_room(room)

        return room

    def generate_room(self, src_room, direction):
        new_x, new_y = self.translate_pos(
            src_room.pos_x, src_room.pos_y, direction)

        try:
            return self.lookup_room(new_x, new_y)
        except NoRoomException:
            pass

        room = self.room_index[(new_x, new_y)] = Room({
            'pos_x': new_x,
            'pos_y': new_y})

        self.populate_room(room)
        self.link_adjacent_rooms(room)

        return room

    def populate_room(self, room):
        for direction in DIRECTIONS.values():
            if self.maybe(self.DOOR_PROBABILITY):
                room.doors[direction] = RoomPlaceholder()

    def link_adjacent_rooms(self, org_room):
        for direction in DIRECTIONS.values():
            tgt_x, tgt_y = self.translate_pos(
                org_room.pos_x, org_room.pos_y, direction)

            try:
                tgt_room = self.lookup_room(tgt_x, tgt_y)
            except NoRoomException:
                continue

            if self.reflect_dir(direction) in tgt_room.doors:
                tgt_room.doors[self.reflect_dir(direction)] = org_room
                if self.maybe(self.TWO_WAY_DOOR_PROBABILITY):
                    org_room.doors[direction] = tgt_room

    def lookup_room(self, pos_x, pos_y):
        room = self.room_index.get((pos_x, pos_y))

        if not room:
            raise NoRoomException

        return room

    @staticmethod
    def reflect_dir(direction):
        if direction == DIRECTIONS['NORTH']:
            return DIRECTIONS['SOUTH']
        elif direction == DIRECTIONS['SOUTH']:
            return DIRECTIONS['NORTH']
        elif direction == DIRECTIONS['EAST']:
            return DIRECTIONS['WEST']
        elif direction == DIRECTIONS['WEST']:
            return DIRECTIONS['EAST']

    @staticmethod
    def translate_pos(pos_x, pos_y, direction):
        if direction == DIRECTIONS['NORTH']:
            return pos_x, pos_y + 1
        elif direction == DIRECTIONS['SOUTH']:
            return pos_x, pos_y - 1
        elif direction == DIRECTIONS['EAST']:
            return pos_x + 1, pos_y
        elif direction == DIRECTIONS['WEST']:
            return pos_x - 1, pos_y

    @staticmethod
    def maybe(probability):
        return probability[0] > random.randint(0, probability[1])

world_instance = World()
