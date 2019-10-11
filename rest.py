#!/usr/bin/env python3

from flask import Flask, make_response
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS

from http import HTTPStatus as h

###############################################################################

HTTP_STATUS_CODES = {
    'OK':                    h.OK,
    'Created':               h.CREATED,
    'Bad Request':           h.BAD_REQUEST,
    'Not Found':             h.NOT_FOUND,
    'Internal Server Error': h.INTERNAL_SERVER_ERROR,
    'Method Not Allowed':    h.METHOD_NOT_ALLOWED,
}

def http_status(status):
    assert status in HTTP_STATUS_CODES.keys(), "status not defined for app"
    return HTTP_STATUS_CODES[status]

###############################################################################

HONK_HELP = """Title of the art - limit 64 bytes"""

def honk(parser):
    parser.add_argument('honk', type=str, help=HONK_HELP)

def honk_validate(args):
    if not args.honk:
        return False, "no honks given"
    if len(args.honk) > 15:
        return False, "to wordy. Honky honk honk."
    return True, None

REST_ARGS = {
    'honk':         {'add':           honk,
                     'validate':      honk_validate},
}

###############################################################################

class Honk(Resource):
    PATH ="/honk"
    EXPECTED_ARGS = ["honk"]

    def _validate_args(self, args):
        for a in self.EXPECTED_ARGS:
            v, e = REST_ARGS[a]['validate'](args)
            if not v:
                return e
        return None

    def _parse_args(self):
        parser = reqparse.RequestParser()
        for a in self.EXPECTED_ARGS:
            REST_ARGS[a]['add'](parser)
        args = parser.parse_args()
        e = self._validate_args(args)
        if e:
            return None, e
        return args, None

    def get(self):
        args, err = self._parse_args()
        if err:
            return {'err': err}, http_status("Bad Request")

        return {'honk': args.honk}, http_status("OK")

###############################################################################

REST_RESOURCES = [Honk]

if __name__ == '__main__':
    app = Flask("honk")
    CORS(app)
    api = Api(app)
    for r in REST_RESOURCES:
        api.add_resource(r, r.PATH)
    app.run(debug=True, use_reloader=False, port=8080, host="0.0.0.0")
