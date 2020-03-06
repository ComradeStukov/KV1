# -*- encoding: utf-8 -*-

__author__ = "chenty"

from flask import request, Response
from json import dumps

from server.base import app
from interface import tag


@app.route("/api/add_tag", methods=["POST"])
def api_add_tag():
    data = request.get_json()
    code, res = tag.add_tag(data["name"])
    resp = dumps({"code": code, "res": res})
    return Response(resp, mimetype="application/json")

@app.route("/api/delete_tag", methods=["POST"])
def api_delete_tag():
    data = request.get_json()
    code, res = tag.delete_tag(data["id"])
    resp = dumps({"code": code, "res": res})
    return Response(resp, mimetype="application/json")

@app.route("/api/edit_tag", methods=["POST"])
def api_edit_tag():
    data = request.get_json()
    code, res = tag.edit_tag(data["id"], data["name"])
    resp = dumps({"code": code, "res": res})
    return Response(resp, mimetype="application/json")

@app.route("/api/get_tags", methods=["POST"])
def api_get_tags():
    data = request.get_json()
    code, res = tag.get_tags(data.get("ids", []))
    resp = dumps({"code": code, "res": res})
    return Response(resp, mimetype="application/json")

@app.route("/api/find_tags", methods=["POST"])
def api_find_tags():
    data = request.get_json()
    code, res = tag.find_tags(data.get("name_query", ""))
    resp = dumps({"code": code, "res": res})
    return Response(resp, mimetype="application/json")
