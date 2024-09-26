#!/usr/bin/env python3
"""
Authentication module for user service
"""

import bcrypt
from user import User
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.hashpw.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The hashed password as bytes.
    """
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initializes the DB instance."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a user if the email is not already taken.

        Args:
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            User: The created user object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            # Try to find an existing user by email
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # If user is not found, proceed to register the user
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate if the login credentials are correct.

        Args:
            email (str): The email of the user.
            password (str): The password to validate.

        Returns:
            bool: True if login is valid, False otherwise.
        """
        try:
            # Find the user by email
            user = self._db.find_user_by(email=email)

            # Check if the provided password matches the stored password
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
        except Exception:
            pass

        return False

    def _generate_uuid(self) -> str:
        """
        Generate a new UUID and return its string representation.

        Returns:
            str: A string representation of a new UUID.
        """
        return str(uuid.uuid4())  # Generate a new UUID and return it as a string
