# -*- encoding: utf-8 -*-

__author__ = "chenty"

from sqlalchemy import Column, String, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from database.base import Base
from database.tag__restaurant import Tag__Restaurant


class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)

    index_name = UniqueConstraint(name)

    restaurants = relationship("Restaurant", secondary=Tag__Restaurant.__table__, back_populates="tags")
