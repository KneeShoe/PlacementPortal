import logging
from typing import Dict, Tuple

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, get_jwt
from .service import getActiveJobs, getJobDetails
from .schema import jobschema, jobdescriptionschema
from datetime import datetime

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
    for job in resp:
        job['remaining_days'] = (datetime.strptime(job['end_date'], '%Y-%m-%d') - datetime.now()).days
        job.pop('end_date')
    return {"active_jobs": resp}

def job_description():
    data = jobdescriptionschema.load(request.get_json(force=True))
    details = getJobDetails(data['job_id'])
    resp = jobschema.dump(details)
    return resp[0]

jobs_blueprint.add_url_rule("/getActiveJobs", "getActiveJobs", active_jobs, methods=["GET"])
jobs_blueprint.add_url_rule("/getJobDescription", "getJobDescription", job_description, methods=["POST"])
