#!/usr/bin/env python3
""" Main 2
"""
from api.v1.auth.basic_auth import BasicAuth

a = BasicAuth()

print(a.extract_base64_authorization_header(None))  # Expected output: None
print(a.extract_base64_authorization_header(89))  # Expected output: None
print(a.extract_base64_authorization_header("Holberton School"))  # Expected output: None
print(a.extract_base64_authorization_header("Basic Holberton"))  # Expected output: Holberton
print(a.extract_base64_authorization_header("Basic SG9sYmVydG9u"))  # Expected output: SG9sYmVydG9u
print(a.extract_base64_authorization_header("Basic SG9sYmVydG9uIFNjaG9vbA=="))  # Expected output: SG9sYmVydG9uIFNjaG9vbA==
print(a.extract_base64_authorization_header("Basic1234"))  # Expected output: None
