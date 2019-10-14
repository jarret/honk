#!/usr/bin/env python3

from requests import get

HOST = "localhost"
PORT = 8000

if __name__ == '__main__':

    res = get("http://%s:%d/%s" % (HOST, PORT, "honk"),
              data={'honk': "Honky Honk!"})
    print(res.json())
