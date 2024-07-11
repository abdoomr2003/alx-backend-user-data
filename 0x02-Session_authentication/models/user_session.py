#!/usr/bin/env python3
'''Module for User Session Class'''
from models.base import Base

class UserSession(Base):
    '''UserSession Class'''
    def __init__(self, *args: list, **kwargs: dict):
        '''Initialization Function'''
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
