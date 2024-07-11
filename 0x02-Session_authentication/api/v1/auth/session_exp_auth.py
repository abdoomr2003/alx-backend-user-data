#!/usr/bin/env python3
'''Module for Authentication'''
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    '''Session Authentication Module with Expiration'''
    session_dictionary = {}

    def __init__(self):
        '''Instantiation Function'''
        from os import getenv
        duration = getenv('SESSION_DURATION')
        try:
            self.session_duration = int(duration)
        except Exception:
            self.session_duration = 0
        print(self.session_duration)

    def create_session(self, user_id=None):
        '''Create session based on parent class'''
        print(self.user_id_by_session_id)
        try:
            session_id = super().create_session(user_id)
        except Exception:
            session_id = None
        from datetime import datetime
        self.session_dictionary["user_id"] = user_id
        self.session_dictionary["created_at"] = datetime.now()
        print(self.session_dictionary)
        print(session_id)
        self.user_id_by_session_id[session_id] = self.session_dictionary
        print(self.user_id_by_session_id[session_id])
        return session_id

    def user_id_for_session_id(self, session_id=None):
        '''Retreives user_id with session_id'''
        if session_id is None:
            return None
        if not self.user_id_by_session_id.get(session_id):
            return None
        if self.session_duration <= 0:
            return self.session_dictionary.get("user_id")
        if not self.session_dictionary.get("created_at"):
            return None
        from datetime import datetime, timedelta
        expired = self.session_dictionary.get(
            "created_at") + timedelta(seconds=self.session_duration)
        if expired < datetime.now():
            return None
        return self.session_dictionary.get("user_id")
