#!/usr/bin/env python3
"""
Authentication module for user service
"""

import uuid
import bcrypt
from user import User
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from bcrypt import hashpw, gensalt
from typing import Optional


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
        return str(
            uuid.uuid4())  # Generate a new UUID and return it as a string

    def create_session(self, email: str) -> str:
        """
        Create a session for the user with the given email.
        Find the user, generate a new UUID, and save it as the session ID.

        Args:
            email (str): The email of the user to create a session for.

        Returns:
            str: The session ID as a string if successful,
                or None if the user is not found.
        """
        try:
            # Find the user by email
            user = self._db.find_user_by(email=email)

            # Generate a new session ID (UUID)
            session_id = self._generate_uuid()

            # Update the user's session_id field with the new session ID
            self._db.update_user(user.id, session_id=session_id)

            # Return the session ID
            return session_id
        except Exception:
            # If user is not found or any other exception occurs, return None
            return None

    def get_user_from_session_id(
            self, session_id: Optional[str]) -> Optional[User]:
        """
        Takes a session_id string and returns the corresponding User or None.

        Args:
            session_id (str): The session ID string.

        Returns:
            User or None: The user corresponding to the session_id or None.
        """
        # Step 1: Check if the session ID is None
        if session_id is None:
            return None

        # Step 2: Try to find the user with the given session_id
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:  # Import this exception from appropriate module
            return None

        # Step 3: Return the user or None
        return user

    def destroy_session(self, user_id: int) -> None:
        """
        Takes a user_id and updates corresponding user's session ID to None.

        Args:
            user_id (int): User ID of user whose session should be destroyed.

        Returns:
            None
        """
        # Step 1: Try to find the user by the given user_id
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None

        # Step 2: Update the user's session ID to None
        self._db.update_user(user.id, session_id=None)

        # Step 3: Return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Finds the user by email and generates a reset password token.

        Args:
            email (str): The email of the user requesting a password reset.

        Returns:
            str: The generated reset password token.

        Raises:
            ValueError: If the user does not exist.
        """
        # Step 1: Find the user by email
        user = self._db.find_user_by(email=email)
        if user is None:
            # Step 2: If user does not exist, raise a ValueError
            raise ValueError("User with this email does not exist.")

        # Step 3: Generate a reset token using uuid
        reset_token = str(uuid.uuid4())

        # Step 4: Update the user's reset_token field in the database
        self._db.update_user(user.id, reset_token=reset_token)

        # Step 5: Return the reset token
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update the password of the user identified by the reset token.

        Args:
            reset_token (str): The reset token used to find the user.
            password (str): The new password to set for the user.

        Raises:
            ValueError: If the reset token is invalid or the user is not found.
        """
        # Step 1: Find user by reset_token
        user: Optional[User] = self._db.find_user_by(reset_token=reset_token)

        if user is None:
            # Step 2: Raise ValueError if no user found
            raise ValueError("Invalid reset token")

        # Step 3: Hash the new password
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())

        # Step 4: Update user's password and reset_token
        self._db.update_user(
            user.id,
            hashed_password=hashed_password,
            reset_token=None)

        # The method returns None implicitly
