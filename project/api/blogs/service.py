from typing import Optional

from flask import current_app

from project.lib import BadRequest, ServerError, ph
from .model import Blog
from ..users import authenticate, User, Student
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required


def get_blog_details():
    """Gets all blogs"""
    blogs: Blog = Blog.query().all()
    print(blogs)
    return blogs


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


def get_user_details(id):
    """Returns user details"""
    try:
        student: Student = Student.query.filter((Student.user_id == id)).first()
    except Exception:
        raise ServerError("It is not You, It is me", status=500)
    return student
