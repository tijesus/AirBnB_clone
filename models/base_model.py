#!/usr/bin/python3
""" Defines all common attributes and methods for model classes """

from uuid import uuid4
from datetime import datetime
import models


class BaseModel:
    """ Method to save and convert to dictionary"""

    def __init__(self, *args, **kwargs):
        """creating ID and datetime instances"""

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
        """Save instances"""

        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """convert to dictionary"""

        instance_dict = self.__dict__.copy()
        instance_dict.update({'__class__': self.__class__.__name__})
        instance_dict['created_at'] = instance_dict['created_at'].isoformat()
        instance_dict['updated_at'] = instance_dict['updated_at'].isoformat()
        return instance_dict

    def __str__(self):
        """string representation"""

        string__ = f'[{self.__class__.__name__}] ({self.id})' +\
            f' {self.__dict__}'
        return string__
