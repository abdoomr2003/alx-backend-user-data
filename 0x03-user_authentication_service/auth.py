#!/usr/bin/env python3
"""
Main file
"""
import logging
import bcrypt
from user import User
from db import DB
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from flask import jsonify
from uuid import uuid4

logging.disable(logging.WARNING)


def _hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


def _generate_uuid() -> str:
    """
    Generate a UUID
    """
    return str(uuid4())


class Auth:
    """
    Auth class
    """
    def __init__(self):
        """
        Constructor
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register user
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            pass
            # print(existing_email)
            # verifier si l'email exist
            # if existing_email:
            #     raise ValueError("User {} already exists".format(email))

            # hasher le mot de passe si l'email n'existe pas
            hashed_password = _hash_password(password)

            # enregistrer le nouvel user a la base de donne
            user = self._db.add_user(email, hashed_password)

            return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find user by a specific attribute
        """
        try:
            user = self._db.find_user_by(**kwargs)
            return user
        except InvalidRequestError:
            return None

    def valid_login(self, email: str, password: str) -> bool:
        """
        validation login
        """
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                password = password.encode('utf-8')
                hased_password = user.hashed_password
                if bcrypt.checkpw(password, user.hashed_password):
                    return True

        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """
        Create a new session
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = _generate_uuid()
                self._db.update_user(user.id, session_id=session_id)
                return session_id
            return {"message": "User {} does not exist".format(email)}, 400
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """
        Get user from session id
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            if user:
                return user
            return None
        except NoResultFound:
            return None
        except InvalidRequestError:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy session
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            pass
        except InvalidRequestError:
            pass
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Get reset password token
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                reset_token = _generate_uuid()
                self._db.update_user(user.id, reset_token=reset_token)
                return reset_token
            return None
        except NoResultFound:
            return None
        except InvalidRequestError:
            return None

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            if user:
                hashed_password = _hash_password(password)
                self._db.update_user(user.id, hashed_password=hashed_password)
            return None
        except NoResultFound:
            return None
        except InvalidRequestError:
            return None
