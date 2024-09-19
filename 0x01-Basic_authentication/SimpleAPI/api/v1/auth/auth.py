#!/usr/bin/env python3
""" Authentication module """

from flask import Request
from typing import List, TypeVar
# import pdb

# Define a type variable 'User'
User = TypeVar('User')


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Return True if authentication is required for the path,
        else False """
        # pdb.set_trace()
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        # Ensure the path and excluded_paths are slash-tolerant
        path = path.rstrip('/')
        for excluded_path in excluded_paths:
            excluded_path = excluded_path.rstrip('/')
            if path == excluded_path:
                return False
        return True

    def authorization_header(self, request: Request = None) -> str:
        """ Return the authorization header from the request """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request: Request = None) -> User:
        """ Return the current user from the request """
        return None
