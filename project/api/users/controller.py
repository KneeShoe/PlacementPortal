import logging

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from .schema import verify_user_schema
from .service import get_student_profile
from ...lib import BadRequest, ServerError

users_blueprint = Blueprint(
    "user",
    __name__,
)


@jwt_required()
def get_user_details():
    try:
        resp = get_student_profile(usn=get_jwt_identity())
    except ServerError as err:
        raise ServerError(message=err.message, status=err.status)
    except BadRequest as err:
        raise BadRequest(message=err.message, status=err.status)
    except Exception as e:
        logging.exception(msg=e)
        raise ServerError("It ain't you, it is me", status=500)
    return resp, 200


users_blueprint.add_url_rule("/getDetails", "getdetails", get_user_details, methods=["GET"])
