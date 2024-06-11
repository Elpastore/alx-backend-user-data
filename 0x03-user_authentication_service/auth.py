#!/usr/bin/env python3
"""
auth module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    method that hash a given password
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password
