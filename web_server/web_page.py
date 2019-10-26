# -*- encoding: utf-8 -*-

__author__ = "chenty"

from flask import request, send_from_directory, render_template
from json import loads

from web_server.base import app
from web_server.config import test


@app.route("/", methods=["GET"])
def web_index():
    return render_template("index.html")

@app.route("/add_restaurant", methods=["GET"])
def web_add_restaurant():
    return render_template("add_restaurant.html")

@app.route("/find_restaurants", methods=["GET"])
def web_find_restaurants():
    search = request.args.get("search", None)
    if search:
        search = loads(search)
    else:
        search = {}
    return render_template("find_restaurants.html", search=search, page=request.args.get("page", 1))

@app.route("/get_restaurant", methods=["GET"])
def web_get_restaurant():
    return render_template("get_restaurant.html", id=request.args["id"])

@app.route("/edit_restaurant", methods=["GET"])
def web_edit_restaurant():
    return render_template("edit_restaurant.html", id=request.args["id"])

@app.route("/find_tags", methods=["GET"])
def web_find_tags():
    return render_template("find_tags.html")

@app.route("/cart", methods=["GET"])
def web_cart():
    return render_template("cart.html")

@app.route("/result", methods=["GET"])
def web_result():
    return render_template("result.html")

if test:
    @app.route("/res/<path:path>", methods=["GET"])
    def test_web_res_file(path):
        return send_from_directory("../front_end/modified/res", path)
