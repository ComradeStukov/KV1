# -*- encoding: utf-8 -*-

__author__ = "chenty"

from flask_cors import CORS

from web_server import config
from web_server.base import app
from interface.utility import end_session
from database.initialize import initialize

from web_server.api import restaurant, tag, cart
import web_server.web_page

def run():
    if config.cors:
        CORS(app, supports_credentials=True)
    app.secret_key = config.secret_key

    app.run(host=config.host, port=config.port, debug=config.debug, threaded=config.threaded)
    end_session()
    return

if __name__ == "__main__":
    initialize()
    run()
