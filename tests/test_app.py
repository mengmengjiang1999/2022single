from views.algorithm import run_algorithm_get

from models import Course, CourseHomework, Problem, Userinfo, db

from .conftest import login


def test_protected_endpoint_returns_json_401(client):
    response = client.post("/course/create", json={"coursename": "Algorithms"})

    assert response.status_code == 401
    assert response.get_json()["status"] is False


def test_legacy_plaintext_password_is_upgraded(app, client):
    with app.app_context():
        user = Userinfo.query.filter_by(username="teacher").one()
        user.password = "teacher-pass"
        db.session.commit()

    response = login(client)

    assert response.status_code == 200
    assert response.get_json()["status"] is True
    with app.app_context():
        upgraded_password = Userinfo.query.filter_by(username="teacher").one().password
        assert upgraded_password != "teacher-pass"
        assert upgraded_password.startswith("pbkdf2:")


def test_course_can_be_created_and_duplicate_is_rejected(app, client):
    login(client)

    response = client.post("/course/create", json={"coursename": " Algorithms "})
    duplicate = client.post("/course/create", json={"coursename": "Algorithms"})

    assert response.status_code == 200
    assert response.get_json()["status"] is True
    assert duplicate.status_code == 409
    with app.app_context():
        course = Course.query.one()
        assert course.username == "teacher"
        assert course.status == 1


def test_teacher_can_add_homework(app, client):
    login(client)
    client.post("/course/create", json={"coursename": "Algorithms"})
    with app.app_context():
        course_id = Course.query.one().id

    response = client.post(
        "/course/addhomework",
        json={
            "courseid": course_id,
            "starttime": 10,
            "endtime": 20,
            "homework": 0,
            "count": 2,
        },
    )

    assert response.status_code == 200
    assert response.get_json()["status"] is True
    with app.app_context():
        homework = CourseHomework.query.one()
        assert homework.courseid == course_id
        assert homework.count == 2


def test_recommendation_endpoint_returns_unique_problem_types(app, client):
    login(client, "student", "student-pass")
    with app.app_context():
        db.session.add_all(
            [
                Problem(
                    username="student",
                    problem_id="a" * 64,
                    problem_type=0,
                    status=0,
                    problem_time=1,
                ),
                Problem(
                    username="student",
                    problem_id="b" * 64,
                    problem_type=0,
                    status=1,
                    problem_time=2,
                ),
            ]
        )
        db.session.commit()

    response = client.get("/recommend")

    assert response.status_code == 200
    assert response.get_json() == {"recommend": [0]}


def test_algorithm_rejects_invalid_or_unowned_problem_ids(client):
    login(client, "student", "student-pass")

    invalid = client.get("/algorithm", query_string={"problem_id": "../../secret"})
    missing = client.post(
        "/algorithm",
        json={"problem_id": "c" * 64, "answer": "1"},
    )

    assert invalid.status_code == 400
    assert missing.status_code == 404


def test_algorithm_rejects_non_string_answer(client):
    login(client, "student", "student-pass")

    response = client.post(
        "/algorithm",
        json={"problem_id": "c" * 64, "answer": 123},
    )

    assert response.status_code == 400


def test_algorithm_result_uses_registered_image_route(app, monkeypatch, tmp_path):
    problem_html = tmp_path / "problem.html"
    problem_html.write_text("problem", encoding="utf-8")
    monkeypatch.setattr(
        "views.run.run",
        lambda *args, **kwargs: (
            str(tmp_path / "input"),
            str(tmp_path / "answer"),
            str(problem_html),
            str(tmp_path / "image"),
        ),
    )
    monkeypatch.chdir(tmp_path)

    with app.test_request_context():
        result = run_algorithm_get(0, "a" * 64, status_now=2)

    assert result["data_image"] == "/algorithm_fig?problem_id=" + "a" * 64
    assert "last_answer" not in result


def test_homework_only_counts_problems_inside_time_window(app, client):
    with app.app_context():
        teacher_course = Course(
            coursename="Algorithms", username="teacher", status=1
        )
        student_membership = Course(
            coursename="Algorithms", username="student", status=0
        )
        db.session.add_all([teacher_course, student_membership])
        db.session.flush()
        db.session.add(
            CourseHomework(
                courseid=teacher_course.id,
                homework=0,
                starttime=10,
                endtime=20,
                count=1,
            )
        )
        db.session.add(
            Problem(
                username="student",
                problem_id="d" * 64,
                problem_type=0,
                status=1,
                problem_time=9,
            )
        )
        db.session.commit()
        course_id = teacher_course.id

    login(client, "student", "student-pass")
    before = client.post("/course/lookhomework", json={"courseid": course_id})
    assert before.get_json()["homework"][0]["finished"] == "❌"

    with app.app_context():
        db.session.add(
            Problem(
                username="student",
                problem_id="e" * 64,
                problem_type=0,
                status=1,
                problem_time=15,
            )
        )
        db.session.commit()

    inside = client.post("/course/lookhomework", json={"courseid": course_id})
    assert inside.get_json()["homework"][0]["finished"] == "✅"
