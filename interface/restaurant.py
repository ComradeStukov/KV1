# -*- encoding: utf-8 -*-

__author__ = "chenty"

from datetime import datetime
import re

from database.restaurant import Restaurant
from database.tag import Tag
from interface.tag import check_tag_id
from interface.utility import get_session, base_return_code


# Todo: Add logging system.
# Todo: Add comment.

return_code = base_return_code.copy()
return_code.update({
    "RESTAURANT_NOT_EXIST": 100,
    "RESTAURANT_EXIST": 101,
})
restaurant_per_page = 20

def check_restaurant_id(id):
    return isinstance(id, int) and 0 < id

def check_restaurant_name(name):
    return isinstance(name, str) and 0 < len(name) < 45

def check_restaurant_branch(branch):
    return isinstance(branch, str) and 0 <= len(branch) < 45

def check_restaurant_postcode(postcode):
    return isinstance(postcode, str) and re.match(r"^[0-9A-Za-z]{0,12}$", postcode)

def check_restaurant_price(price):
    return isinstance(price, int) and 0 <= price <= 400

def check_restaurant_note(note):
    return isinstance(note, str) and 0 <= len(note)

@get_session
def add_restaurant(name, branch, postcode, price, note, tags, session=None):
    valid = \
        check_restaurant_name(name) and\
        check_restaurant_branch(branch) and\
        check_restaurant_postcode(postcode) and\
        check_restaurant_price(price) and\
        check_restaurant_note(note) and \
        isinstance(tags, list) and all([check_tag_id(x) for x in tags])
    if not valid:
        return False, return_code["INVALID_DATA"], None
    r_same_name = session.query(Restaurant).filter(Restaurant.name == name, Restaurant.branch == branch)
    if r_same_name.count():
        return False, return_code["RESTAURANT_EXIST"], None
    t = session.query(Tag).filter(Tag.id.in_(tags)).all()
    r = Restaurant(
        name=name,
        branch=branch,
        postcode=postcode,
        price=price,
        note=note,
        update_time=datetime.now(),
        tags=t
    )
    session.add(r)
    session.flush()
    return True, return_code["OK"], r.id

@get_session
def delete_restaurant(id, session=None):
    valid = check_restaurant_id(id)
    if not valid:
        return False, return_code["INVALID_DATA"], None
    r = session.query(Restaurant).filter(Restaurant.id == id)
    if not r.count():
        return False, return_code["RESTAURANT_NOT_EXIST"], None
    session.delete(r.first())
    return True, return_code["OK"], None

@get_session
def edit_restaurant(id, name, branch, postcode, price, note, tags, session=None):
    valid = \
        check_restaurant_id(id) and\
        check_restaurant_name(name) and \
        check_restaurant_branch(branch) and \
        check_restaurant_postcode(postcode) and \
        check_restaurant_price(price) and \
        check_restaurant_note(note) and \
        isinstance(tags, list) and all([check_tag_id(x) for x in tags])
    if not valid:
        return False, return_code["INVALID_DATA"], None
    r = session.query(Restaurant).filter(Restaurant.id == id)
    if not r.count():
        return False, return_code["RESTAURANT_NOT_EXIST"], None
    r = r.first()
    r_same_name = session.query(Restaurant).filter(Restaurant.name == name, Restaurant.branch == branch)
    if r_same_name.count() and r_same_name.first().id != id:
        return False, return_code["RESTAURANT_EXIST"], None
    t = session.query(Tag).filter(Tag.id.in_(tags)).all()
    r.name, r.branch, r.postcode, r.price, r.note, r.update_time, r.tags =\
        name, branch, postcode, price, note, datetime.now(), t
    return True, return_code["OK"], id

@get_session
def get_restaurant(id, session=None):
    valid = check_restaurant_id(id)
    if not valid:
        return False, return_code["INVALID_DATA"], None
    r = session.query(Restaurant).filter(Restaurant.id == id)
    if not r.count():
        return False, return_code["RESTAURANT_NOT_EXIST"], None
    r = r.first()
    return True, return_code["OK"], {
        "id": r.id,
        "name": r.name,
        "branch": r.branch,
        "postcode": r.postcode,
        "price": r.price,
        "note": r.note,
        "update_time": r.update_time.strftime("%Y-%m-%d %H:%M:%S"),
        "tags": [{"id": t.id, "name": t.name} for t in r.tags]
    }

@get_session
def find_restaurants(name_query, postcode_prefix, min_price, max_price, tags, page, session=None):
    valid = \
        (True if not name_query else check_restaurant_name(name_query)) and\
        (True if not postcode_prefix else check_restaurant_postcode(postcode_prefix)) and\
        (True if min_price is None else check_restaurant_price(min_price)) and\
        (True if max_price is None else check_restaurant_price(max_price)) and \
        isinstance(tags, list) and (True if not tags else all([check_tag_id(x) for x in tags]))
    if not valid:
        return False, return_code["INVALID_DATA"], None
    q = session.query(Restaurant)
    if name_query:
        name_query = re.sub(r"\s+", "%", " " + name_query.replace("%", " ") + " ")
        q = q.filter(Restaurant.name.ilike(name_query))
    if postcode_prefix:
        postcode_prefix = postcode_prefix.replace(" ", "") + "%"
        q = q.filter(Restaurant.postcode.ilike(postcode_prefix))
    if min_price is not None:
        q = q.filter(Restaurant.price >= min_price)
    if max_price is not None:
        q = q.filter(Restaurant.price <= max_price)
    if tags:
        q = q.filter(Restaurant.tags.any(Tag.id.in_(tags)))
    q = q.order_by(Restaurant.id)
    total_page = q.count() // restaurant_per_page + (1 if q.count() % restaurant_per_page != 0 else 0)
    r = q[(page - 1) * restaurant_per_page: page * restaurant_per_page]
    return True, return_code["OK"], {
        "page": page,
        "total_page": total_page,
        "restaurants": [
            {
                "id": x.id,
                "name": x.name,
                "branch": x.branch,
                "tags": [{"id": t.id, "name": t.name} for t in x.tags]
            } for x in r
        ]
    }

@get_session
def get_restaurants_name_branch(ids, session=None):
    valid = isinstance(ids, list) and all([check_restaurant_id(x) for x in ids])
    if not valid:
        return False, return_code["INVALID_DATA"], None
    q = session.query(Restaurant)
    if ids:
        q = q.filter(Restaurant.id.in_(ids))
    r = q.all()
    return True, return_code["OK"], [
        {
            "id": x.id,
            "name": x.name,
            "branch": x.branch
        } for x in r
    ]
