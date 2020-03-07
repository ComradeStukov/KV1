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

from flask import request, Response
from json import dumps, loads
from requests import get

from server.base import app
from interface import restaurant, utility


# Return code of interfaces
return_code = utility.base_return_code
return_code.update(
    {
        "COORD_NOT_FOUND": 150
    }
)

@app.route("/api/test", methods=["GET"])
def api_test():
    """
    Flask response function
    Check if the module is running
    :return: Plain text
    """
    return "HTTP API Module is running."

@app.route("/api/add_restaurant", methods=["POST"])
def api_add_restaurant():
    """
    Flask response function
    Add a restaurant to the database
    :return: Flask response
    """
    # Get the restaurant and add it
    data = request.get_json()
    code, res = restaurant.add_restaurant(
        data["name"],
        data["branch"],
        data["postcode"].replace(" ", ""),
        data["price"],
        data["note"],
        data["tags"]
    )
    resp = dumps({"code": code, "res": res})
    return Response(resp, mimetype="application/json")

@app.route("/api/delete_restaurant", methods=["POST"])
def api_delete_restaurant():
    """
    Flask response function
    Delete a restaurant from the database
    :return: Flask response
    """
    # Get the restaurant and delete it
    data = request.get_json()
    code, res = restaurant.delete_restaurant(data["id"])
    resp = dumps({"code": code, "res": res})
    return Response(resp, mimetype="application/json")

@app.route("/api/edit_restaurant", methods=["POST"])
def api_edit_restaurant():
    """
    Flask response function
    Edit a restaurant
    :return: Flask response
    """
    # Get data of the restaurant and edit it
    data = request.get_json()
    code, res = restaurant.edit_restaurant(
        data["id"],
        data["name"],
        data["branch"],
        data["postcode"].replace(" ", ""),
        data["price"],
        data["note"],
        data["tags"]
    )
    resp = dumps({"code": code, "res": res})
    return Response(resp, mimetype="application/json")

@app.route("/api/get_restaurant", methods=["POST"])
def api_get_restaurant():
    """
    Flask response function
    Get a restaurant from the database
    :return: Flask response
    """
    # Get the restaurant id and fetch the restaurant
    data = request.get_json()
    code, res = restaurant.get_restaurant(data["id"])
    resp = dumps({"code": code, "res": res})
    return Response(resp, mimetype="application/json")

@app.route("/api/find_restaurants", methods=["POST"])
def api_find_restaurants():
    """
    Flask response function
    Find restaurants according to conditions
    :return: Flask response
    """
    # Get the conditions and find the restaurant
    data = request.get_json()
    code, res = restaurant.find_restaurants(
        data.get("name_query", ""),
        data.get("postcode_prefix", ""),
        data.get("min_price", None),
        data.get("max_price", None),
        data.get("tags", []),
        data.get("page", 1),
    )
    resp = dumps({"code": code, "res": res})
    return Response(resp, mimetype="application/json")

@app.route("/api/get_postcode_coord", methods=["POST"])
def api_get_postcode_coord():
    """
    Flask response function
    Get a coordination of a UK postcode
    :return: Flask response
    """
    # Get the postcode
    postcode = request.get_json()["postcode"]
    if not restaurant.check_restaurant_postcode(postcode):
        return Response(dumps({"code": return_code["INVALID_DATA"]}), mimetype="application/json")
    try:
        # Request it through api.postcodes.io
        r = loads(get("http://api.postcodes.io/postcodes/" + postcode).text)["result"]
        return Response(dumps({
            "code": return_code["OK"],
            "res": [r["longitude"], r["latitude"]]
        }), mimetype="application/json")
    except:
        return Response(dumps({"code": return_code["COORD_NOT_FOUND"]}))
