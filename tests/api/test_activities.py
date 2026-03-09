import src.app as app_module


def test_get_activities_returns_activity_map(client):
    response = client.get("/activities")
    assert response.status_code == 200

    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["max_participants"] == 12


def test_signup_adds_student(client):
    activity_name = "Chess Club"
    email = "new@mergington.edu"

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for {activity_name}",
    }
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_unknown_activity_returns_404(client):
    response = client.post(
        "/activities/Unknown/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_student_returns_400(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_full_activity_returns_400(client):
    activity_name = "Basketball"
    max_participants = app_module.activities[activity_name]["max_participants"]
    app_module.activities[activity_name]["participants"] = [
        f"player{index}@mergington.edu" for index in range(max_participants)
    ]

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": "extra@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"


def test_remove_student_succeeds(client):
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"

    response = client.delete(
        f"/activities/{activity_name}/remove",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Removed {email} from {activity_name}",
    }
    assert email not in app_module.activities[activity_name]["participants"]


def test_remove_unknown_activity_returns_404(client):
    response = client.delete(
        "/activities/Unknown/remove",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_missing_student_returns_400(client):
    activity_name = "Chess Club"
    email = "missing@mergington.edu"

    response = client.delete(
        f"/activities/{activity_name}/remove",
        params={"email": email},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student not signed up for this activity"
