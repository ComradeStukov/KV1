# -*- encoding: utf-8 -*-

__author__ = "chenty"

import unittest

from database.initialize import initialize
from interface.utility import end_session
from interface.restaurant import *
from interface.tag import *
from interface.restaurant import return_code as r_ret_code
from interface.tag import return_code as t_ret_code


class InterfaceTest(unittest.TestCase):
    def setUp(self):
        initialize()
        return

    def _test_add_restaurant(self):
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

    def _test_delete_restaurant(self):
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

    def _test_edit_restaurant(self):
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

    def _test_get_restaurant(self):
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

    def _test_find_restaurants(self):
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

    def _test_get_restaurant_name_branch(self):
        code, res = get_restaurants_name_branch([1, 2, 3])
        self.assertEqual(code, r_ret_code["OK"])
        self.assertEqual(res, [
            {"id": 1, "name": "r", "branch": "b"},
            {"id": 2, "name": "r2", "branch": "b2"},
            {"id": 3, "name": "r3", "branch": "b3"}
        ])
        code, res = get_restaurants_name_branch([1, 2, 3, 4])
        self.assertEqual(code, r_ret_code["OK"])
        self.assertEqual(res, [
            {"id": 1, "name": "r", "branch": "b"},
            {"id": 2, "name": "r2", "branch": "b2"},
            {"id": 3, "name": "r3", "branch": "b3"}
        ])
        code, res = get_restaurants_name_branch([1, 3])
        self.assertEqual(code, r_ret_code["OK"])
        self.assertEqual(res, [
            {"id": 1, "name": "r", "branch": "b"},
            {"id": 3, "name": "r3", "branch": "b3"}
        ])
        code, res = get_restaurants_name_branch([4])
        self.assertEqual(code, r_ret_code["OK"])
        self.assertEqual(res, [])
        code, res = get_restaurants_name_branch(["asdf"])
        self.assertEqual(code, r_ret_code["INVALID_DATA"])
        self.assertEqual(res, None)
        return

    def _test_add_tag(self):
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

    def _test_delete_tag(self):
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

    def _test_edit_tag(self):
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

    def _test_find_tags(self):
        code, res = get_tags([])
        self.assertEqual(code, t_ret_code["OK"])
        self.assertEqual(len(res), 2)
        self.assertEqual(res, [
            {"id": 1, "name": "t"},
            {"id": 2, "name": "t2"},
        ])
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

    def test(self):
        self._test_add_restaurant()
        self._test_delete_restaurant()
        self._test_edit_restaurant()
        self._test_get_restaurant()
        self._test_find_restaurants()
        self._test_get_restaurant_name_branch()
        self._test_add_tag()
        self._test_delete_tag()
        self._test_edit_tag()
        self._test_find_tags()
        return

    def tearDown(self):
        end_session()
        return


if __name__ == "__main__":
    unittest.main()
