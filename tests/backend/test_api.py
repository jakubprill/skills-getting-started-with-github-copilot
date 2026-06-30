from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_get_activities_returns_all():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    # spot-check a known activity
    assert "Chess Club" in data


def test_signup_and_remove_participant_flow():
    activity = "Math Olympiad"
    email = "tester@example.edu"

    # save and ensure clean initial state
    initial_participants = list(activities[activity]["participants"])
    if email in initial_participants:
        activities[activity]["participants"] = [p for p in initial_participants if p != email]
        initial_participants = list(activities[activity]["participants"])

    # signup
    activity_encoded = quote(activity, safe="")
    resp = client.post(f"/activities/{activity_encoded}/signup?email={email}")
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # remove
    resp2 = client.delete(f"/activities/{activity_encoded}/participants?email={email}")
    assert resp2.status_code == 200
    assert email not in activities[activity]["participants"]

    # restore state
    activities[activity]["participants"] = initial_participants
