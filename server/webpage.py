# -*- coding: utf-8 -*-

# The MIT License (MIT)
# Copyright (c) 2020 SBofGaySchoolBuPaAnything
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

__author__ = "chenty"

from flask import request, send_from_directory, render_template
from json import loads

from server.base import app


@app.route("/", methods=["GET"])
def web_index():
    """
    Flask response function
    Render index page
    :return: Rendered HTML
    """
    return render_template("index.html")

@app.route("/add_restaurant", methods=["GET"])
def web_add_restaurant():
    """
    Flask response function
    Render add restaurant page
    :return: Rendered HTML
    """
    return render_template("add_restaurant.html")

@app.route("/find_restaurants", methods=["GET"])
def web_find_restaurants():
    """
    Flask response function
    Render find restaurant page
    :return: Rendered HTML
    """
    # Load search conditions
    search = request.args.get("search", None)
    if search:
        search = loads(search)
    else:
        search = {}
    # Load current page and return the HTML
    return render_template("find_restaurants.html", search=search, page=request.args.get("page", 1))

@app.route("/get_restaurant", methods=["GET"])
def web_get_restaurant():
    """
    Flask response function
    Render get restaurant page
    :return: Rendered HTML
    """
    # Load restaurant id and return the HTML
    return render_template("get_restaurant.html", id=request.args["id"])

@app.route("/edit_restaurant", methods=["GET"])
def web_edit_restaurant():
    """
    Flask response function
    Render edit restaurant page
    :return: Rendered HTML
    """
    # Load restaurant id and return the HTML
    return render_template("edit_restaurant.html", id=request.args["id"])

@app.route("/find_tags", methods=["GET"])
def web_find_tags():
    """
    Flask response function
    Render find tag page
    :return: Rendered HTML
    """
    return render_template("find_tags.html")

@app.route("/cart", methods=["GET"])
def web_cart():
    """
    Flask response function
    Render cart page
    :return: Rendered HTML
    """
    return render_template("cart.html")

@app.route("/result", methods=["GET"])
def web_result():
    """
    Flask response function
    Render restaurant selection result page
    :return: Rendered HTML
    """
    return render_template("result.html")

@app.route("/favicon.ico", methods=["GET"])
def web_favicon():
    """
    Flask response function
    Fetch the icon
    :return: Static file
    """
    return send_from_directory("webpage/res", "icon/D.ico")

@app.route("/res/<path:path>", methods=["GET"])
def web_res_file(path):
    """
    Flask response function
    Fetch a static file
    :return: Static file
    """
    return send_from_directory("webpage/res", path)
