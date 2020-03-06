# -*- encoding: utf-8 -*-

import unittest
import os
from datetime import datetime

from database.restaurant import Restaurant
from database.tag import Tag
from database.initialize import initialize
from database.base import Session

__author__ = "chenty"


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
