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


@app.route('/sessions', methods=['DELETE'])
def logout():
    """
    Handle the logout functionality for the DELETE /sessions route.

    Retrieves the session_id from the cookie, destroys the session if valid,
    and redirects to home page. If the session is invalid, responds with 403.
    """
    # Step 1: Retrieve session ID from the cookie
    session_id = request.cookies.get("session_id")

    # Step 2: Get the user associated with the session ID
    if session_id is None:
        return abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    # Step 3: Check if the user exists
    if user is None:
        return abort(403)

    # Step 4: Destroy the session
    AUTH.destroy_session(user.id)

    # Step 5: Redirect to the home page and clear the session_id cookie
    response = redirect('/')
    response.delete_cookie('session_id')

    return response


@app.route('/profile', methods=['GET'])
def profile():
    """
    Handle the profile functionality for the GET /profile route.

    Retrieves the session_id from the cookie, finds the user,
    and returns the user's email in a JSON response.
    If session_id is invalid or the user is not found, returns a 403 status.
    """
    # Step 1: Retrieve session ID from the cookie
    session_id = request.cookies.get("session_id")

    # Step 2: Get the user associated with the session ID
    if session_id is None:
        return abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    # Step 3: Check if the user exists
    if user is None:
        return abort(403)

    # Step 4: Return a JSON response with the user's email
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """
    POST /reset_password route that handles generating a reset password token.

    Expects form data with an "email" field.

    If the email is not registered, respond with 403 HTTP status.
    If the email is registered, generate a reset token and return a 200 status
    with the email and token in JSON format.

    Returns:
        Response object: JSON response with either 403 status or reset token.
    """
    # Step 1: Get email from the request form data
    email = request.form.get('email')

    if not email:
        # Step 2: If no email provided, respond with a 403
        return abort(403)

    try:
        # Step 3: Generate reset token using Auth method
        reset_token = auth.get_reset_password_token(email)

        # Step 4: Return 200 status with email and reset token in JSON
        return jsonify({"email": email, "reset_token": reset_token}), 200

    except ValueError:
        # Step 5: If the email is not registered, respond with 403 status
        return abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """
    Handles password reset for the user.

    Expected form data:
        - email: The user's email address
        - reset_token: The token to validate password reset
        - new_password: The new password to set for the user

    Responses:
        - 403: If the token is invalid or any error occurs
        - 200: If the password was successfully updated
    """
    # Step 1: Parse form data
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    if not email or not reset_token or not new_password:
        # If required fields are missing, return a 400 Bad Request
        return abort(400, description="Missing required fields")

    try:
        # Step 2: Validate user and update password
        user = auth.get_user_by_email(email)
        if user is None:
            return abort(403, description="User not found")

        # Step 3: Attempt to update password with the reset token
        auth.update_password(reset_token, new_password)

        # Step 4: Respond with success
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        # Step 5: Handle invalid token or any error, respond with 403
        return abort(403, description="Invalid reset token")

# Running the app is outside of the snippet as this is part of the task
# solution.


if __name__ == "__main__":
    # Run the app on host 0.0.0.0 and port 5000
    app.run(host="0.0.0.0", port=5000)
