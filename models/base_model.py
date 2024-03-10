#!/usr/bin/python3
'''
Defines all common attributes and methods for
model classes
'''

from uuid import uuid4
from datetime import datetime
import models


class BaseModel:
    """
    Methods:
        save()
        to_dict()
    """

    def __init__(self, *args, **kwargs):
        """
        Creates an id for each BaseModel and keeps track of each time
        a user is created and updated

        Attrs:
            id: uuid.uuid4 string
            creates_at: current datetime when an instance is created
            updated_at: current datetime when an instance is created
            and it will be updated every time you change your object
        """
        format = "%Y-%m-%dT%H:%M:%S.%f"
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key == 'created_at' or key == 'updated_at':
                        try:
                            time = datetime.strptime(value, format)
                            setattr(self, key, time)
                        except Exception as Exc:
                            raise Exc(f"{value} is not in right {format}")
                    else:
                        setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def save(self):
        """
        Updates the public instance attribute updated_at
        and serialises it
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        returns a dictionary containing all
        keys/values of __dict__ of the instance
        """
        instance_dict = self.__dict__.copy()
        instance_dict.update({'__class__': self.__class__.__name__})
        instance_dict['created_at'] = instance_dict['created_at'].isoformat()
        instance_dict['updated_at'] = instance_dict['updated_at'].isoformat()
        return instance_dict

    def __str__(self):
        '''
        string representatioon of a BaseModel
        '''
        string__ = f'[{self.__class__.__name__}] ({self.id})' +\
            f' {self.__dict__}'
        return string__
