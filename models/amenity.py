#!/usr/bin/python3
"""This is the amenity class"""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import Base, BaseModel
from models.place import place_amenity


class Amenity(BaseModel, Base):
    """
    This is the class Amenity Attributes:
    name: input name
    """

    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    place_amenities = relationship("Place", secondary=place_amenity)
