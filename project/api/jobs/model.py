import uuid
from typing import Optional

import pytz
from sqlalchemy import false, func, text
from sqlalchemy.dialects.postgresql import UUID
from project.extensions import db
from project.lib import ResourceMixin, ph


class Job(db.Model):
    __tablename__ = "jobs"
    job_id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    job_role = db.Column(db.String(120))
    job_type = db.Column(db.String(120), nullable=False)
    company_name = db.Column(db.String(256), nullable=True)
    dept_allowed = db.Column(db.String(256), nullable=True)
    ctc = db.Column(db.INT, nullable=True)
    location = db.Column(db.String(256), nullable=True)
    comp_address = db.Column(db.String(256), nullable=True)
    internship = db.Column(db.Boolean, nullable=True)
    job_desc = db.Column(db.String(256), nullable=True)
    placed_slab = db.Column(db.INT, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    jd_link = db.Column(db.String(256), nullable=True)
    extras = db.Column(db.String(256), nullable=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Applications(db.Model):
    __tablename__ = "applications"
    app_id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    s_id = db.Column(
        db.String(80),
        db.ForeignKey("users.username")
    )
    job_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("jobs.job_id"),
    )
    resume = db.Column(db.String(256))
    date = db.Column(db.Date)
    status = db.Column(db.String(50))

