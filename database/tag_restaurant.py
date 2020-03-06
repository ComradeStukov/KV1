# -*- encoding: utf-8 -*-

__author__ = "chenty"

from sqlalchemy import Column, Integer, ForeignKey

from database.base import Base


class TagRestaurant(Base):
    """
    m to n relationships between tags and restaurants
    """
    __tablename__ = "tag_restaurant"

    tag_id = Column(
        Integer,
        ForeignKey("tag.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True
    )
    restaurant_id = Column(
        Integer,
        ForeignKey("restaurant.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True
    )
