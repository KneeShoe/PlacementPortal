import logging
from typing import Dict, Tuple

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required

from .schema import blog_schema
from .service import get_blog_details, create_new_blog
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


@jwt_required()
def create_blog():
    try:
        data = request.get_json()
        create_new_blog(data, get_jwt_identity())
    except ServerError as err:
        raise ServerError(message=err.message, status=err.status)
    except BadRequest as err:
        raise BadRequest(message=err.message, status=err.status)
    except Exception as e:
        logging.exception(msg=e)
        raise ServerError("It ain't you, it is me", status=500)
    return "Blog Created!", 200


blog_blueprint.add_url_rule("/getBlogs", "getBlogs", get_blogs, methods=["GET"])
blog_blueprint.add_url_rule("/createBlog", "createBlog", create_blog, methods=["POST"])
