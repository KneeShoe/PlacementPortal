import json
from typing import Optional

from flask import current_app
from datetime import datetime, timedelta
from project.lib import BadRequest, ServerError, ph
from .model import Job


def getActiveJobs():
    """Returns jobs whose ends dates are 2 days prior to current date"""
    try:
        jobs: Job = Job.query.with_entities(Job.job_id, Job.company_name, Job.job_role, Job.job_type,
                                            Job.end_date).filter(
            Job.end_date + timedelta(days=2) > datetime.now()).all()
        return jobs
    except Exception:
        raise ServerError("It is not You, It is me", status=500)
