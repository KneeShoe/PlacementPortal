"""Just a ping endpoint for testing purpose"""
from flask import Blueprint
from flask.views import MethodView

from automation_scripts.add_users import create_users

ping_blueprint = Blueprint("ping", __name__)


class Ping(MethodView):
    """Just ping endpoint"""
    # noinspection PyMethodMayBeStatic
    def get(self):
        """Return a reply to the ping request"""
        create_users()
        return {"status": "success", "message": "pong!"}


ping_blueprint.add_url_rule("/ping", view_func=Ping.as_view("ping"))
