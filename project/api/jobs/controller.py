import logging
from typing import Dict, Tuple

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, get_jwt

from .service import authenticate_user, encode_auth_token, encode_refresh_token
from .schema import verify_user_schema
from project.lib import (
    BadRequest,
    ServerError,
    auth_required,
    basic_auth_required,
)

jobs_blueprint = Blueprint(
    "jobs",
    __name__,
)




# jobs_blueprint.add_url_rule("/login", "login", login_user, methods=["POST"])
