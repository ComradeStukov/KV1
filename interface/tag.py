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

import re

from database.tag import Tag
from interface.utility import get_session, base_return_code


# Return code of interfaces
return_code = base_return_code.copy()
return_code.update({
    "TAG_NOT_EXIST": 200,
    "TAG_EXIST": 201
})

def check_tag_id(id):
    """
    Check whether an id is valid
    :param id: The id
    :return: The result
    """
    return isinstance(id, int) and 0 < id

def check_tag_name(name):
    """
    Check whether a tag name is valid
    :param name: The name
    :return: The result
    """
    return isinstance(name, str) and 0 < len(name) < 45

@get_session
def add_tag(name, session=None):
    """
    Add a tag to the database
    :param name: Tag name
    :param session: Auto filled database link session
    :return: If a session should commit, return code, tag id
    """
    # Check if all inputs are valid
    valid = check_tag_name(name)
    if not valid:
        return False, return_code["INVALID_DATA"], None
    # Check if there is any tag with the same name
    t_same_name = session.query(Tag).filter(Tag.name == name)
    if t_same_name.count():
        return False, return_code["TAG_EXIST"], None
    # Add the tag to the database
    t = Tag(name=name)
    session.add(t)
    session.flush()
    return True, return_code["OK"], {"id": t.id, "name": t.name}

@get_session
def delete_tag(id, session=None):
    """
    Delete a tag by its id
    :param id: Tag id
    :param session: Auto filled database link session
    :return: If a session should commit, return code, none
    """
    # Check if all inputs are valid
    valid = check_tag_id(id)
    if not valid:
        return False, return_code["INVALID_DATA"], None
    # Find and delete the tag
    t = session.query(Tag).filter(Tag.id == id)
    if not t.count():
        return False, return_code["TAG_NOT_EXIST"], None
    session.delete(t.first())
    return True, return_code["OK"], id

@get_session
def edit_tag(id, name, session=None):
    """
    Edit a tag
    :param id: Tag id
    :param name: Tag name
    :param session: Auto filled database link session
    :return: If a session should commit, return code, tag id and tag name
    """
    # Check if all inputs are valid
    valid = check_tag_id(id) and check_tag_name(name)
    if not valid:
        return False, return_code["INVALID_DATA"], None
    # Find the tag and modify it
    t = session.query(Tag).filter(Tag.id == id)
    if not t.count():
        return False, return_code["TAG_NOT_EXIST"], None
    t = t.first()
    # Check if there is any tag with the specified name
    t_same_name = session.query(Tag).filter(Tag.name == name)
    if t_same_name.count() and t_same_name.first().id != id:
        return False, return_code["TAG_EXIST"], None
    t.name = name
    return True, return_code["OK"], {"id": id, "name": name}

@get_session
def get_tags(ids, session=None):
    """
    Get tags with specified ids
    :param ids: List of ids
    :param session: Auto filled database link session
    :return: If a session should commit, return code, id and name of tags
    """
    # Check if all inputs are valid
    valid = isinstance(ids, list) and all([check_tag_id(x) for x in ids])
    if not valid:
        return False, return_code["INVALID_DATA"], None
    if not ids:
        return True, return_code["OK"], []
    # Find tags
    t = session.query(Tag).filter(Tag.id.in_(ids)).all()
    return True, return_code["OK"], [{"id": x.id, "name": x.name} for x in t]

@get_session
def find_tags(name_query, session=None):
    """
    Find tags by names
    :param name_query: Partial name
    :param session: Auto filled database link session
    :return: If a session should commit, return code, id and name of tags
    """
    # Check if all inputs are valid
    valid = True if not name_query else check_tag_name(name_query)
    if not valid:
        return False, return_code["INVALID_DATA"], None
    # Find tags by names and return them
    q = session.query(Tag)
    if name_query:
        name_query = re.sub(r"\s+", "%", " " + name_query.replace("%", " ") + " ")
        q = q.filter(Tag.name.ilike(name_query))
    t = q.all()
    return True, return_code["OK"], [{"id": x.id, "name": x.name} for x in t]
