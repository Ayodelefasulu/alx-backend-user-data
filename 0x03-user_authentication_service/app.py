#!/usr/bin/env python3
"""
Flask app to handle user registration with Auth
"""

from flask import Flask, request, jsonify
from auth import Auth

# Create an instance of the Auth class
AUTH = Auth()

# Create a Flask app instance
app = Flask(__name__)


@app.route("/users", methods=["POST"])
def users():
    """
    POST /users route to register a user with email and password.

    Returns:
        JSON response with a success or error message.
    """
    # Get the form data from the request
    email = request.form.get('email')
    password = request.form.get('password')

    # Ensure both email and password are provided
    if not email or not password:
        return jsonify({"message": "Missing email or password"}), 400

    try:
        # Try to register the user
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        # If the user already exists, return an error
        return jsonify({"message": "email already registered"}), 400

@app.route('/sessions', methods=['POST'])
def login():
    """Handles user login and creates a session."""
    email = request.form.get('email')
    password = request.form.get('password')

    # Validate the login credentials
    if not AUTH.valid_login(email, password):
        abort(401)  # Unauthorized

    # Create a session for the user
    session_id = AUTH.create_session(email)

    # Create response
    response = jsonify({"email": email, "message": "logged in"})

    # Set the session ID as a cookie in the response
    response.set_cookie("session_id", session_id)

    return response


if __name__ == "__main__":
    # Run the app on host 0.0.0.0 and port 5000
    app.run(host="0.0.0.0", port=5000)
