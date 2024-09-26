#!/usr/bin/env python3
"""
User module for SQLAlchemy database model.

This module defines a User class for the users table.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    User SQLAlchemy model for a users table.

    Attributes:
        id (int): The user's ID, which is the primary key.
        email (str): The user's email, non-nullable.
        hashed_password (str): The user's hashed password, non-nullable.
        session_id (str): The user's session ID, nullable.
        reset_token (str): The user's reset token, nullable.
    """
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True)
    email: str = Column(String(250), nullable=False)
    hashed_password: str = Column(String(250), nullable=False)
    session_id: str = Column(String(250), nullable=True)
    reset_token: str = Column(String(250), nullable=True)

    def __init__(
            self,
            email: str,
            hashed_password: str,
            session_id: str = None,
            reset_token: str = None):
        """
        Initialize a new User instance.

        Args:
            email (str): The user's email.
            hashed_password (str): The user's hashed password.
            session_id (str, optional): The user's session ID.
            reset_token (str, optional): The user's reset token.
        """
        self.email = email
        self.hashed_password = hashed_password
        self.session_id = session_id
        self.reset_token = reset_token
