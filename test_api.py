from fastapi.testclient import TestClient

from main import app


client = TestClient(app)
token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyb290IiwiZXhwIjoxNjgyMDg0NDkyfQ.WU_IauAKctcJXyqOibyBAzZq5R0EH6WwdyZVRT5rT2k"


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
