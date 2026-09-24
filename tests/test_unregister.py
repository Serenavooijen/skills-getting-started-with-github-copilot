from pathlib import Path
import sys

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from app import app


def test_unregister_participant_removes_email():
    client = TestClient(app)

    response = client.delete("/activities/Chess Club/signup?email=michael@mergington.edu")

    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"

    activities = client.get("/activities").json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_unknown_participant_returns_404():
    client = TestClient(app)

    response = client.delete("/activities/Chess Club/signup?email=not-here@mergington.edu")

    assert response.status_code == 404
