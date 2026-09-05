import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from models import Userinfo, db


@pytest.fixture()
def app():
    flask_app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret",
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
        }
    )

    with flask_app.app_context():
        db.create_all()
        db.session.add_all(
            [
                Userinfo(
                    username="teacher",
                    password=generate_password_hash("teacher-pass"),
                    email="teacher@example.com",
                    submitted=0,
                    correct=0,
                ),
                Userinfo(
                    username="student",
                    password=generate_password_hash("student-pass"),
                    email="student@example.com",
                    submitted=0,
                    correct=0,
                ),
            ]
        )
        db.session.commit()

    yield flask_app

    with flask_app.app_context():
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def login(client, username="teacher", password="teacher-pass"):
    return client.post(
        "/login",
        json={"username": username, "password": password},
    )
