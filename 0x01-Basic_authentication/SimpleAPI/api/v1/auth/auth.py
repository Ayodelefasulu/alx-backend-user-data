#!/usr/bin/env python3
""" Authentication module """

from flask import Request
from typing import List, TypeVar

# Define a type variable 'User'
User = TypeVar('User')

class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Return True if authentication is required for the path, else False """
        return False

    def authorization_header(self, request: Request = None) -> str:
        """ Return the authorization header from the request """
        return None

    def current_user(self, request: Request = None) -> User:
        """ Return the current user from the request """
        return None
