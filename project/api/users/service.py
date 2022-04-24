from typing import Optional
from .model import User, Student
from project.lib import BadRequest, ph
from project.extensions import db
from argon2.exceptions import VerifyMismatchError


def authenticate(identity: str, password: str) -> Optional[User]:
    """Ensure a user is authenticated by checking their existence and verifying their password
    :param identity: Either username or email_id any other identification depends on the business requirement
    :type identity: str
    :param password: User entered password
    :type password: str
    :return Model User Object
    :except returns None
    """
    user = find_by_identity(identity=identity)
    if not user:
        return None
    if not verify_password(plain_password=password, hashed_password=user.hashed_password):
        raise BadRequest("Invalid Password", status=401)
    return user


def find_by_identity(identity: str) -> Optional[User]:
    """
    Find a user by their e-mail or username.

    :param identity: Email or username
    :type identity: str
    :return: User instance
    """
    user: User = User.query.filter((User.username == identity) | (User.email_id == identity)).first()
    if not user:
        raise BadRequest("User Not found", status=400)
    return user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password hash
    :param hashed_password: The hashed password from User model
    :param plain_password: The received password
    :return: bool
    """
    try:
        return ph.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False

def get_student_profile(usn: str):
    """
    Get the profile of a student
    :param usn: USN(id) of student
    :return: Details for profile
    """
    return Student.get_student_details(usn=usn)
