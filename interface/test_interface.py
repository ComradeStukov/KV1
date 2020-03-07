#!/usr/bin/env python
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

import os
import sys
sys.path.append(os.path.dirname(os.getcwd()))
import unittest

from database.initialize import initialize
from interface.utility import end_session
from interface.restaurant import *
from interface.tag import *
from interface.restaurant import return_code as r_ret_code
from interface.tag import return_code as t_ret_code


class TestInterface(unittest.TestCase):
    """
    Unit test class for logic interface
    """
    @classmethod
    def setUpClass(cls):
        """
        Initialize the database before all tests
        :return: None
        """
        initialize()
        return

    def test_000_add_restaurant(self):
        """
        Test to add restaurants
        :return: None
        """
        code, res = add_restaurant("r1", "b1", "p1", 1, "", [])
        self.assertEqual(code, r_ret_code["OK"])
        self.assertEqual(res, 1)
        code, res = add_restaurant("r2", "b2", "p2", 2, "", [])
        self.assertEqual(code, r_ret_code["OK"])
        self.assertEqual(res, 2)
        code, res = add_restaurant("r3", "b3", "p3", 3, "note3", [])
        self.assertEqual(code, r_ret_code["OK"])
        self.assertEqual(res, 3)
        code, res = add_restaurant("r1", "b1", "p", 1, "", [])
        self.assertEqual(code, r_ret_code["RESTAURANT_EXIST"])
        self.assertEqual(res, None)
        code, res = add_restaurant("", "b", "p1", 1, "", [])
        self.assertEqual(code, r_ret_code["INVALID_DATA"])
        self.assertEqual(res, None)
        code, res = add_restaurant("", "b" * 100, "p1", 1, "", [])
        self.assertEqual(code, r_ret_code["INVALID_DATA"])
        self.assertEqual(res, None)
        code, res = add_restaurant("r", "b", "p111111111111111111", 1, "", [])
        self.assertEqual(code, r_ret_code["INVALID_DATA"])
        self.assertEqual(res, None)
        code, res = add_restaurant("r", "b", "p", -1, "", [])
        self.assertEqual(code, r_ret_code["INVALID_DATA"])
        self.assertEqual(res, None)
        code, res = add_restaurant("r", "b", "p", -1, 1234, [])
        self.assertEqual(code, r_ret_code["INVALID_DATA"])
        self.assertEqual(res, None)
        code, res = add_restaurant("r", "b", "p", -1, "", ["asdf"])
        self.assertEqual(code, r_ret_code["INVALID_DATA"])
        self.assertEqual(res, None)
        code, res = add_restaurant("rd", "bd", "pd", 4, "noted", [])
        self.assertEqual(code, r_ret_code["OK"])
        self.assertEqual(res, 4)
        return

    def test_001_delete_restaurant(self):
        """
        Test to delete restaurants
        :return: None
        """
        code, res = delete_restaurant(4)
        self.assertEqual(code, r_ret_code["OK"])
        self.assertEqual(res, None)
        code, res = delete_restaurant(4)
        self.assertEqual(code, r_ret_code["RESTAURANT_NOT_EXIST"])
        self.assertEqual(res, None)
        code, res = delete_restaurant("asdf")
        self.assertEqual(code, r_ret_code["INVALID_DATA"])
        self.assertEqual(res, None)
        return

    def test_002_edit_restaurant(self):
        """
        Test to edit restaurants
        :return: None
        """
        code, res = edit_restaurant(1, "r", "b", "p", 1, "", [])
        self.assertEqual(code, r_ret_code["OK"])
        self.assertEqual(res, 1)
        code, res = edit_restaurant(1, "r", "b", "p", 1, "", [])
        self.assertEqual(code, r_ret_code["OK"])
        self.assertEqual(res, 1)
        code, res = edit_restaurant(2, "r", "b", "p", 1, "", [])
        self.assertEqual(code, r_ret_code["RESTAURANT_EXIST"])
        self.assertEqual(res, None)
        code, res = edit_restaurant(4, "r4", "b4", "p4", 4, "", [])
        self.assertEqual(code, r_ret_code["RESTAURANT_NOT_EXIST"])
        self.assertEqual(res, None)
        code, res = edit_restaurant(2, "r", "b", "p", "t", "", [])
        self.assertEqual(code, r_ret_code["INVALID_DATA"])
        self.assertEqual(res, None)
        return

    def test_003_get_restaurant(self):
        """
        Test to get restaurants
        :return: None
        """
        code, res = get_restaurant(1)
        del res["update_time"]
        self.assertEqual(code, r_ret_code["OK"])
        self.assertEqual(res, {
            "id": 1,
            "name": "r",
            "branch": "b",
            "postcode": "p",
            "price": 1,
            "note": "",
            "tags": []
        })
        code, res = get_restaurant(4)
        self.assertEqual(code, r_ret_code["RESTAURANT_NOT_EXIST"])
        self.assertEqual(res, None)
        code, res = get_restaurant("asdf")
        self.assertEqual(code, r_ret_code["INVALID_DATA"])
        self.assertEqual(res, None)
        return

    def test_004_find_restaurants(self):
        """
        Test to find restaurants
        :return: None
        """
        code, res = find_restaurants("", "", None, None, [], 1)
        self.assertEqual(code, r_ret_code["OK"])
        self.assertEqual(len(res["restaurants"]), 3)
        self.assertEqual(res["restaurants"][0]["id"], 1)
        self.assertEqual(res["page"], 1)
        self.assertEqual(res["total_page"], 1)
        code, res = find_restaurants("2", "", None, None, [], 1)
        self.assertEqual(code, r_ret_code["OK"])
        self.assertEqual(len(res["restaurants"]), 1)
        self.assertEqual(res["restaurants"][0]["id"], 2)
        code, res = find_restaurants("1", "", None, None, [], 1)
        self.assertEqual(code, r_ret_code["OK"])
        self.assertEqual(len(res["restaurants"]), 0)
        code, res = find_restaurants(" %r   3", "", None, None, [], 1)
        self.assertEqual(code, r_ret_code["OK"])
        self.assertEqual(len(res["restaurants"]), 1)
        self.assertEqual(res["restaurants"][0]["id"], 3)
        code, res = find_restaurants("", "P", None, None, [], 1)
        self.assertEqual(code, r_ret_code["OK"])
        self.assertEqual(len(res["restaurants"]), 3)
        code, res = find_restaurants("r", "", 1, 2, [], 1)
        self.assertEqual(code, r_ret_code["OK"])
        self.assertEqual(len(res["restaurants"]), 2)
        code, res = find_restaurants("1", "", None, None, [], 2)
        self.assertEqual(code, r_ret_code["OK"])
        self.assertEqual(len(res["restaurants"]), 0)
        code, res = find_restaurants(1, "", None, None, [], 2)
        self.assertEqual(code, r_ret_code["INVALID_DATA"])
        self.assertEqual(res, None)
        return

    def test_005_get_restaurants(self):
        """
        Test to get restaurants
        :return: None
        """
        code, res = get_restaurants([1, 2, 3])
        self.assertEqual(code, r_ret_code["OK"])
        self.assertEqual(res[0]["id"], 1)
        code, res = get_restaurants([1, 2, 3, 4])
        self.assertEqual(code, r_ret_code["OK"])
        self.assertEqual(len(res), 3)
        code, res = get_restaurants([1, 3])
        self.assertEqual(code, r_ret_code["OK"])
        self.assertEqual(len(res), 2)
        code, res = get_restaurants([4])
        self.assertEqual(code, r_ret_code["OK"])
        self.assertEqual(res, [])
        code, res = get_restaurants(["asdf"])
        self.assertEqual(code, r_ret_code["INVALID_DATA"])
        self.assertEqual(res, None)
        return

    def test_006_add_tag(self):
        """
        Test to add tags
        :return: None
        """
        code, res = add_tag("t1")
        self.assertEqual(code, t_ret_code["OK"])
        self.assertEqual(res, {"id": 1, "name": "t1"})
        code, res = add_tag("t2")
        self.assertEqual(code, t_ret_code["OK"])
        self.assertEqual(res, {"id": 2, "name": "t2"})
        code, res = add_tag("t3")
        self.assertEqual(code, t_ret_code["OK"])
        self.assertEqual(res, {"id": 3, "name": "t3"})
        code, res = add_tag(1)
        self.assertEqual(code, t_ret_code["INVALID_DATA"])
        self.assertEqual(res, None)
        code, res = add_tag("t1")
        self.assertEqual(code, t_ret_code["TAG_EXIST"])
        self.assertEqual(res, None)
        code, res = edit_restaurant(1, "r", "b", "p", 1, "", [1, 2, 3])
        self.assertEqual(code, r_ret_code["OK"])
        self.assertEqual(res, 1)
        code, res = get_restaurant(1)
        self.assertEqual(code, r_ret_code["OK"])
        self.assertEqual(res["tags"], [
            {"id": 1, "name": "t1"},
            {"id": 2, "name": "t2"},
            {"id": 3, "name": "t3"}
        ])
        return

    def test_007_delete_tag(self):
        """
        Test to delete tags
        :return: None
        """
        code, res = delete_tag(3)
        self.assertEqual(code, t_ret_code["OK"])
        self.assertEqual(res, 3)
        code, res = delete_tag(3)
        self.assertEqual(code, t_ret_code["TAG_NOT_EXIST"])
        self.assertEqual(res, None)
        code, res = delete_tag("asdf")
        self.assertEqual(code, t_ret_code["INVALID_DATA"])
        self.assertEqual(res, None)
        code, res = get_restaurant(1)
        self.assertEqual(code, r_ret_code["OK"])
        self.assertEqual(res["tags"], [
            {"id": 1, "name": "t1"},
            {"id": 2, "name": "t2"}
        ])
        code, res = find_restaurants("r", "", None, None, [1, 3], 1)
        self.assertEqual(code, r_ret_code["OK"])
        self.assertEqual(len(res["restaurants"]), 1)
        self.assertEqual(res["restaurants"][0]["id"], 1)
        return

    def test_008_edit_tag(self):
        """
        Test to edit tags
        :return: None
        """
        code, res = edit_tag(1, "t")
        self.assertEqual(code, t_ret_code["OK"])
        self.assertEqual(res, {"id": 1, "name": "t"})
        code, res = edit_tag(1, "t")
        self.assertEqual(code, t_ret_code["OK"])
        self.assertEqual(res, {"id": 1, "name": "t"})
        code, res = edit_tag(3, "t3")
        self.assertEqual(code, t_ret_code["TAG_NOT_EXIST"])
        self.assertEqual(res, None)
        code, res = edit_tag(2, "t")
        self.assertEqual(code, t_ret_code["TAG_EXIST"])
        self.assertEqual(res, None)
        code, res = edit_tag(1, 1)
        self.assertEqual(code, t_ret_code["INVALID_DATA"])
        self.assertEqual(res, None)
        code, res = get_restaurant(1)
        self.assertEqual(code, r_ret_code["OK"])
        self.assertEqual(res["tags"], [
            {"id": 1, "name": "t"},
            {"id": 2, "name": "t2"},
        ])
        return

    def test_009_get_tags(self):
        """
        Test to get tags
        :return: None
        """
        code, res = get_tags([])
        self.assertEqual(code, t_ret_code["OK"])
        self.assertEqual(len(res), 0)
        self.assertEqual(res, [])
        code, res = get_tags([1, 2])
        self.assertEqual(code, t_ret_code["OK"])
        self.assertEqual(len(res), 2)
        self.assertEqual(res, [
            {"id": 1, "name": "t"},
            {"id": 2, "name": "t2"},
        ])
        code, res = get_tags([2])
        self.assertEqual(code, t_ret_code["OK"])
        self.assertEqual(len(res), 1)
        self.assertEqual(res, [
            {"id": 2, "name": "t2"},
        ])
        code, res = get_tags([3])
        self.assertEqual(code, t_ret_code["OK"])
        self.assertEqual(len(res), 0)
        self.assertEqual(res, [])
        code, res = get_tags(1)
        self.assertEqual(code, t_ret_code["INVALID_DATA"])
        self.assertEqual(res, None)
        return

    def test_010_find_tags(self):
        """
        Test to find tags
        :return: None
        """
        code, res = find_tags("")
        self.assertEqual(code, t_ret_code["OK"])
        self.assertEqual(len(res), 2)
        self.assertEqual(res, [
            {"id": 1, "name": "t"},
            {"id": 2, "name": "t2"},
        ])
        code, res = find_tags("t")
        self.assertEqual(code, t_ret_code["OK"])
        self.assertEqual(len(res), 2)
        self.assertEqual(res, [
            {"id": 1, "name": "t"},
            {"id": 2, "name": "t2"},
        ])
        code, res = find_tags("2")
        self.assertEqual(code, t_ret_code["OK"])
        self.assertEqual(len(res), 1)
        self.assertEqual(res, [
            {"id": 2, "name": "t2"},
        ])
        code, res = find_tags("3")
        self.assertEqual(code, t_ret_code["OK"])
        self.assertEqual(len(res), 0)
        self.assertEqual(res, [])
        code, res = find_tags(1)
        self.assertEqual(code, t_ret_code["INVALID_DATA"])
        self.assertEqual(res, None)
        return

    def tearDown(self):
        """
        Remove session after each test
        :return: None
        """
        end_session()
        return

    @classmethod
    def tearDownClass(cls):
        """
        Remove the database after all tests
        :return: None
        """
        os.remove("kv1.db")
        return

if __name__ == "__main__":
    unittest.main()
