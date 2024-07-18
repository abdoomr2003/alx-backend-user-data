#!/usr/bin/env python3
"""
Route module for the API
"""
import logging
from flask import Flask, jsonify, request, abort
from auth import Auth
# logging.disable(logging.WARNING)

AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """
    WELCOME
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """
    create user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """POST /sessions
    Return:
        - 401: if email or password is incorrect
        - 200: if login is successful
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    result = jsonify({"email": email, "message": "logged in"})
    result.status_code = 200
    result.set_cookie("session_id", session_id)
    return result


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """DELETE /sessions
    Return:
        - 403: if session_id is None
        - 200: if logout is successful
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """GET /profile
    Return:
        - 403: if session_id is None
        - 200: if login is successful
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """POST /reset_password
    Return:
        - 403: if email is not registered
        - 200: if reset token is successful
    """
    email = request.form.get('email')
    reset_token = AUTH.get_reset_password_token(email)
    if reset_token is None:
        abort(403)
    return jsonify({"email": email, "reset_token": reset_token}), 200


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """PUT /reset_password
    Return:
        - 403: if email is not registered
        - 400: if reset token is invalid
        - 200: if update password is successful
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    if not AUTH.update_password(reset_token, new_password):
        abort(400)
    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
