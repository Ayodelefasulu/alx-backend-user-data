#!/usr/bin/env python3
""" Main 4
"""
from api.v1.auth.basic_auth import BasicAuth

a = BasicAuth()

print(a.extract_user_credentials(None))  # Should print: (None, None)
print(a.extract_user_credentials(89))  # Should print: (None, None)
print(a.extract_user_credentials("Holberton School"))  # Should print: (None, None)
print(a.extract_user_credentials("Holberton:School"))  # Should print: ('Holberton', 'School')
print(a.extract_user_credentials("bob@gmail.com:toto1234"))  # Should print: ('bob@gmail.com', 'toto1234')
