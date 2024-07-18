#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    self._session:
        refers to SQLAlchemy session obj associated with database connection
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

    def add_user(self, email: str, hashed_password: str) -> User:
        """Methid adding a user into the db
        Args:
            email (str): The email of the user
            hashed_password (str): hashed password of the user
        Returns:
            User: The newly added User object"""

        try:
            new_user = User(email=email, hashed_password=hashed_password)
            # Add the new_user object to the session
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            # Rollback the transaction in case of an error
            self._session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Method finding a user in db based on provided criteria
        Args:
            **kwargs: Arbitrary keyword args used to filter users table
        Returns:
            User: First user found matching the provided criteria"""
        if not kwargs:
            raise InvalidRequestError

        # Query the users table based on the provided criteria
        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            # If no user is found, raise NoResultFound
            raise NoResultFound

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user's  attributes based on provided args
        Args:
            user_id (int): The ID of the user to update
            **kwargs: Arbitrary kwargs rep user attribute + their new values"""

        # Locate the user to update
        user = self.find_user_by(id=user_id)
        if user is None:
            return

        # Update the user's attribute
        for attr, value in kwargs.items():
            if hasattr(User, attr):
                setattr(user, attr, value)
            else:
                raise ValueError

        # Commit changes to the database
        try:
            self._session.commit()
        except InvalidRequestError:
            self._session.rollback()
            raise InvalidRequestError
