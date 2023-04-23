from fastapi.testclient import TestClient

from main import app

from config import settings


client = TestClient(app)
token = ""


def test_login():
    global token
    response = client.post("/auth/login", data={"username": settings.ROOT_USER, "password": settings.ROOT_PASS})
    assert response.status_code == 200
    assert "access_token" in response.json()
    token = f"Bearer {response.json()['access_token']}"


def test_get_weather():
    city = "Tehran"
    response = client.get(f"/v1/weather?city={city}", headers={"Authorization": token})
    assert response.status_code == 200
    assert response.json()["city"] == city
    assert "Temp" in response.json()
    assert "Hum" in response.json()


def test_get_weather_multiple_cities():
    cities = ["Tehran", "London", "New York", "Sydney", "Tokyo"]
    for city in cities:
        response = client.get(f"/v1/weather?city={city}",headers={"Authorization": token})
        assert response.status_code == 200
        assert response.json()["city"] == city
        assert "Temp" in response.json()
        assert "Hum" in response.json()
