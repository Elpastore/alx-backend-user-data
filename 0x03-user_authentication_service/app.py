#!/usr/bin/env python3
"""
app module
"""
from flask import Flask, jsonify, request
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def home() -> str:
    """
    welcome route
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register() -> str:
    """
    register endpoint
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or password is None:
        return jsonify({"message": "email and password are required"}), 400
    try:
        new_user = AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"})


if __name__ == '__main__':
    """
    main app
    """
    app.run(host="0.0.0.0", port=5000, debug=False)
