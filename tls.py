#!/usr/bin/env python3

import os
import sys
import argparse

from twisted.internet import reactor, ssl
from twisted.python import log

from autobahn.twisted.websocket import WebSocketServerFactory
from autobahn.twisted.websocket import WebSocketServerProtocol
from autobahn.twisted.websocket import listenWS

class TlsHonkServerProtocol(WebSocketServerProtocol):

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
    parser.add_argument('-p', "--port", type=int, default=443,
                        help="port to listen on (default=443)")
    parser.add_argument('-c', "--cert-dir", type=str, default="cert/",
                        help="directory w/ cert.key and cert.pem (default=cert/)")
    s = parser.parse_args()

    log.startLogging(sys.stdout)
    cert_key = os.path.join(s.cert_dir, "cert.key")
    cert_pem = os.path.join(s.cert_dir, "cert.pem")
    contextFactory = ssl.DefaultOpenSSLContextFactory(cert_key, cert_pem)
    factory = WebSocketServerFactory(u"wss://127.0.0.1:%s" % s.port)
    factory.setProtocolOptions(trustXForwardedFor=1)
    factory.protocol = TlsHonkServerProtocol

    listenWS(factory, contextFactory)

    reactor.run()
