import datetime
import urllib.request
import uuid

import pandas as pd
from sqlalchemy import update, insert

from project import db
from project.api.jobs.model import Applications
from project.api.users.model import User, Student
from project.lib import ServerError, ph


def update_job_status(url, job_id, ctc, company_name):
    try:
        df = pd.read_excel(url, 'Sheet1')
        for i in df.index:
            update_job = update(Applications).values(status=df['status'][i]).where(Applications.job_id == job_id,
                                                                                   Applications.s_id == df['usn'][i])
            if df['status'][i] == 'accepted':
                if ctc<699999:
                    update_student = update(Student).values(slab1=company_name).where(Student.s_id == df['usn'][i])
                elif ctc>2000000:
                    update_student = update(Student).values(slab3=company_name).where(Student.s_id == df['usn'][i])
                else:
                    update_student = update(Student).values(slab2=company_name).where(Student.s_id == df['usn'][i])
            db.session.execute(update_job)
        db.session.commit()
    except Exception as e:
        raise ServerError("It ain't you, it is me", status=500)
    return "Jobs Updated"


def create_users():
    try:
        df = pd.read_csv("/home/kneeshoeee/PycharmProjects/PlacementPortal/automation_scripts/user_data.csv")
        for i in df.index:
            password = ph.hash(df['first_name'][i] + df['dob'][i])
            user_id = uuid.uuid4()
            batch = '20' + df['username'][i][3:4]
            add_user = insert(User).values(user_id=user_id, first_name=df['first_name'][i],
                                           last_name=df['last_name'][i],
                                           username=df['username'][i], hashed_password=password, user_type='student',
                                           email_id=df['email_id'][i], phone_number=str(df['phone_number'][i]))
            add_student = insert(Student).values(user_id=user_id, dept=df['dept'][i], batch=batch,
                                                 dob=datetime.datetime.strptime(df['dob'][i], '%d-%m-%Y'),
                                                 sem=str(df['sem'][i]), sec=df['sec'][i], cgpa=str(df['cgpa'][i]))
            db.session.execute(add_user)
            db.session.execute(add_student)
        db.session.commit()
    except Exception as e:
        raise ServerError("It ain't you, it is me", status=500)
    return "Users Created"
