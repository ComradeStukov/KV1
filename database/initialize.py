# -*- encoding: utf-8 -*-

__author__ = "chenty"

from datetime import datetime

from database.base import Base, engine
from database.restaurant import Restaurant
from database.tag import Tag
from database.tag__restaurant import Tag__Restaurant


def initialize():
    Base.metadata.create_all(engine)
    return

if __name__ == "__main__":
    initialize()
