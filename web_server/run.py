# -*- encoding: utf-8 -*-

__author__ = "chenty"

from web_server import config
from web_server.base import app
import web_server.api
from interface.utility import end_session
from database.initialize import initialize


def run():
    app.run(host=config.host, port=config.port, debug=config.debug, threaded=config.threaded)
    end_session()
    return

if __name__ == "__main__":
    initialize()
    run()
