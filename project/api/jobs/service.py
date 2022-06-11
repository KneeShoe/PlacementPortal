import json
import uuid
from typing import Optional

from flask import current_app
from datetime import datetime, timedelta
from project.lib import BadRequest, ServerError, ph
from .model import Job, Applications
from project.extensions import db
from sqlalchemy import select, insert, update, delete


def create_sorted_list(joblist):
    postives = []
    negatives = []
    for job in joblist:
        if job['remaining_days'] >= 0:
            postives.append(job)
        else:
            negatives.append(job)
    positive_sortedlist = sorted(postives, key=lambda d: d['remaining_days'])
    negative_sortedlist = sorted(negatives, key=lambda d: d['remaining_days'], reverse=True)
    resp = positive_sortedlist + negative_sortedlist
    return resp


def getActiveJobs():
    """Returns jobs whose ends dates are 2 days prior to current date"""
    try:
        jobs: Job = Job.query.with_entities(Job.job_id, Job.company_name, Job.job_role, Job.job_type,
                                            Job.end_date).all()
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
    resp = True
    try:
        application: Applications = Applications.query.with_entities(Applications.app_id).filter(
            Applications.s_id == identity).filter(
            Applications.job_id == job_id).one()
        if application:
            resp = False
    except Exception:
        print()
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
        db.session.execute(insert_job)
        db.session.commit()
    except Exception:
        raise ServerError("It is not You, It is me", status=500)
    return "Created Job!"


def update_job_details(data):
    """Update job details"""
    try:
        job_id = data['job_id']
        data.pop('job_id')
        update_job = update(Job).values(data).where(Job.job_id == job_id)
        db.session.execute(update_job)
        db.session.commit()
    except Exception:
        raise ServerError("It is not You, It is me", status=500)
    return "Updated Job!"


def delete_job_service(job_id):
    """Delete job"""
    try:
        Job.query.filter_by(job_id=job_id).delete()
        db.session.commit()
    except Exception:
        raise ServerError("It is not You, It is me", status=500)
    return "Deleted Job!"
