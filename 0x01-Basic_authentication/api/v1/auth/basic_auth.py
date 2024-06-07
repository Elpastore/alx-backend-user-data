#!/usr/bin/env python3
"""
basic_auth module
"""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    BasicAuth class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        return the Base64 part of the Authorization header
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        token = authorization_header.split(" ")[-1]
        return token
