#!/usr/bin/python3
"""
An extension of BaseModel for review
"""
from models.base_model import BaseModel


class Review(BaseModel):
    '''
    represents a Review
    '''
    place_id = ''
    user_id = ''
    text = ''
