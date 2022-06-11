import urllib.request
import pandas as pd
from sqlalchemy import update

from project import db
from project.api.jobs.model import Applications
from project.lib import ServerError


def update_job_status(url, job_id):
    try:
        df = pd.read_excel(url,'Sheet1')
        for i in df.index:
            update_job = update(Applications).values(status=df['status'][i]).where(Applications.job_id == job_id,
                                                                                 Applications.s_id == df['usn'][i])
            db.session.execute(update_job)
        db.session.commit()
    except Exception as e:
        raise ServerError("It ain't you, it is me", status=500)
    return "Jobs Updated"