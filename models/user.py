#!/usr/bin/python3
"""
An extension of BaseModel for Users
"""
from models.base_model import BaseModel


class User(BaseModel):
    '''
    represents a user model
    '''
    email = ''
    password = ''
    first_name = ''
    last_name = ''
