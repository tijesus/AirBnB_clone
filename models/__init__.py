#!/usr/bin/python3
"""
All classes in this package represent a database table in the form
of classes

modules:
    base_model
"""
from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
