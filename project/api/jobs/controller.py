import logging
from typing import Dict, Tuple

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required
from .service import getActiveJobs, getJobDetails, create_application, get_user_applications, canApply, add_job_details
from .schema import jobschema, jobdescriptionschema, applicationschema
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
    try:
        jobs = getActiveJobs()
        resp = jobschema.dump(jobs)
        for job in resp:
            job['remaining_days'] = (datetime.strptime(job['end_date'], '%Y-%m-%d') - datetime.now()).days
            job.pop('end_date')
    except ServerError as err:
        raise ServerError(message=err.message, status=err.status)
    except BadRequest as err:
        raise BadRequest(message=err.message, status=err.status)
    except Exception as e:
        logging.exception(msg=e)
        raise ServerError("It ain't you, it is me", status=500)
    return {"active_jobs": resp}, 200


@jwt_required()
def job_description():
    try:
        data = jobdescriptionschema.load(request.get_json(force=True))
        details = getJobDetails(data['job_id'])
        resp = jobschema.dump(details)[0]
        resp["can_apply"] = canApply(data['job_id'], get_jwt_identity())
    except ServerError as err:
        raise ServerError(message=err.message, status=err.status)
    except KeyError as err:
        raise BadRequest(message=err.message, status=err.status)
    except Exception as e:
        logging.exception(msg=e)
        raise ServerError("It ain't you, it is me", status=500)
    return resp, 200


@jwt_required()
def apply_job():
    data = request.get_json(force=True)
    try:
        create_application(resume=data['resume_link'], job_id=data['job_id'], s_id=get_jwt_identity())
    except ServerError as err:
        raise ServerError(message=err.message, status=err.status)
    except KeyError as err:
        raise BadRequest(message=err.message, status=err.status)
    except Exception as e:
        logging.exception(msg=e)
        raise ServerError("It ain't you, it is me", status=500)
    return "Application created", 200


@jwt_required()
def get_applications():
    try:
        applications = get_user_applications(get_jwt_identity())
        resp = applicationschema.dump(applications)
    except ServerError as err:
        raise ServerError(message=err.message, status=err.status)
    except KeyError as err:
        raise BadRequest(message=err.message, status=err.status)
    except Exception as e:
        logging.exception(msg=e)
        raise ServerError("It ain't you, it is me", status=500)
    return {"applications": resp}


def create_job():
    try:
        data = request.get_json(force=True)
        add_job_details(data)
    except ServerError as err:
        raise ServerError(message=err.message, status=err.status)
    except KeyError as err:
        raise BadRequest(message=err.message, status=err.status)
    except Exception as e:
        logging.exception(msg=e)
        raise ServerError("It ain't you, it is me", status=500)
    return "New job created", 200


jobs_blueprint.add_url_rule("/getActiveJobs", "getActiveJobs", active_jobs, methods=["GET"])
jobs_blueprint.add_url_rule("/getJobDescription", "getJobDescription", job_description, methods=["POST"])
jobs_blueprint.add_url_rule("/apply", "Apply", apply_job, methods=["POST"])
jobs_blueprint.add_url_rule("/getApplications", "Applications", get_applications, methods=["GET"])
jobs_blueprint.add_url_rule("/createJob", "createJob", create_job, methods=["POST"])
