#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import User, Base


class DB:
    """DB class for interacting with the database."""

    def __init__(self) -> None:
        """Initialize a new DB instance."""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to the database and returns the User object.

        Args:
            email (str): The user's email.
            hashed_password (str): The user's hashed password.

        Returns:
            User: The newly added User object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()  # Save to the database
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find user by arbitrary keyword arguments.
        Returns a User object if found, else raises an error.

        :param kwargs: Arbitrary keyword arguments to filter users by.
        :return: User object
        :raises NoResultFound: If no matching user is found.
        :raises InvalidRequestError: If invalid query arguments are passed.
        """
        try:
            # Query the user table and filter by keyword arguments
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            # Raise NoResultFound if no user matches the query
            raise NoResultFound("No user found matching the query.")
        except InvalidRequestError:
            # Raise InvalidRequestError if the query arguments are invalid
            raise InvalidRequestError("Invalid query arguments.")

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a user's attributes in the database.

        :param user_id: The ID of the user to update.
        :param kwargs: Arbitrary keyword arguments representing the user's attributes to update.
        :raises ValueError: If a given attribute does not exist on the User model.
        """
        try:
            # Find the user by their ID
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError(f"User with id {user_id} not found.")

        # Update the user's attributes
        for key, value in kwargs.items():
            # Ensure the attribute exists on the user model
            if not hasattr(user, key):
                raise ValueError(f"Attribute '{key}' does not exist on User model.")
            # Set the attribute dynamically
            setattr(user, key, value)

        # Commit the changes to the database
        self._session.commit()
