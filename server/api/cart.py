# -*- encoding: utf-8 -*-

__author__ = "chenty"

from flask import request, Response, session
from json import dumps
from random import choice

from server.base import app
from interface import restaurant, utility


return_code = utility.base_return_code
return_code.update(
    {
        "EMPTY_CART": 300
    }
)

def check_delta(delta):
    return delta == -1 or delta == 1

def check_session_restaurant(r=None):
    original_id = list(int(x) for x in session.keys() if x.isdigit())
    if r is None:
        code, r = restaurant.get_restaurants(original_id)
        if code !=return_code["OK"]:
            return
    ids = set(x["id"] for x in r)
    for k in original_id:
        if k not in ids:
            session.pop(str(k), None)
    return

@app.route("/api/add_cart", methods=["POST"])
def api_add_cart():
    data = request.get_json()
    id = data["id"]
    if not restaurant.check_restaurant_id(id):
        return Response(dumps({"code": return_code["INVALID_DATA"]}), mimetype="application/json")
    id = str(id)
    session[id] = session.get(id, 0) + 1
    return Response(dumps({"code": return_code["OK"], "res": None}), mimetype="application/json")

@app.route("/api/delete_cart", methods=["POST"])
def api_delete_cart():
    data = request.get_json()
    id = data["id"]
    if not restaurant.check_restaurant_id(id):
        return Response(dumps({"code": return_code["INVALID_DATA"]}), mimetype="application/json")
    id = str(id)
    session.pop(id, None)
    return Response(dumps({"code": return_code["OK"], "res": None}), mimetype="application/json")

@app.route("/api/edit_cart", methods=["POST"])
def api_edit_cart():
    data = request.get_json()
    id, delta = data["id"], data["delta"]
    if not (restaurant.check_restaurant_id(id) and check_delta(delta)):
        return Response(dumps({"code": return_code["INVALID_DATA"]}), mimetype="application/json")
    id = str(id)
    session[id] = max(session.get(id, 0) + delta, 1)
    return Response(dumps({"code": return_code["OK"], "res": None}), mimetype="application/json")

@app.route("/api/get_cart", methods=["POST"])
def api_get_cart():
    code, r = restaurant.get_restaurants(list(int(x) for x in session.keys() if x.isdigit()))
    if code != return_code["OK"]:
        return Response(dumps({"code": code, "res": r}), mimetype="application/json")
    check_session_restaurant(r=r)
    for x in r:
        x["weight"] = session.get(str(x["id"]), 0)
    return Response(dumps({"code": return_code["OK"], "res": r}), mimetype="application/json")

@app.route("/api/clean_cart", methods=["POST"])
def api_clean_cart():
    ids = list(str(x) for x in session.keys() if x.isdigit)
    for id in ids:
        session.pop(id, None)
    return Response(dumps({"code": return_code["OK"], "res": None}), mimetype="application/json")

@app.route("/api/get_result", methods=["POST"])
def api_get_result():
    if "result" not in session:
        check_session_restaurant()
        opt = []
        for k, v in session.items():
            if not k.isdigit():
                continue
            opt += [int(k)] * v
        if not opt:
            return Response(dumps({"code": return_code["EMPTY_CART"], "res": None}), mimetype="application/json")
        session["result"] = choice(opt)
    code, res = restaurant.get_restaurant(session["result"])
    return Response(dumps({"code": code, "res": res}), mimetype="application/json")

@app.route("/api/clean_result", methods=["POST"])
def api_clean_result():
    session.pop("result", None)
    return Response(dumps({"code": return_code["OK"], "res": None}), mimetype="application/json")
