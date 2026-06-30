from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_remove_participant_from_activity():
    initial_participants = list(activities["Chess Club"]["participants"])

    response = client.delete(
        "/activities/Chess%20Club/participants?email=michael@mergington.edu"
    )

    assert response.status_code == 200
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
    assert "Chess Club" in response.json()["message"]

    activities["Chess Club"]["participants"] = initial_participants


def test_signup_updates_activity_participants_immediately():
    initial_participants = list(activities["Chess Club"]["participants"])

    response = client.post(
        "/activities/Chess%20Club/signup?email=student@example.edu"
    )

    assert response.status_code == 200
    assert "student@example.edu" in activities["Chess Club"]["participants"]

    activities["Chess Club"]["participants"] = initial_participants
