#!/usr/bin/python3
'''file storage engine for serialization and desialization of data'''
from json import dump, load
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State


class FileStorage:
    '''
    serializes instances to a JSON file and
    deserializes JSON file to instances
    '''

    __file_path = 'file.json'
    __objects = {}  # dictionary of insantiated objects

    def all(self):
        '''
        returns __objects
        '''
        return FileStorage.__objects

    def new(self, obj):
        '''
        sets in __objects the obj with key <obj class name>.id
        '''
        obj_class_name = obj.__class__.__name__
        obj_id = obj.id

        FileStorage.__objects[obj_class_name + '.' + obj_id] = obj

    def save(self):
        """
        serializes __objects to the JSON file (path: __file_path)
        """
        allobj_dict = FileStorage.__objects

        formatted_objects_dict = \
            {key: allobj_dict[key].to_dict() for key in allobj_dict.keys()}

        with open(FileStorage.__file_path, "w", encoding='utf-8') as json_file:
            dump(formatted_objects_dict, json_file)

    def reload(self):
        """
        deserializes the JSON file to __objects
        (only if the JSON file (__file_path) exists
        otherwise, do nothing.
        If the file doesn’t exist, no exception should be raised)
        """

        try:
            with open(FileStorage.__file_path, 'r', encoding='utf-8') as f:
                json_object = load(f)

                for key, value in json_object.items():
                    cls_name, object_id = key.split('.')
                    instance = eval(cls_name)(**value)
                    FileStorage.__objects[key] = instance
        except FileNotFoundError:
            pass
