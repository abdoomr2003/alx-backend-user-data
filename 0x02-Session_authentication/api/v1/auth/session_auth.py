#!/usr/bin/env python3
'''Module for Authentication'''
from flask import request
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    '''Session Authentication Module'''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''Generates session id for isers'''
        session_id = None if user_id is None or type(
            user_id) is not str else str(uuid4())
        if session_id:
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''Retreives user_id for session_id'''
        if session_id is None or type(session_id) is not str:
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None):
        '''Returns a User instance based on a cookie value'''
        session_cookie = self.session_cookie(request)
        if session_cookie:
            user_id = self.user_id_for_session_id(session_cookie)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        '''Destroys session'''
        if request is None or not self.session_cookie(request):
            return False
        session = self.session_cookie(request)
        if not self.user_id_for_session_id(session):
            return False
        del self.user_id_by_session_id[session]
        return True
