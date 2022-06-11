import urllib.request
import pandas as pd
from sqlalchemy import update

from project import db
from project.api.jobs.model import Applications
from project.lib import ServerError


def update_job_status(url, job_id):
    try:
        datafile = urllib.request.urlopen(url)
        df = pd.read_excel(datafile)
        for row in df[1:]:
            update_job = update(Applications).values(status=row['status']).where(Applications.job_id == job_id,
                                                                                 Applications.s_id == row['usn'])
            db.session.execute(update_job)
        db.session.commit()
    except Exception as e:
        raise ServerError("It ain't you, it is me", status=500)
    return "Jobs Updated"