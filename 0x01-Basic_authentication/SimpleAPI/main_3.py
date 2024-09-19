#!/usr/bin/env python3
""" Main 3
"""
from api.v1.auth.basic_auth import BasicAuth

a = BasicAuth()

print(a.decode_base64_authorization_header(None))  # Should print: None
print(a.decode_base64_authorization_header(89))  # Should print: None
print(a.decode_base64_authorization_header("Holberton School"))  # Should print: None
print(a.decode_base64_authorization_header("SG9sYmVydG9u"))  # Should print: Holberton
print(a.decode_base64_authorization_header("SG9sYmVydG9uIFNjaG9vbA=="))  # Should print: Holberton School
print(a.decode_base64_authorization_header(a.extract_base64_authorization_header("Basic SG9sYmVydG9uIFNjaG9vbA==")))  # Should print: Holberton School
