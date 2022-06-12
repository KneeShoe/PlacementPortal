"""
This will be the entry point to the application, containing the cli commands to run the app etc..
"""
from flask.cli import FlaskGroup

from project import create_app

app = create_app()
cli = FlaskGroup(create_app=create_app)


if __name__ == "__main__":
    cli()
