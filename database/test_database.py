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
from datetime import datetime

from database.restaurant import Restaurant
from database.tag import Tag
from database.initialize import initialize
from database.base import Session


class TestDatabase(unittest.TestCase):
    """
    Unit test class for database
    """
    @classmethod
    def setUpClass(cls):
        """
        Initialize the database before all tests
        :return: None
        """
        initialize()
        return

    def setUp(self):
        """
        Initialize the session before each test
        :return: None
        """
        self.session = Session()
        return

    def test_000_restaurant(self):
        """
        Test to operate restaurant models
        :return: None
        """
        r1 = Restaurant(name="r1", branch="b1", postcode="a", price=1, note="", update_time=datetime.now())
        r2 = Restaurant(name="r2", branch="b2", postcode="b", price=2, note="", update_time=datetime.now())
        r3 = Restaurant(name="r3", branch="b3", postcode="c", price=3, note="", update_time=datetime.now())
        self.assertEqual(r1.name, "r1")
        self.assertEqual(r1.id, None)
        self.session.add(r1)
        self.session.add(r2)
        self.session.add(r3)
        self.assertEqual(r2.id, None)
        self.session.flush()
        self.assertEqual(r1.id, 1)
        self.assertEqual(r3.tags, [])
        self.session.commit()
        return

    def test_001_tag(self):
        """
        Test to operate tag models
        :return: None
        """
        t1 = Tag(name="t1")
        t2 = Tag(name="t2")
        self.session.add(t1)
        self.session.add(t2)
        self.session.flush()
        self.assertEqual(t1.id, 1)
        self.assertEqual(self.session.query(Tag).count(), 2)
        self.session.commit()
        return

    def test_002_restaurant_tag(self):
        """
        Test to operate relationships between tags and restaurants models
        :return: None
        """
        self.assertEqual(self.session.query(Tag).count(), 2)
        self.assertEqual(self.session.query(Restaurant).count(), 3)
        r2 = self.session.query(Restaurant).filter(Restaurant.id == 2).first()
        self.assertEqual(r2.name, "r2")
        t = self.session.query(Tag).all()
        self.assertEqual(len(t), 2)
        r2.tags = t
        self.session.flush()
        self.assertEqual(len(r2.tags), 2)
        self.session.commit()

    def tearDown(self):
        """
        Commit and end session after each test
        :return: None
        """
        self.session.commit()
        Session.remove()
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
