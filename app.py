import os

import click
from flask import Flask
from flask_migrate import Migrate

from models import db


migrate = Migrate()


def create_app(test_config=None):
    """Create and configure the Flask application."""
    flask_app = Flask(__name__)
    flask_app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-only-change-me"),
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            "DATABASE_URL", "sqlite:///site.db"
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        flask_app.config.update(test_config)

    db.init_app(flask_app)
    migrate.init_app(flask_app, db)

    from views.algorithm import bluealgorithm
    from views.course import bluecourse
    from views.problem import blueproblem
    from views.test import bluetest
    from views.tool import bluetool
    from views.user import blueuser, login_manager

    login_manager.init_app(flask_app)
    for blueprint in (
        blueuser,
        bluealgorithm,
        bluetool,
        bluetest,
        blueproblem,
        bluecourse,
    ):
        flask_app.register_blueprint(blueprint)

    @flask_app.cli.command("init-db")
    @click.option("--drop", is_flag=True, help="Drop tables before creating them.")
    def init_db(drop):
        """Initialize the application database."""
        if drop:
            db.drop_all()
        db.create_all()
        click.echo("Initialized database.")

    return flask_app


app = create_app()


if __name__ == "__main__":
    from werkzeug.middleware.proxy_fix import ProxyFix

    from views.run import pre_compile

    app.wsgi_app = ProxyFix(app.wsgi_app)
    pre_compile()
    app.run()
