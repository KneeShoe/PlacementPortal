import os
from flask import Flask
from .blueprints_registry import register_blueprints
from .extensions import db, jwt, migrate
from flask_cors import CORS


def create_app(script_info=None):
    """
    Application Factory pattern to create a Flask instance
    :return: Flask app
    """

    app = Flask(__name__)
    CORS(app)

    app_settings = os.environ.get("APP_SETTINGS")
    app.config.from_object(app_settings)
    register_models()
    extensions(app)
    register_blueprints(app)

    @app.shell_context_processor
    def ctx():
        """
        Used to register the app and db to the shell
        :return: Dictionary of mapping the string to instances
        """
        return {"app": app, "db": db}

    return app


def extensions(app: Flask):
    """
    Register the extensions
    """

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db, compare_type=True)

    return None


def register_models():

    from project.api.users import User, Student
    from project.api.jobs import Job

    return None
