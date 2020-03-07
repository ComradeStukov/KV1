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
from json import dumps

from server.base import app
from interface import tag


@app.route("/api/add_tag", methods=["POST"])
def api_add_tag():
    """
    Flask response function
    Add a tag to the database
    :return: Flask response
    """
    # Get the tag and add it
    data = request.get_json()
    code, res = tag.add_tag(data["name"])
    resp = dumps({"code": code, "res": res})
    return Response(resp, mimetype="application/json")

@app.route("/api/delete_tag", methods=["POST"])
def api_delete_tag():
    """
    Flask response function
    Delete a tag from the database
    :return: Flask response
    """
    # Get the tag id and delete it
    data = request.get_json()
    code, res = tag.delete_tag(data["id"])
    resp = dumps({"code": code, "res": res})
    return Response(resp, mimetype="application/json")

@app.route("/api/edit_tag", methods=["POST"])
def api_edit_tag():
    """
    Flask response function
    Edit a tag name
    :return: Flask response
    """
    # Modify the name of the tag
    data = request.get_json()
    code, res = tag.edit_tag(data["id"], data["name"])
    resp = dumps({"code": code, "res": res})
    return Response(resp, mimetype="application/json")

@app.route("/api/get_tags", methods=["POST"])
def api_get_tags():
    """
    Flask response function
    Get tags by id
    :return: Flask response
    """
    # Get the list of the id and then get all corresponding tags
    data = request.get_json()
    code, res = tag.get_tags(data.get("ids", []))
    resp = dumps({"code": code, "res": res})
    return Response(resp, mimetype="application/json")

@app.route("/api/find_tags", methods=["POST"])
def api_find_tags():
    """
    Flask response function
    Find tags by partial names
    :return: Flask response
    """
    # Get the name condition and find tags
    data = request.get_json()
    code, res = tag.find_tags(data.get("name_query", ""))
    resp = dumps({"code": code, "res": res})
    return Response(resp, mimetype="application/json")
