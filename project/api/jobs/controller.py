import logging
from typing import Dict, Tuple

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, get_jwt
from .service import getActiveJobs
from .schema import jobschema

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


def active_jobs():
    jobs = getActiveJobs()
    resp = jobschema.dump(jobs)
    return {"active_jobs": resp}


jobs_blueprint.add_url_rule("/getActiveJobs", "getActiveJobs", active_jobs, methods=["GET"])
