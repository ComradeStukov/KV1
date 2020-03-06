# -*- encoding: utf-8 -*-

__author__ = "chenty"

from flask import request, Response
from json import dumps, loads
from requests import get

from server.base import app
from interface import restaurant, utility


return_code = utility.base_return_code
return_code.update(
    {
        "COORD_NOT_FOUND": 150
    }
)

@app.route("/api/test", methods=["GET"])
def api_test():
    return "API Module is running."

@app.route("/api/add_restaurant", methods=["POST"])
def api_add_restaurant():
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
        data["postcode"].replace(" ", ""),
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

@app.route("/api/get_postcode_coord", methods=["POST"])
def api_get_postcode_coord():
    postcode = request.get_json()["postcode"]
    if not restaurant.check_restaurant_postcode(postcode):
        return Response(dumps({"code": return_code["INVALID_DATA"]}), mimetype="application/json")
    try:
        r = loads(get("http://api.postcodes.io/postcodes/" + postcode).text)["result"]
        return Response(dumps({
            "code": return_code["OK"],
            "res": [r["longitude"], r["latitude"]]
        }), mimetype="application/json")
    except:
        return Response(dumps({"code": return_code["COORD_NOT_FOUND"]}))
