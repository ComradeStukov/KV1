# -*- encoding: utf-8 -*-

import unittest
from datetime import datetime

from database.restaurant import Restaurant
from database.tag import Tag
from database.initialize import initialize
from database.base import Session

__author__ = "chenty"


class DatabaseTest(unittest.TestCase):
    def setUp(self):
        initialize()
        self.session = Session()
        return

    def _test_restaurant(self):
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

    def _test_tag(self):
        t1 = Tag(name="t1")
        t2 = Tag(name="t2")
        self.session.add(t1)
        self.session.add(t2)
        self.session.flush()
        self.assertEqual(t1.id, 1)
        self.assertEqual(self.session.query(Tag).count(), 2)
        self.session.commit()
        return

    def _test_restaurant_tag(self):
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

    def test(self):
        self._test_restaurant()
        self._test_tag()
        self._test_restaurant_tag()
        return

    def tearDown(self):
        self.session.commit()
        Session.remove()
        return


if __name__ == "__main__":
    unittest.main()
