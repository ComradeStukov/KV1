# -*- encoding: utf-8 -*-

__author__ = "chenty"

from sqlalchemy import Column, Integer, ForeignKey

from database.base import Base


class TagRestaurant(Base):
    __tablename__ = "tag__restaurant"

    tag_id = Column(Integer,
                    ForeignKey("tag.id", onupdate="CASCADE", ondelete="CASCADE"),
                    primary_key=True)
    restaurant_id = Column(Integer,
                           ForeignKey("restaurant.id", onupdate="CASCADE", ondelete="CASCADE"),
                           primary_key=True)
