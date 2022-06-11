from sqlalchemy import false, func, text
from sqlalchemy.dialects.postgresql import UUID
from project.extensions import db


class Blog(db.Model):
    __tablename__ = "blogs"
    blog_id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    time = db.Column(db.Date)
    username = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(256), nullable=True)
    content = db.Column(db.Text, nullable=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
