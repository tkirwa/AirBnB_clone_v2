#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from os import getenv

from models.amenity import Amenity

# Model Import
from models.base_model import BaseModel
from models.city import City
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

if getenv("HBNB_TYPE_STORAGE") == "db":
    storage = DBStorage()
else:
    storage = FileStorage()
storage.reload()
