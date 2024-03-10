#!/usr/bin/python3
"""A BaseModel class that serves as the backbone to the AirBnB project"""

import uuid
from datetime import datetime
import models


class BaseModel():
    """BaseModel class initilization"""

    def __init__(self, *args, **kwargs):
        """Initialize the instances creations"""
        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                setattr(self, key, value)
            if "created_at" in kwargs:
                c_a_str = kwargs['created_at']
                formmatter = "%Y-%m-%dT%H:%M:%S.%f"
                self.created_at = datetime.strptime(c_a_str, formmatter)
            if "updated_at" in kwargs:
                u_a_str = kwargs['updated_at']
                formmatter = "%Y-%m-%dT%H:%M:%S.%f"
                self.updated_at = datetime.strptime(u_a_str, formmatter)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        models.storage.new(self)

    def save(self):
        """Save object to file"""
        self.created_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary after saving the instance as a key"""
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        return obj_dict

    def __str__(self):
        """Return a string representation of this instance"""
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)
