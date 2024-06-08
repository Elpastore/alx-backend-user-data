#!/usr/bin/env python3
"""
session_db_auth module
"""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth
from api.v1.auth.session_exp_auth import SessionExpAuth
import base64
from models.user import User
import uuid
import os
from datetime import datetime,  timedelta
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class
    """
    def create_session(self, user_id=None):
        """
        return Session ID
        """
        session_id = super().create_session(user_id)

        if session_id is None:
            return None
        if type(session_id) != str:
            return None
        
        kwargs = {
                'user_id': user_id,
                'session_id': session_id,
            }
        user_session = UserSession(**kwargs)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        returns the User ID by requesting UserSession in the database
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None

        session = UserSession.search({'session_id': session_id})
        if session is None:
            return None

        created_at = session[0].created_at
        if created_at is None:
            return None

        if self.session_duration <= 0:
            return session[0].user_id
        
        exp_time = created_at + timedelta(seconds=self.session_duration)
        if exp_time < datetime.now():
            return None
        return session[0].user_id

    def destroy_session(self, request=None):
        """
        destroy session
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        sessions[0].remove()
        return True
