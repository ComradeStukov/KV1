# -*- encoding: utf-8 -*-

__author__ = "chenty"

from flask_cors import CORS

from web_server import config
from web_server.base import app

from web_server.api import restaurant, tag, cart
import web_server.web_page


if config.cors:
    CORS(app, supports_credentials=True)
app.secret_key = config.secret_key

if __name__ == "__main__":
    from database.initialize import initialize
    from interface.utility import end_session
    initialize()
    app.run(host=config.host, port=config.port, debug=config.debug, threaded=config.threaded)
    end_session()
