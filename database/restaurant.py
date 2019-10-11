# -*- encoding: utf-8 -*-

__author__ = "chenty"

from sqlalchemy import Column, String, Integer, DateTime, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from database.base import Base
from database.tag__restaurant import Tag__Restaurant


class Restaurant(Base):
    __tablename__ = "restaurant"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    branch = Column(String, nullable=False)
    postcode = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    note = Column(Text, nullable=False)
    update_time = Column(DateTime, nullable=False)

    index_name_branch = UniqueConstraint(name, branch)

    tags = relationship("Tag", secondary=Tag__Restaurant.__table__, back_populates="restaurants")
