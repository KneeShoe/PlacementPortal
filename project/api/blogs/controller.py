import logging
from typing import Dict, Tuple

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, get_jwt

from .service import encode_auth_token, encode_refresh_token, get_user_details, get_blog_details
from .schema import verify_user_schema
from project.lib import (
    BadRequest,
    ServerError,
    auth_required,
    basic_auth_required,
)

blog_blueprint = Blueprint(
    "blogs",
    __name__,
)


def get_blogs():
    """Method is used to verify the user , login into the system and return the encoded token"""
    try:
        resp = get_blog_details()
    except ServerError as err:
        raise ServerError(message=err.message, status=err.status)
    except BadRequest as err:
        raise BadRequest(message=err.message, status=err.status)
    except Exception as e:
        logging.exception(msg=e)
        raise ServerError("It ain't you, it is me", status=500)
    return resp, 200


def create_blog():
    print("abc")


blog_blueprint.add_url_rule("/getBlogs", "getBlogs", get_blogs, methods=["GET"])
