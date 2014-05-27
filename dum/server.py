import logging
import textwrap
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from game import Game

logger = logging.getLogger()


class GameProtocol(LineReceiver):
    WRAP_AFTER = 78
    CRLF = '\r\n'

    def __init__(self):
        self.delimiter = self.CRLF
        self.game = Game(protocol=self)
        logger.debug('%s instantiated', self.__class__.__name__)

    def connectionMade(self):
        self.game.initialize()
        self._log('Connection is ready and raring to go!', level='info')

    def connectionLost(self, reason):
        self.game.teardown()
        self._log('Disconnected: %s', reason.getErrorMessage(), level='info')

    def lineReceived(self, line):
        self._log('<-- %s', line)
        self.game.line_received(line)

    def dum_respond(self, response='', prompt='dum'):
        self._log('--> <%d bytes, prompt=%s>', len(response), prompt)

        if response:
            self.sendLine('')
            for line in response.split(self.CRLF):
                wrapped_line = textwrap.wrap(line, width=self.WRAP_AFTER)
                self.sendLine(self.CRLF.join(wrapped_line))

        if prompt:
            self.delimiter = ' '
            self.sendLine('{0}>'.format(prompt))
            self.delimiter = self.CRLF

    def dum_close(self):
        self._log('Closing connection')
        self.transport.loseConnection()

    def _log(self, *args, **kwargs):
        args = list(args)
        level = kwargs.get('level', 'debug')

        args[0] = 'Protocol({}): '.format(self.game.player.uid) + args[0]

        getattr(logger, level)(*args)


class GameFactory(Factory):
    def __init__(self):
        logger.debug('%s instantiated', self.__class__.__name__)

    def buildProtocol(self, addr):
        logger.debug('Building a new protocol')
        return GameProtocol()


def run():
    logger.info('Starting dum telnet server')
    reactor.listenTCP(8123, GameFactory())
    reactor.run()

if __name__ == '__main__':
    run()
