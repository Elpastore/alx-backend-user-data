#!/usr/bin/env python3
"""
session_exp_auth module
"""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth
from api.v1.auth.session_auth import SessionAuth
import base64
from models.user import User
import uuid
import os
from datetime import datetime,  timedelta


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class
    """
    def __init__(self):
        """
        init method
        """
        super().__init__()
        try:
            session_duration = os.getenv('SESSION_DURATION')
            self.session_duration = int(session_duration)
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        create session method
        """
        try:
            session_id = super().create_session(user_id)
            """if type(session_id) != str:
                    return None"""
            session_dict = {
                "user_id": user_id,
                "created_at": datetime.now()
            }
            self.user_id_by_session_id[session_id] = session_dict
            return session_id
        except Exception:
            return None

    def user_id_for_session_id(self, session_id=None):
        """
        return user_id from session dictionnary
        """
        if session_id is None:
            return None
        session = self.user_id_by_session_id.get(session_id)
        if session is None:
            return None
        if self.session_duration <= 0:
            return session.get("user_id")
        created_at = session.get("created_at")
        if created_at is None:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None

        return session.get("user_id")
