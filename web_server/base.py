# -*- encoding: utf-8 -*-

__author__ = "chenty"

from flask import Flask

from web_server import config


app = Flask(__name__, template_folder=config.template_folder)
app.jinja_env.variable_start_string = '[['
app.jinja_env.variable_end_string = ']]'
