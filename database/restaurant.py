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

from sqlalchemy import Column, String, Integer, DateTime, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from database.base import Base
from database.tag_restaurant import TagRestaurant


class Restaurant(Base):
    """
    Table class to for Restaurant model
    """
    __tablename__ = "restaurant"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False)
    branch = Column(String(50), nullable=False)
    postcode = Column(String(15), nullable=False)
    price = Column(Integer, nullable=False)
    note = Column(Text, nullable=False)
    update_time = Column(DateTime, nullable=False)

    # Name and branch combination must be unique
    index_name_branch = UniqueConstraint(name, branch)

    # m to n relationships between tags and restaurants
    tags = relationship("Tag", secondary=TagRestaurant.__table__, back_populates="restaurants")
