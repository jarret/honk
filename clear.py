#!/usr/bin/env python3

import sys
import argparse

from twisted.internet import reactor
from twisted.python import log

from autobahn.twisted.websocket import WebSocketServerFactory
from autobahn.twisted.websocket import WebSocketServerProtocol
from autobahn.twisted.websocket import listenWS


class ClearHonkServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("WebSocket connection request: %s" % request)

    def onOpen(self):
        print("WebSocket connection open")

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed %s %s %s" % (wasClean, code, reason))

    def onMessage(self, payload, isBinary):
        print("WebSocket message: %s" % payload)
        self.sendMessage(payload, isBinary)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="clear.py")
    parser.add_argument('-p', "--port", type=int, default=80,
                        help="port to listen on (default=80)")
    s = parser.parse_args()

    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory(u"ws://127.0.0.1:%s" % s.port)
    factory.protocol = ClearHonkServerProtocol

    listenWS(factory)

    reactor.run()
