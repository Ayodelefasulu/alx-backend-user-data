#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
# import pdb
import importlib
from api.v1.auth.auth import Auth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# initialize auth variable
auth = None

# Load auth instance based on AUTH_TYPE environment variable
auth_type = getenv("AUTH_TYPE")
if auth_type == "basic_auth":
    # Import BasicAuth from api.v1.auth.basic_auth
    basic_auth_module = importlib.import_module('api.v1.auth.basic_auth')
    BasicAuth = basic_auth_module.BasicAuth
    auth = BasicAuth()
else:
    # Import Auth from api.v1.auth.auth
    auth_module = importlib.import_module('api.v1.auth.auth')
    Auth = auth_module.Auth
    auth = Auth()


@app.before_request
def before_request():
    """ Filter each request """
    # pdb.set_trace()
    if auth is None:
        return

    # List of paths that do not require authentication
    public_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/']

    if request.path not in public_paths:
        if auth.require_auth(request.path, public_paths):
            if auth.authorization_header(request) is None:
                abort(401)  # Unauthorized
            if auth.current_user(request) is None:
                abort(403)  # Forbidden


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not Found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Unauthorized
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """Forbidden
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
