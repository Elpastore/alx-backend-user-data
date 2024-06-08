#!/usr/bin/env python3
""" user_session module
"""
from models.base import Base


class UserSession(Base):
    """
    UserSession class
    """
    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a User session instance
        """
        super().__init__(*args, **kwargs)
        user_id = kwargs.get('user_id')
        session_id = kwargs.get('session_id')
