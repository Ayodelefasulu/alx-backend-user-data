#!/usr/bin/env python3
""" Module for Basic Authentication
"""
from api.v1.auth.auth import Auth
import base64

class BasicAuth(Auth):
    """ Basic Authentication class
    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """ Extracts the Base64 part of the Authorization header

        Args:
            authorization_header (str): The Authorization header

        Returns:
            str: The Base64 part of the header, or None if conditions are not met
        """
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """ Decodes a Base64 authorization header """
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """ Extracts user credentials from the decoded Base64 authorization header """
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password
