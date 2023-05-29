from flask import request, g, current_app

import jwt

from datetime import timedelta


def decode_session_token(token):
    try:
        return jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            leeway=timedelta(seconds=10),
            algorithms=['HS256']
        )
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def get_current_user():
    session_token = request.headers.get('Authorization')

    if session_token:
        # Get the token from the header
        session_token = session_token.replace('Bearer ', '')
        decoded_token = decode_session_token(session_token)
        if decoded_token:
            g.current_user = decoded_token


def has_permission(permission, user=None):
    user = user or g.current_user
    if not user:
        return False
    return user.get('permissions') >= permission
