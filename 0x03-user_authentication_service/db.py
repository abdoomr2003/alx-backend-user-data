#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email, hashed_password):
        """Add a new user to the database.

        Args:
            email (str): The user's email address.
            hashed_password (str): The user's hashed password.

        Returns:
            User: The newly created User object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **args):
        """
        Find a user in the database based on input arguments.

        Args:
            **kwargs: Arbitrary keyword arguments to filter the query.

        Returns:
            User: The first matching User object.

        Raises:
            NoResultFound: If no results are found.
            InvalidRequestError: If invalid query arguments are passed.
        """
        try:
            user = self._session.query(User).filter_by(**args).first()
            if user is None:
                raise NoResultFound
            return user
        except InvalidRequestError:
            self._session.rollback()
            raise

    def update_user(self, user_id, **args):
        """
        Update a user in the database.

        Args:
            user_id (int): The user ID.
            **kwargs: Arbitrary keyword arguments to update the user.

        Returns:
            None
        """
        try:
            user = self.find_user_by(id=user_id)
            user.email = args.get('email', user.email)
            user.hashed_password = args.get('hashed_password',
                                            user.hashed_password)
            self._session.add(user)
            self._session.commit()
            return None
        except ValueError:
            raise
