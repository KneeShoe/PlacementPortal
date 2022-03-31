"""This module is to define the decorators used in the pilot_project"""
from functools import wraps

from flask_jwt_extended import (
    get_jwt_identity,
    get_jwt,
    verify_jwt_in_request,
)
from flask_jwt_extended.exceptions import (
    InvalidHeaderError,
    NoAuthorizationError,
    WrongTokenError,
)
from jwt import (
    DecodeError,
    ExpiredSignatureError,
    InvalidAlgorithmError,
)

from .errors import BadRequest


def auth_required(*perms):
    """This decorator ensures that the user is registered user and has the permission to perform
    *the actions* as per methods defined in the Role model
    raise: BadRequest if the authentication | permission | blacklisted token |  doesn't exist"""

    def wrapper(view_function):
        """
        Wrapper function
        """

        # noinspection DuplicatedCode
        @wraps(view_function)  # Tells the debugger that it is function wrapper
        def decorator(*args, **kwargs):
            """
            decorator function
            """
            try:
                verify_jwt_in_request()

                from ..api.auth import is_blacklisted_token

                auth_jti = get_jwt()["jti"]
                illegal_token = is_blacklisted_token(token=auth_jti)
                if illegal_token:
                    raise BadRequest(
                        "The token is blacklisted, generate a fresh token",
                        status=401,
                    )

                from ..api.users.service import find_by_identity

                user = find_by_identity(get_jwt_identity())
                if not user:
                    raise BadRequest("Invalid Token, User does not exist", status=401)

                if not user.has_permission(*perms):
                    raise BadRequest(
                        "You do not have necessary permission to perform the requested action",
                        status=403,
                    )
            except (NoAuthorizationError, InvalidHeaderError) as err:
                raise BadRequest(message=err.args[0], status=400)
            except (
                ValueError,
                DecodeError,
                TypeError,
                WrongTokenError,
                InvalidAlgorithmError,
            ):
                raise BadRequest("Illegal token, please check", status=401)
            except (ExpiredSignatureError):
                raise BadRequest("Signature Expired, Please Login again", status=401)
            else:
                return view_function(*args, **kwargs)

        return decorator

    return wrapper


def basic_auth_required(*some_args):
    """This decorator is to handle the basic authentication not authorization"""

    def auth_wrapper(view_function):
        """
        Wrapper function
        """

        # noinspection DuplicatedCode
        @wraps(view_function)  # Tells the debugger that it is function wrapper
        def auth_decorator(*args, **kwargs):
            """
            decorator function
            """
            try:
                error = verify_jwt_in_request()

                from ..api.auth import is_blacklisted_token

                auth_jti = get_jwt()["jti"]
                illegal_token = is_blacklisted_token(token=auth_jti)
                if illegal_token:
                    raise BadRequest(
                        "The token is blacklisted, generate a fresh token",
                        status=401,
                    )

                from ..api.users.service import find_by_identity

                user = find_by_identity(get_jwt_identity())
                if not user:
                    raise BadRequest("Invalid Token, User does not exist", status=401)

            except (ValueError, DecodeError, TypeError, WrongTokenError):
                raise BadRequest("Token decode failed, please check the token", status=401)
            except (NoAuthorizationError, InvalidHeaderError) as err:
                raise BadRequest(message=err.args[0], status=401)
            except BadRequest as err:
                raise BadRequest(message=err.message, status=err.status)
            except (ExpiredSignatureError):
                raise BadRequest("Signature Expired, Please Login again", status=401)
            else:
                return view_function(*args, **kwargs)

        return auth_decorator

    return auth_wrapper
