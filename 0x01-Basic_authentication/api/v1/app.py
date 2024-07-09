#!/usr/bin/env python3
"""
task 1: Error handler: Unauthorized
"""
from os import getenv
from api.v1.views import app_views
from typing import Tuple, Any
from flask_cors import (CORS, cross_origin)
from flask import Flask, jsonify, abort, request
import os

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
AUTH_TYPE = os.getenv("AUTH_TYPE")
if AUTH_TYPE == "auth":
    from api.v1.auth.auth import Auth

    auth = Auth()
elif AUTH_TYPE == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth

    auth = BasicAuth()


@app.errorhandler(401)
def not_found(error) -> str:
    """ handler not found
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def noacess(error) -> Tuple[Any, int]:
    """
        Your access is not authorized
    Args:
        error: Error code

    Returns:
      A string for the error
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request():
    """
    Each request is handled with its proper route
    """
    if auth is None:
        pass
    else:
        excluded = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/'
        ]
        if auth.require_auth(request.path, excluded):
            if auth.authorization_header(request) is None:
                abort(401, description="Unauthorized")
            if auth.current_user(request) is None:
                abort(403, description="Forbidden")


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
