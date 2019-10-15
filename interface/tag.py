# -*- encoding: utf-8 -*-

__author__ = "chenty"

import re

from database.tag import Tag
from interface.utility import get_session, base_return_code


return_code = base_return_code.copy()
return_code.update({
    "TAG_NOT_EXIST": 200,
    "TAG_EXIST": 201
})

def check_tag_id(id):
    return isinstance(id, int) and 0 < id

def check_tag_name(name):
    return isinstance(name, str) and 0 < len(name) < 45

@get_session
def add_tag(name, session=None):
    valid = check_tag_name(name)
    if not valid:
        return False, return_code["INVALID_DATA"], None
    t_same_name = session.query(Tag).filter(Tag.name == name)
    if t_same_name.count():
        return False, return_code["TAG_EXIST"], None
    t = Tag(name=name)
    session.add(t)
    session.flush()
    return True, return_code["OK"], {"id": t.id, "name": t.name}

@get_session
def delete_tag(id, session=None):
    valid = check_tag_id(id)
    if not valid:
        return False, return_code["INVALID_DATA"], None
    t = session.query(Tag).filter(Tag.id == id)
    if not t.count():
        return False, return_code["TAG_NOT_EXIST"], None
    session.delete(t.first())
    return True, return_code["OK"], id

@get_session
def edit_tag(id, name, session=None):
    valid = check_tag_id(id) and check_tag_name(name)
    if not valid:
        return False, return_code["INVALID_DATA"], None
    t = session.query(Tag).filter(Tag.id == id)
    if not t.count():
        return False, return_code["TAG_NOT_EXIST"], None
    t = t.first()
    t_same_name = session.query(Tag).filter(Tag.name == name)
    if t_same_name.count() and t_same_name.first().id != id:
        return False, return_code["TAG_EXIST"], None
    t.name = name
    return True, return_code["OK"], {"id": id, "name": name}

@get_session
def get_tags(ids, session=None):
    valid = isinstance(ids, list) and all([check_tag_id(x) for x in ids])
    if not valid:
        return False, return_code["INVALID_DATA"], None
    if not ids:
        return True, return_code["OK"], []
    q = session.query(Tag)
    if ids:
        q = q.filter(Tag.id.in_(ids))
    t = q.all()
    return True, return_code["OK"], [{"id": x.id, "name": x.name} for x in t]

@get_session
def find_tags(name_query, session=None):
    valid = True if not name_query else check_tag_name(name_query)
    if not valid:
        return False, return_code["INVALID_DATA"], None
    q = session.query(Tag)
    if name_query:
        name_query = re.sub(r"\s+", "%", " " + name_query.replace("%", " ") + " ")
        q = q.filter(Tag.name.ilike(name_query))
    t = q.all()
    return True, return_code["OK"], [{"id": x.id, "name": x.name} for x in t]
