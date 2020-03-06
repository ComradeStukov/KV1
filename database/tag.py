# -*- encoding: utf-8 -*-

__author__ = "chenty"

from sqlalchemy import Column, String, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from database.base import Base
from database.tag_restaurant import TagRestaurant


class Tag(Base):
    """
    Table class to for Tag model
    """
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False)

    # Name of the tag must be unique
    index_name = UniqueConstraint(name)

    # m to n relationships between tags and restaurants
    restaurants = relationship("Restaurant", secondary=TagRestaurant.__table__, back_populates="tags")
