import logging
from typing import Dict, Tuple

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required

from automation_scripts import update_job_status
from .service import getActiveJobs, getJobDetails, create_application, get_user_applications, canApply, add_job_details, \
    update_job_details, create_sorted_list, delete_job_service, get_statistics_details
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
    """Get list of jobs"""
    try:
        jobs = getActiveJobs()
        joblist = jobschema.dump(jobs)
        for job in joblist:
            job['remaining_days'] = (datetime.strptime(job['end_date'], '%Y-%m-%d') - datetime.now()).days
            job.pop('end_date')
        resp = create_sorted_list(joblist)
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
    """Add job description"""
    try:
        data = jobdescriptionschema.load(request.get_json(force=True))
        details = getJobDetails(data['job_id'])
        resp = jobschema.dump(details)[0]
        resp["can_apply"] = canApply(data['job_id'], get_jwt_identity())
        remianing_days = (datetime.strptime(resp['end_date'], '%Y-%m-%d') - datetime.now()).days
        if remianing_days > 0:
            resp['old_job'] = False
        else:
            resp['old_job'] = True
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
    """Apply for job"""
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
    """Get all applications"""
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
    """Create new Job"""
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


def update_job():
    """Update job details"""
    try:
        data = request.get_json(force=True)
        resp = update_job_details(data)
    except ServerError as err:
        raise ServerError(message=err.message, status=err.status)
    except KeyError as err:
        raise BadRequest(message=err.message, status=err.status)
    except Exception as e:
        logging.exception(msg=e)
        raise ServerError("It ain't you, it is me", status=500)
    return resp, 200


def update_status():
    """Update status of job applicant"""
    try:
        data = request.get_json(force=True)
        resp = update_job_status(data['url'], data['job_id'], data['ctc'], data['company_name'])
    except ServerError as err:
        raise ServerError(message=err.message, status=err.status)
    except KeyError as err:
        raise BadRequest(message=err.message, status=err.status)
    except Exception as e:
        logging.exception(msg=e)
        raise ServerError("It ain't you, it is me", status=500)
    return resp, 200


def delete_job():
    """Delete Job"""
    try:
        data = request.get_json()
        delete_job_service(data['job_id'])
    except ServerError as err:
        raise ServerError(message=err.message, status=err.status)
    except KeyError as err:
        raise BadRequest(message=err.message, status=err.status)
    except Exception as e:
        logging.exception(msg=e)
        raise ServerError("It ain't you, it is me", status=500)
    return "Job Deleted", 200

def get_statistics():
    """Return statistics of placements"""
    try:
        resp = get_statistics_details()
    except ServerError as err:
        raise ServerError(message=err.message, status=err.status)
    except KeyError as err:
        raise BadRequest(message=err.message, status=err.status)
    except Exception as e:
        logging.exception(msg=e)
        raise ServerError("It ain't you, it is me", status=500)
    return resp, 200


jobs_blueprint.add_url_rule("/statistics", "statistics", get_statistics, methods=["GET"])
jobs_blueprint.add_url_rule("/getActiveJobs", "getActiveJobs", active_jobs, methods=["GET"])
jobs_blueprint.add_url_rule("/getJobDescription", "getJobDescription", job_description, methods=["POST"])
jobs_blueprint.add_url_rule("/apply", "Apply", apply_job, methods=["POST"])
jobs_blueprint.add_url_rule("/getApplications", "Applications", get_applications, methods=["GET"])
jobs_blueprint.add_url_rule("/createJob", "createJob", create_job, methods=["POST"])
jobs_blueprint.add_url_rule("/updateJob", "updateJob", update_job, methods=["PUT"])
jobs_blueprint.add_url_rule("/updateJobStatus", "updateJobStatus", update_status, methods=["POST"])
jobs_blueprint.add_url_rule("/deleteJob", "deleteJob", delete_job, methods=["POST"])
