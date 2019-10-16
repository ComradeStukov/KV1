# -*- encoding: utf-8 -*-

__author__ = "chenty"

from flask import send_from_directory

from web_server.base import app


@app.route("/<path:path>")
def static_file(path):
    return send_from_directory("../front_end/modified", path)
