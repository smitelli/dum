# DUM

    =================     ====          ====   ========  ========
    \\ . . . . . . .\\   //. \\        // .\\  \\. . .\\// . . //
    ||. . ._____. . .|| ||. . ||      || . .|| || . . .\/ . . .||
    || . .||   ||. . || || . .||      ||. . || ||. . . . . . . ||
    ||. . ||   || . .|| ||. . ||      || . .|| || . | . . . . .||
    || . .||   ||. _-|| ||-_ .||      ||. _-|| ||-_.|\ . . . . ||
    ||. . ||   ||-'  || ||  `-||      ||-'  || ||  `|\_ . .|. .||
    || . _||   ||    || ||    ||      ||    || ||   |\ `-_/| . ||
    ||_-' ||  .|/    || ||    \|.    .|/    || ||   | \  / |-_.||
    ||    ||_-'      || ||      `-__-'      || ||   | \  / |  `||
    ||    `'         || ||                  || ||   | \  / |   ||
    ||            .===' `===.            .===' /==. |  \/  |   ||
    ||         .=='   \_|-_ `===.    .===' _-|/   `==  \/  |   ||
    ||      .=='    _-'    `-_  `===='  _-'   `-_  /|  \/  |   ||
    ||   .=='    _-'          `-______-'         `' |. /|  |   ||
    ||.=='    _-'                                    `' |  /==.||
    =='    _-'                                           \/   `==
    \   _-'                                               `-_   /
     `''                                                     ``'

A damn unfinished MUD.

## About

Many years ago, I worked with a team that had an interesting whiteboard problem they would present to interview candidates: Design a [multi-user dungeon](https://en.wikipedia.org/wiki/MUD) (MUD) whose world consists of a two-dimensional grid of square rooms. Each room can be connected to any combination of its four adjacent rooms with doors. Some of the doors only allowed passage in one direction. The rooms are generated randomly as the world is explored by players. As players arrive and leave, the world persists as long as the server continues to run.

Eventually it became apparent that nobody on the team had ever actually attempted to solve the problem with a full implementation. So I took it upon myself to try. This is the result, with some fun affordances added in.

## Install and Run

Depending on the configuration of your system, you might need to say `python`, `python2` or `python2.7`. Same deal with `pip`. DUM **must** be run under Python 2.7, and the version of pip must corresponds that version of Python as well.

You might want to use [Virtualenv](https://virtualenv.pypa.io/en/latest/) to keep your system clean. Otherwise,

    pip install -r reqs.txt
    python run.py

Once the server starts, it listens on TCP port 8123 on all available interfaces.

## Playing the Game

From the computer running the server, run:

    telnet localhost 8123

To connect to a DUM server from another server, substitute the server IP address or hostname:

    telnet 192.168.42.42 8123
    telnet triton 8123

If connection is successful, a brief intro will appear followed by a `dum>` prompt. Any of the following commands can be used:

* **name <str>:** View or set the player name. `name` by itself shows the current player name, and `name perljam` sets the player name to perljam.
* **look:** Describe the room the player currently occupies, along with what's in it.
* **walk <dir>:** Move to an adjacent room using a cardinal direction (`north`) or an abbreviation of one (`n`). There must be a door in the desired direction. Beware: Some doors are one-way and cannot be backtracked through!
* **help:** Display a summary of game commands.
* **quit:** Leave the game and disconnect from the server.

The principle of the game is straightforward: **look** around the room to see what's there, **walk** through one of the available doors, and repeat. If another player is in the same room as you, the game will let you know. The game world is stable and can be drawn out on paper as new areas are explored. Disconnecting and reconnecting will place you back in the origin room.

## Yes, it's Python 2.7

While Python 3.4 was available in 2014 when DUM was originally written, the project was developed and tested in Python 2.7 only. The bulk of the syntax should work without modification in newer Python versions (I sniff-tested it in 3.8) but the game will not work correctly due to Python 3's Unicode handling and the changes to `str`/`bytes`. 

The fix may be as simple as upgrading the [Twisted](https://pypi.org/project/Twisted/) version, but I'm not particularly eager to mess with that at the moment.

## License

MIT
