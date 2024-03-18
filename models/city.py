#!/usr/bin/python3
"""
An extension of BaseModel for city
"""
from models.base_model import BaseModel


class City(BaseModel):
    '''
    represents a City
    '''
    state_id = ''
    name = ''
