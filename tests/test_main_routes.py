# tests the main / routes that serve website

def test_homepage(test_client):
    """
    GIVEN fastapi test app
    WHEN homepage is called
    THEN check if response code is correct
        and has "WeatherApp"
    """
    response = test_client.get("/")
    assert response.status_code == 200
    assert 'WeatherApp' in response.text
    