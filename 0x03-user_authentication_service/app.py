#!/usr/bin/env python3
"""
app module
"""
from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def home() -> str:
    """
    welcome route
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == '__main__':
    """
    main app
    """
    app.run(host="0.0.0.0", port=5000, debug=False)
