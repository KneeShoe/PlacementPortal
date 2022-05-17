import json
from typing import Optional

from flask import current_app
from datetime import datetime, timedelta
from project.lib import BadRequest, ServerError, ph
from .model import Job, Applications
from project.extensions import db


def getActiveJobs():
    """Returns jobs whose ends dates are 2 days prior to current date"""
    try:
        jobs: Job = Job.query.with_entities(Job.job_id, Job.company_name, Job.job_role, Job.job_type,
                                            Job.end_date).filter(
            Job.end_date + timedelta(days=2) > datetime.now()).all()
        return jobs
    except Exception:
        raise ServerError("It is not You, It is me", status=500)


def getJobDetails(job_id):
    """Returns job descriptions (After opening card)"""
    try:
        jobs: Job = Job.query.with_entities(Job.company_name, Job.job_role, Job.job_type, Job.job_desc, Job.ctc,
                                            Job.end_date, Job.start_date, Job.extras, Job.jd_link, Job.location,
                                            Job.dept_allowed
                                            ).filter(Job.job_id == job_id).all()
        return jobs
    except Exception:
        raise ServerError("It is not You, It is me", status=500)


def create_application(resume, job_id, s_id):
    """Creates job application"""
    try:
        db.session.add(Applications(s_id=s_id, job_id=job_id, resume=resume, status="Applied", date=datetime.now()))
        db.session.commit()
    except Exception:
        raise ServerError("It is not You, It is me", status=500)
