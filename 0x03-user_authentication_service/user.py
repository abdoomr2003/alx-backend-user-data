#!/usr/bin/env python3
"""User class module."""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Column, Integer

Base = declarative_base()


class User(Base):
    """User class.
    Attributes:
        id (int): User id.
        email (str): User email.
        hashed_password (str): User hashed password.
        session_id (str): User session id.
        reset_token (str): User reset token.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
