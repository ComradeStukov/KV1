# -*- encoding: utf-8 -*-

__author__ = "chenty"


test = True

host = "0.0.0.0"
port = 8493
debug = False
threaded = True
cors = False

if test:
    host = "127.0.0.1"
    port = 8493
    debug = True
    threaded = True
    cors = True
