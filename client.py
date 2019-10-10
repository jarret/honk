#!/usr/bin/env python3

import sys

from twisted.python import log
from twisted.internet import reactor, ssl

from autobahn.twisted.websocket import WebSocketClientFactory
from autobahn.twisted.websocket import WebSocketClientProtocol
from autobahn.twisted.websocket import connectWS

from twisted.python.modules import getModule

class TlsHonkClientProtocol(WebSocketClientProtocol):

    def sendHello(self):
        self.sendMessage("Honk!".encode('utf8'))

    def onOpen(self):
        self.sendHello()

    def onMessage(self, payload, isBinary):
        if not isBinary:
            print("Text message received: {}".format(payload.decode('utf8')))
        reactor.callLater(1, self.sendHello)

HONK_WSS = "wss://localhost:4443/howdy"
#HONK_WSS = "wss://ws.rarepepemuseum.com:443"

if __name__ == '__main__':
    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory(HONK_WSS)
    factory.protocol = TlsHonkClientProtocol

    if factory.isSecure:
        contextFactory = ssl.ClientContextFactory()
    else:
        contextFactory = None

    connectWS(factory, contextFactory)
    reactor.run()
