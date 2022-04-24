from typing import Optional

from flask import current_app

from project.lib import BadRequest, ServerError, ph
from ..users import authenticate, User
from flask_jwt_extended import create_access_token, get_jti, create_refresh_token


def authenticate_user(identity: str, password: str) -> Optional[User]:
    """Authenticates the use"""
    usr = authenticate(identity=identity, password=password)
    if not usr:
        raise BadRequest("Couldn't find your account ", status=404)
    if usr:
        if ph.check_needs_rehash(usr.hashed_password):
            usr.hashed_password = ph.hash(password)
        return usr
    else:
        raise ServerError("Unable to login", status=500)


def encode_auth_token(username: str) -> str:
    """Generates an Authentication token with the constants configured
    :return token
    """
    try:
        acc_tok = create_access_token(
            identity=username,
            expires_delta=current_app.config.get("JWT_ACCESS_TOKEN_EXPIRES"),
        )
        return acc_tok
    except Exception:
        raise ServerError("It is not You, It is me", status=500)

def encode_refresh_token(username: str) -> str:
    """Generates an Refresh token with the constants configured
    :return token
    """
    try:
        ref_tok = create_refresh_token(
            identity=username,
            expires_delta=current_app.config.get("JWT_REFRESH_TOKEN_EXPIRES"),
        )
        return ref_tok
    except Exception:
        raise ServerError("It is not You, It is me", status=500)
