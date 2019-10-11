# -*- encoding: utf-8 -*-

__author__ = "chenty"

from flask import request, Response
from json import dumps

from web_server.base import app
from interface import restaurant, tag


@app.route("/api/test", methods=["GET"])
def test():
    return "API Module is running."

@app.route("/api/add_restaurant", methods=["POST"])
def add_restaurant():
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
def delete_restaurant():
    data = request.get_json()
    code, res = restaurant.delete_restaurant(data["id"])
    resp = dumps({"code": code, "res": res})
    return Response(resp, mimetype="application/json")

@app.route("/api/edit_restaurant", methods=["POST"])
def edit_restaurant():
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
def get_restaurant():
    data = request.get_json()
    code, res = restaurant.get_restaurant(data["id"])
    resp = dumps({"code": code, "res": res})
    return Response(resp, mimetype="application/json")

@app.route("/api/find_restaurants", methods=["POST"])
def find_restaurants():
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

@app.route("/api/get_restaurants_name_branch")
def get_restaurants_name_branch():
    data = request.get_json()
    code, res = restaurant.get_restaurants_name_branch(data.get("ids", []))
    resp = dumps({"code": code, "res": res})
    return Response(resp, mimetype="application/json")

@app.route("/api/add_tag", methods=["POST"])
def add_tag():
    data = request.get_json()
    code, res = tag.add_tag(data["name"])
    resp = dumps({"code": code, "res": res})
    return Response(resp, mimetype="application/json")

@app.route("/api/delete_tag", methods=["POST"])
def delete_tag():
    data = request.get_json()
    code, res = tag.delete_tag(data["id"])
    resp = dumps({"code": code, "res": res})
    return Response(resp, mimetype="application/json")

@app.route("/api/edit_tag", methods=["POST"])
def edit_tag():
    data = request.get_json()
    code, res = tag.edit_tag(data["id"], data["name"])
    resp = dumps({"code": code, "res": res})
    return Response(resp, mimetype="application/json")

@app.route("/api/find_tags", methods=["POST"])
def find_tags():
    data = request.get_json()
    code, res = tag.find_tags(data.get("name_query", ""))
    resp = dumps({"code": code, "res": res})
    return Response(resp, mimetype="application/json")
