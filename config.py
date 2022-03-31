import datetime
import os


class BaseConfig:
    """Base configuration"""

    DEBUG = True
    TESTING = False
    FLASK_ENV = "development"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ALGORITHM = "HS512"
    FRONTEND_APP_URL = os.environ.get("FRONTEND_APP_URL")
    SERVER_URI = os.environ.get("SERVER_URI")
    # SECRET_KEY = os.environ.get("SECRET_KEY")
    # if not SECRET_KEY:
    #     SECRET_KEY = os.urandom(64)  # type: ignore
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    JWT_SECRET_KEY = os.environ.get("SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30)
