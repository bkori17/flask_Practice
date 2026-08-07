import pytest
from app import app, mongo


@pytest.fixture
def client():
    app.config["TESTING"] = True
    client = app.test_client()

    # Clean only pytest-created records
    with app.app_context():
        mongo.db.students.delete_many({
            "email": {"$regex": "^pytest_"}
        })

        result = mongo.db.students.insert_one({
            "name": "Test Student",
            "email": "pytest_home@test.com",
            "course": "Flask"
        })

        # Save generated MongoDB ID for update test
        app.config["TEST_STUDENT_ID"] = str(result.inserted_id)

    yield client

    # Cleanup only pytest-created records
    with app.app_context():
        mongo.db.students.delete_many({
            "email": {"$regex": "^pytest_"}
        })


def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert b"healthy" in response.data


def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Test Student" in response.data


def test_add_student(client):
    data = {
        "name": "New User",
        "email": "pytest_add@test.com",
        "course": "Python"
    }

    response = client.post(
        '/add',
        data=data,
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"New User" in response.data


def test_update_student(client):
    student_id = app.config["TEST_STUDENT_ID"]

    data = {
        "name": "Updated Name",
        "email": "pytest_update@test.com",
        "course": "Updated Course"
    }

    response = client.post(
        f'/update/{student_id}',
        data=data,
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Updated Name" in response.data


def test_delete_student(client):
    with app.app_context():
        student_id = mongo.db.students.insert_one({
            "name": "Temp User",
            "email": "pytest_delete@test.com",
            "course": "Temp Course"
        }).inserted_id

    response = client.get(
        f'/delete/{student_id}',
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Temp User" not in response.data
