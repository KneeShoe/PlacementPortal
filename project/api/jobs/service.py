import json
import uuid
from typing import Optional

from flask import current_app
from datetime import datetime, timedelta
from project.lib import BadRequest, ServerError, ph
from .model import Job, Applications
from project.extensions import db
from sqlalchemy import select, insert


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


def canApply(job_id, identity):
    """Check if a user already has applied to the job"""
    try:
        resp = True
        application: Applications = Applications.query.with_entities(Applications.app_id).filter(
            Applications.s_id == identity).filter(
            Applications.job_id == job_id).one()
        if application:
            resp = False
    except Exception:
        print("Can apply!")
    return resp


def create_application(resume, job_id, s_id):
    """Creates job application"""
    try:
        db.session.add(Applications(s_id=s_id, job_id=job_id, resume=resume, status="Applied", date=datetime.now()))
        db.session.commit()
    except Exception:
        raise ServerError("It is not You, It is me", status=500)


def get_user_applications(identity):
    """Get applications for a user"""
    try:
        data = db.session.query(Applications, Job, ).with_entities(Applications.date, Applications.status,
                                                                   Job.company_name, Job.job_type, Job.job_role, Job.ctc
                                                                   ).filter(Applications.s_id == identity
                                                                            ).filter(Applications.job_id == Job.job_id
                                                                                     ).all()
    except Exception:
        raise ServerError("It is not You, It is me", status=500)
    return data


def add_job_details(data):
    """Create a new job"""
    try:
        data['start_date'] = datetime.strptime(data['start_date'], '%Y-%m-%d')
        data['end_date'] = datetime.strptime(data['end_date'], '%Y-%m-%d')
        data['job_id'] = uuid.uuid4()
        insert_job = insert(Job).values(data)
        print(insert_job)
        db.session.execute(insert_job)
        db.session.commit()
    except Exception:
        raise ServerError("It is not You, It is me", status=500)
    return "Created Job!"
