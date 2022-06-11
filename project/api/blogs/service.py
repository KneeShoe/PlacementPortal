import uuid
from datetime import datetime
from typing import Optional

from flask import current_app
from sqlalchemy import insert

from project.lib import BadRequest, ServerError, ph
from .model import Blog
from .schema import blog_schema
from ..users import authenticate, User, Student
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required

from ... import db


def get_blog_details():
    """Gets all blogs"""
    blogs: Blog = Blog.query.all()
    bloglist = blog_schema.dump(blogs)
    bloglist.reverse()
    return {"blogs": bloglist}


def create_new_blog(data, identity):
    """Create new blogs"""
    try:
        data['blog_id'] = uuid.uuid4()
        data['time'] = datetime.now()
        data['username'] = identity
        insert_blog = insert(Blog).values(data)
        db.session.execute(insert_blog)
        db.session.commit()
    except Exception:
        raise ServerError("It is not You, It is me", status=500)
    return "Created Job!"
