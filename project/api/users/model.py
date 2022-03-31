import uuid
from typing import Optional

import pytz
from sqlalchemy import false, func, text
from sqlalchemy.dialects.postgresql import UUID

from project.extensions import db
from project.lib import ResourceMixin, ph


class User(db.Model):
    """
    Model related to the user details
    :param UUID 'user_id': Unique Identifier for the user set as primary key
    :param str 'first_name: First Name of the User
    :param str 'last_name': Last Name of the User
    :param str 'username': Unique string identifier used by the end user
    :param str 'hashed_password': d'oh Password
    :param str 'email_id': d'oh Email id
    :param str 'user_type': Student/ Teacher
    """

    __tablename__ = "users"

    user_id = db.Column(
        UUID(as_uuid=True),
        unique=True,
        server_default=text("gen_random_uuid()"),
        nullable=False,
        primary_key=True,
        index=True,
    )
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    hashed_password = db.Column(db.String(255), nullable=False)
    email_id = db.Column(db.String(120), unique=True, nullable=False)
    user_type = db.Column(db.String(64), default=None)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

        self.hashed_password = User.encrypt_password(kwargs.get("hashed_password"))

    @classmethod
    def encrypt_password(cls, plaintext_password: str) -> Optional[str]:
        """
        Hash a Plain Text Password via Argon2. This has won the Password Hashing Competition.
        Some say Bcrypt or PBKDF2is better , but I prefer to choose Argon2 based on my reading
        :param plaintext_password: str
        :return: Encrypted Password: str
        """
        try:
            return ph.hash(plaintext_password)
        except Exception as e:
            raise e

    def has_permission(self, perms):
        """Checks whether the permission exists in the permissions list or not"""
        if isinstance(perms, list):
            for perm in perms:
                if perm in self.role.permissions:
                    return True
            return False
        else:
            if perms not in self.role.permissions:
                return False
            return True
