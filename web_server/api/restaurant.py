# -*- encoding: utf-8 -*-

__author__ = "chenty"

from flask import request, Response, session
from json import dumps

from web_server.base import app
from interface import restaurant


@app.route("/api/test", methods=["GET"])
def api_test():
    return "API Module is running."

@app.route("/api/add_restaurant", methods=["POST"])
def api_add_restaurant():
    data = request.get_json()
    code, res = restaurant.add_restaurant(
        data["name"],
        data["branch"],
        data["postcode"],
        data["price"],
        data["note"],
        data["tags"]
    )
    resp = dumps({"code": code, "res": res})
    return Response(resp, mimetype="application/json")

@app.route("/api/delete_restaurant", methods=["POST"])
def api_delete_restaurant():
    data = request.get_json()
    code, res = restaurant.delete_restaurant(data["id"])
    resp = dumps({"code": code, "res": res})
    return Response(resp, mimetype="application/json")

@app.route("/api/edit_restaurant", methods=["POST"])
def api_edit_restaurant():
    data = request.get_json()
    code, res = restaurant.edit_restaurant(
        data["id"],
        data["name"],
        data["branch"],
        data["postcode"],
        data["price"],
        data["note"],
        data["tags"]
    )
    resp = dumps({"code": code, "res": res})
    return Response(resp, mimetype="application/json")

@app.route("/api/get_restaurant", methods=["POST"])
def api_get_restaurant():
    data = request.get_json()
    code, res = restaurant.get_restaurant(data["id"])
    resp = dumps({"code": code, "res": res})
    return Response(resp, mimetype="application/json")

@app.route("/api/find_restaurants", methods=["POST"])
def api_find_restaurants():
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
