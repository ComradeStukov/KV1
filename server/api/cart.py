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

from flask import request, Response, session
from json import dumps
from random import choice

from server.base import app
from interface import restaurant, utility


# Return code of interfaces
return_code = utility.base_return_code
return_code.update(
    {
        "EMPTY_CART": 300
    }
)

def check_delta(delta):
    """
    Check whether a weight adjustment delta is valid
    :param delta: The weight adjustment
    :return: The result
    """
    return delta == -1 or delta == 1

def check_session_restaurant(r=None):
    """
    Check if all restaurant id stored in the session are included in the given list, and remove those excluded
    :param r: The given list of id
    :return: None
    """
    # Get all restaurant id in the session
    original_id = list(int(x) for x in session.keys() if x.isdigit())
    # If list is not specified, let ids of all restaurants to be the list
    if r is None:
        code, r = restaurant.get_restaurants(original_id)
        if code !=return_code["OK"]:
            return
    ids = set(x["id"] for x in r)
    # Remove those id which is in the session but not in the list
    for k in original_id:
        if k not in ids:
            session.pop(str(k), None)
    return

@app.route("/api/add_cart", methods=["POST"])
def api_add_cart():
    """
    Flask response function
    Add a restaurant id to the cart
    :return: Flask response
    """
    # Get the id
    data = request.get_json()
    id = data["id"]
    # Check if it is valid
    if not restaurant.check_restaurant_id(id):
        return Response(dumps({"code": return_code["INVALID_DATA"]}), mimetype="application/json")
    id = str(id)
    # Add it to the cart in the session
    session[id] = session.get(id, 0) + 1
    return Response(dumps({"code": return_code["OK"], "res": None}), mimetype="application/json")

@app.route("/api/delete_cart", methods=["POST"])
def api_delete_cart():
    """
    Flask response function
    Delete a restaurant id from the cart
    :return: Flask response
    """
    # Get the id
    data = request.get_json()
    id = data["id"]
    # Check if it is valid
    if not restaurant.check_restaurant_id(id):
        return Response(dumps({"code": return_code["INVALID_DATA"]}), mimetype="application/json")
    id = str(id)
    # Delete it
    session.pop(id, None)
    return Response(dumps({"code": return_code["OK"], "res": None}), mimetype="application/json")

@app.route("/api/edit_cart", methods=["POST"])
def api_edit_cart():
    """
    Flask response function
    Edit the weight of a restaurant in the cart
    :return: Flask response
    """
    # Get the id and weight adjustment
    data = request.get_json()
    id, delta = data["id"], data["delta"]
    # Check if them are valid
    if not (restaurant.check_restaurant_id(id) and check_delta(delta)):
        return Response(dumps({"code": return_code["INVALID_DATA"]}), mimetype="application/json")
    id = str(id)
    # Adjust the weight
    session[id] = max(session.get(id, 0) + delta, 1)
    return Response(dumps({"code": return_code["OK"], "res": None}), mimetype="application/json")

@app.route("/api/get_cart", methods=["POST"])
def api_get_cart():
    """
    Flask response function
    Get all restaurants in the cart
    :return: Flask response
    """
    # Get all restaurants in the cart
    code, r = restaurant.get_restaurants(list(int(x) for x in session.keys() if x.isdigit()))
    if code != return_code["OK"]:
        return Response(dumps({"code": code, "res": r}), mimetype="application/json")
    # Remove those invalid (those restaurant deleted from the database but still in the cart)
    check_session_restaurant(r=r)
    # Get their weights which are stored in the session
    for x in r:
        x["weight"] = session.get(str(x["id"]), 0)
    return Response(dumps({"code": return_code["OK"], "res": r}), mimetype="application/json")

@app.route("/api/clean_cart", methods=["POST"])
def api_clean_cart():
    """
    Flask response function
    Clean the cart
    :return: Flask response
    """
    # Remove all restaurant id in the cart
    ids = list(str(x) for x in session.keys() if x.isdigit)
    for id in ids:
        session.pop(id, None)
    return Response(dumps({"code": return_code["OK"], "res": None}), mimetype="application/json")

@app.route("/api/get_result", methods=["POST"])
def api_get_result():
    """
    Flask response function
    Get result of restaurant selection
    :return: Flask response
    """
    # If the result is not selected
    if "result" not in session:
        # Remove all invalid restaurant id
        check_session_restaurant()
        # Put those id with weight in a list
        opt = []
        for k, v in session.items():
            if not k.isdigit():
                continue
            opt += [int(k)] * v
        if not opt:
            return Response(dumps({"code": return_code["EMPTY_CART"], "res": None}), mimetype="application/json")
        # Randomly choose one
        session["result"] = choice(opt)
    # Return the result
    code, res = restaurant.get_restaurant(session["result"])
    return Response(dumps({"code": code, "res": res}), mimetype="application/json")

@app.route("/api/clean_result", methods=["POST"])
def api_clean_result():
    """
    Flask response function
    Clean the selection result
    :return: Flask response
    """
    # Remove the result
    session.pop("result", None)
    return Response(dumps({"code": return_code["OK"], "res": None}), mimetype="application/json")
