#!/usr/bin/env python3
"""
basic_auth module
"""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth
import base64


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

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """
        decode the Base64 part of header
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decode = base64.b64decode(base64_authorization_header).decode('utf-8')
            return decode
        except Exception:
            return None
