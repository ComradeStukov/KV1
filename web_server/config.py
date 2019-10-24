# -*- encoding: utf-8 -*-

__author__ = "chenty"


test = True

template_folder = "front_end/modified"
host = "0.0.0.0"
port = 8493
debug = False
threaded = True
cors = False
secret_key = "jU5lYm6qGRRcGpLddaBp"

if test:
    template_folder = "../front_end/modified"
    host = "127.0.0.1"
    port = 8493
    debug = True
    threaded = True
    cors = True
    secret_key = "WFC0XsplPU03XqKXu3iu"
