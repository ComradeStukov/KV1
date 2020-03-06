# -*- encoding: utf-8 -*-

__author__ = "chenty"

from flask import Flask
from flask_cors import CORS

from server import config


app = Flask(__name__, template_folder=config.flask_args["template_folder"])
app.secret_key = config.flask_args["secret_key"]
app.jinja_env.variable_start_string = config.flask_args["jinja_variable_start_string"]
app.jinja_env.variable_end_string = config.flask_args["jinja_variable_end_string"]

if config.flask_args["cors"]:
    CORS(app, supports_credentials=True)
