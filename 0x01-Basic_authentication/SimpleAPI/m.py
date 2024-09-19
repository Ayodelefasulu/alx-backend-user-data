#!/usr/bin/env python3
""" Main 2 for testing """
from api.v1.auth.auth import Auth
from flask import Request

a = Auth()

# Simulate a Flask request
class MockRequest:
    def __init__(self, headers):
        self.headers = headers
    def get(self, key, default=None):
        return self.headers.get(key, default)

request = MockRequest(headers={'Authorization': 'Test'})

print(a.require_auth("/api/v1/status/", ["/api/v1/status/"]))
print(a.require_auth("/api/v1/users", ["/api/v1/status/"]))
print(a.authorization_header(request))
print(a.current_user(request))

