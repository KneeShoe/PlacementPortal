from flask import Flask


def register_blueprints(app: Flask):
    """
    Register Blueprint paths for packages
    :param app:
    :return: None
    """

    from project.api.ping import ping_blueprint
    app.register_blueprint(ping_blueprint, url_prefix="/api")
    from project.api.auth import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/api")
    return None
