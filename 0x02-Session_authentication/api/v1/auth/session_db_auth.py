#!/usr/bin/env python3
'''Module for Authentication'''
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    '''Session Authentication Module for database'''

    def create_session(self, user_id=None):
        '''Create And Stores Instance of UserSession'''
        session_id = super().create_session(user_id)
        user = UserSession(user_id=user_id, session_id=session_id)
        user.save()
        print(session_id)
        return session_id

    def user_id_for_session_id(self, session_id=None):
        '''Retreives user_id for UserSession vi session_id'''
        if session_id is None or type(session_id) != str:
            return None
        print(session_id)
        UserSession.load_from_file()
        user_session = UserSession.get(session_id)
        return user_session.user_id if user_session else None

    def destroy_session(self, request=None):
        '''Destroys UserSession based on cookie session_id'''
        '''Destroys session'''
        if request is None or not self.session_cookie(request):
            return False
        session = self.session_cookie(request)
        user_session = UserSession.get(session)
        if user_session:
            user_session.remove()
            return True
        return False
