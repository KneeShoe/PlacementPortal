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
    from project.api.users import users_blueprint
    app.register_blueprint(users_blueprint, url_prefix="/api/user")
    from project.api.jobs import jobs_blueprint
    app.register_blueprint(jobs_blueprint, url_prefix="/api/jobs")
    from project.api.blogs import blog_blueprint
    app.register_blueprint(blog_blueprint, url_prefix="/api/blogs")
    return None
