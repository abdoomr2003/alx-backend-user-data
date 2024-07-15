#!/usr/bin/env python3
"""
auth module
"""
from bcrypt import hashpw, gensalt
from db import DB, User
from sqlalchemy.exc import NoResultFound

def _hash_password(password: str) -> str:
    """Hash a password

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return hashpw(password.encode(), gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user

        Args:
            email (str): The user's email
            password (str): The user's password

        Returns:
            User: The newly created User object

        Raises:
            ValueError: If a user with the given email already exists
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            user = self._db.add_user(email=email, hashed_password=_hash_password(password))
            return user