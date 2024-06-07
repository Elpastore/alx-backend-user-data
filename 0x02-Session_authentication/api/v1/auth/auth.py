#!/usr/bin/env python3
"""
auth module
"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """ Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require_auth
        """
        if path is None:
            return True

        if excluded_paths is None or excluded_paths == []:
            return True

        if path in excluded_paths:
            return False

        for excluded_path in excluded_paths:
            if excluded_path.startswith(path):
                return False
            if path.startswith(excluded_path.rstrip("*")):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ authorization_header
        """
        if request is None:
            return None

        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ current_user
        """
        return None

    def session_cookie(self, request=None):
        """
        returns a cookie value from a request
        """
        if request is None:
            return None
        cookie_name = os.getenv("SESSION_NAME")
        return request.cookies.get(cookie_name)
