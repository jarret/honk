#!/usr/bin/env python3

import os
import sys
import logging
import inspect
import argparse
import txaio

from OpenSSL import SSL


from twisted.internet import reactor, ssl
from twisted.python import log

from twisted.logger import Logger, LogLevel

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

def log_dump(event):
    if event['log_namespace'] == 'stdout':
        return
    print("dumpp: %s" % event)


if __name__ == '__main__':
    txaio.start_logging(level='debug')
    log.startLogging(sys.stdout)
    #log.addObserver(log_dump)

    parser = argparse.ArgumentParser(prog="clear.py")
    parser.add_argument('-p', "--port", type=int, default=443,
                        help="port to listen on (default=443)")
    parser.add_argument('-c', "--cert-dir", type=str, default="cert/",
                        help="directory w/ cert.key and cert.pem (default=cert/)")
    s = parser.parse_args()

    cert_key = os.path.join(s.cert_dir, "cert.key")
    cert_pem = os.path.join(s.cert_dir, "cert.pem")
    contextFactory = ssl.DefaultOpenSSLContextFactory(
        cert_key, cert_pem, sslmethod=SSL.TLSv1_2_METHOD)
    factory = WebSocketServerFactory(u"wss://127.0.0.1:%s" % s.port)
    factory.setProtocolOptions(trustXForwardedFor=1)
    factory.protocol = TlsHonkServerProtocol

    listenWS(factory, contextFactory)

    reactor.run()
