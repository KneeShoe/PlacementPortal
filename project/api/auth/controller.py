import logging
from typing import Dict, Tuple

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, get_jwt

from .service import authenticate_user, encode_auth_token, encode_refresh_token, get_user_details
from .schema import verify_user_schema
from project.lib import (
    BadRequest,
    ServerError,
    auth_required,
    basic_auth_required,
)

auth_blueprint = Blueprint(
    "auth",
    __name__,
)


def login_user() -> Tuple[Dict[str, str], int]:
    """Method is used to verify the user , login into the system and return the encoded token"""
    val = verify_user_schema.validate(request.json)
    if val:
        raise BadRequest(val, status=400)
    try:
        u = verify_user_schema.load(request.get_json(force=True))
        auth_user = authenticate_user(identity=u["username"], password=u["hashed_password"])
        resp = {
            "access_token": encode_auth_token(auth_user.username),
            "refresh_token": encode_refresh_token(auth_user.username),
            "role": auth_user.user_type,
            "username": auth_user.username
        }
        if auth_user.user_type == "student":
            user = get_user_details(auth_user.user_id)
            resp = {
                "access_token": encode_auth_token(auth_user.username),
                "refresh_token": encode_refresh_token(auth_user.username),
                "role": auth_user.user_type,
                "dept": user.dept,
                "username": auth_user.username
            }
    except ServerError as err:
        raise ServerError(message=err.message, status=err.status)
    except BadRequest as err:
        raise BadRequest(message=err.message, status=err.status)
    except Exception as e:
        logging.exception(msg=e)
        raise ServerError("It ain't you, it is me", status=500)
    return resp, 200


auth_blueprint.add_url_rule("/login", "login", login_user, methods=["POST"])
