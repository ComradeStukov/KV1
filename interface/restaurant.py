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

from datetime import datetime
import re

from database.restaurant import Restaurant
from database.tag import Tag
from interface.tag import check_tag_id
from interface.utility import get_session, base_return_code


# Return code of interfaces
return_code = base_return_code.copy()
return_code.update({
    "RESTAURANT_NOT_EXIST": 100,
    "RESTAURANT_EXIST": 101,
})
# Default restaurant numbers per page
restaurant_per_page = 20

def check_restaurant_id(id):
    """
    Check whether an id is valid
    :param id: The id
    :return: The result
    """
    return isinstance(id, int) and 0 < id

def check_restaurant_name(name):
    """
    Check whether a restaurant name is valid
    :param name: The name
    :return: The result
    """
    return isinstance(name, str) and 0 < len(name) < 45

def check_restaurant_branch(branch):
    """
    Check whether a restaurant branch is valid
    :param branch: The branch
    :return: The result
    """
    return isinstance(branch, str) and 0 <= len(branch) < 45

def check_restaurant_postcode(postcode):
    """
    Check whether a postcode of UK is valid
    :param postcode: The postcode
    :return: The result
    """
    return isinstance(postcode, str) and re.match(r"^[0-9A-Za-z]{0,12}$", postcode)

def check_restaurant_price(price):
    """
    Check whether the average price of a restaurant is valid
    :param price: The average price
    :return: The result
    """
    return isinstance(price, int) and 0 <= price <= 400

def check_restaurant_note(note):
    """
    Check whether a restaurant note is valid
    :param note: The restaurant note
    :return: The result
    """
    return isinstance(note, str) and 0 <= len(note)

@get_session
def add_restaurant(name, branch, postcode, price, note, tags, session=None):
    """
    Add a restaurant to the database
    :param name: Restaurant name
    :param branch: Restaurant branch
    :param postcode: Restaurant postcode
    :param price: Restaurant price
    :param note: Restaurant note
    :param tags: Restaurant tag id list
    :param session: Auto filled database link session
    :return: If a session should commit, return code, restaurant id
    """
    # Check if all inputs are valid
    valid = \
        check_restaurant_name(name) and\
        check_restaurant_branch(branch) and\
        check_restaurant_postcode(postcode) and\
        check_restaurant_price(price) and\
        check_restaurant_note(note) and \
        isinstance(tags, list) and all([check_tag_id(x) for x in tags])
    if not valid:
        return False, return_code["INVALID_DATA"], None
    # Check if there is a restaurant with the same name and branch
    r_same_name = session.query(Restaurant).filter(Restaurant.name == name, Restaurant.branch == branch)
    if r_same_name.count():
        return False, return_code["RESTAURANT_EXIST"], None
    t = session.query(Tag).filter(Tag.id.in_(tags)).all()
    # Add the restaurant to the database
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
    """
    Delete a restaurant from database
    :param id: Restaurant id
    :param session: Auto filled database link session
    :return: If a session should commit, return code, none
    """
    # Check if all inputs are valid
    valid = check_restaurant_id(id)
    if not valid:
        return False, return_code["INVALID_DATA"], None
    # Find and delete the restaurant
    r = session.query(Restaurant).filter(Restaurant.id == id)
    if not r.count():
        return False, return_code["RESTAURANT_NOT_EXIST"], None
    session.delete(r.first())
    return True, return_code["OK"], None

@get_session
def edit_restaurant(id, name, branch, postcode, price, note, tags, session=None):
    """
    Edit a restaurant
    :param id: Restaurant id
    :param name: Restaurant name
    :param branch: Restaurant branch
    :param postcode: Restaurant postcode
    :param price: Restaurant price
    :param note: Restaurant note
    :param tags: Restaurant tag id list
    :param session: Auto filled database link session
    :return: If a session should commit, return code, restaurant id
    """
    # Check if all inputs are valid
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
    # Find the restaurant and modify it
    r = session.query(Restaurant).filter(Restaurant.id == id)
    if not r.count():
        return False, return_code["RESTAURANT_NOT_EXIST"], None
    r = r.first()
    # Check if a restaurant with the same name and branch exists
    # In that case, the name or branch of the current restaurant can not be changed
    r_same_name = session.query(Restaurant).filter(Restaurant.name == name, Restaurant.branch == branch)
    if r_same_name.count() and r_same_name.first().id != id:
        return False, return_code["RESTAURANT_EXIST"], None
    t = session.query(Tag).filter(Tag.id.in_(tags)).all()
    r.name, r.branch, r.postcode, r.price, r.note, r.update_time, r.tags =\
        name, branch, postcode, price, note, datetime.now(), t
    return True, return_code["OK"], id

@get_session
def get_restaurant(id, session=None):
    """
    Get a restaurant by its id
    :param id: Restaurant id
    :param session:
    :param session: Auto filled database link session
    :return: If a session should commit, return code, details of the restaurant
    """
    # Check if all inputs are valid
    valid = check_restaurant_id(id)
    if not valid:
        return False, return_code["INVALID_DATA"], None
    # Find and return the restaurant
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
    """
    Search restaurants according to conditions
    :param name_query: Partial name
    :param postcode_prefix: Prefix of postcode
    :param min_price: Min of average price
    :param max_price: Max of average price
    :param tags: List of id tags
    :param page: Current page
    :param session: Auto filled database link session
    :return: If a session should commit, return code, brief information of restaurants
    """
    # Check if all inputs are valid
    valid = \
        (True if not name_query else check_restaurant_name(name_query)) and\
        (True if not postcode_prefix else check_restaurant_postcode(postcode_prefix)) and\
        (True if min_price is None else check_restaurant_price(min_price)) and\
        (True if max_price is None else check_restaurant_price(max_price)) and \
        isinstance(tags, list) and (True if not tags else all([check_tag_id(x) for x in tags]))
    if not valid:
        return False, return_code["INVALID_DATA"], None
    # Search with filters according to the conditions
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
    # Get the set of result according to the specified page
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
                "postcode": x.postcode,
                "price": x.price,
                "tags": [{"id": t.id, "name": t.name} for t in x.tags]
            } for x in r
        ]
    }

@get_session
def get_restaurants(ids, session=None):
    """
    Get restaurants according to id
    :param ids: List of restaurant ids
    :param session: Auto filled database link session
    :return: If a session should commit, return code, brief information of restaurants
    """
    # Check if all inputs are valid
    valid = isinstance(ids, list) and all([check_restaurant_id(x) for x in ids])
    if not valid:
        return False, return_code["INVALID_DATA"], None
    if not ids:
        return True, return_code["OK"], []
    # Get and return information
    r = session.query(Restaurant).filter(Restaurant.id.in_(ids)).all()
    return True, return_code["OK"], [
        {
            "id": x.id,
            "name": x.name,
            "branch": x.branch,
            "postcode": x.postcode,
            "price": x.price,
            "tags": [{"id": t.id, "name": t.name} for t in x.tags]
        } for x in r
    ]
