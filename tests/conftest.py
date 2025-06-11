import pytest
from app.main import create_app
from config import Settings
from fastapi.testclient import TestClient
from app.dependencies.api_client import APIClient
from . import mock_data
from unittest.mock import AsyncMock


class TestSettings(Settings):
    testing: bool = True
    weather_api_key: str = "123fakeweatherkey"
    geocoding_api_key: str = "456fakegeokey"
    base_geocoding_url: str = "https://mock_geoco/search?q="
    base_weather_url: str = "https://mock_openweatherapi?"


@pytest.fixture(scope="module")
def test_client():
    fastapi_app = create_app(TestSettings)
    
    with TestClient(fastapi_app) as c:
        yield c



@pytest.fixture(scope="module")
def mock_geo_data():
    data = {
    "https://mock_geoco/search?q=New+York+City+NY+US&api_key=456fakegeokey": [{"lat": "40.68","lon": "-74.05",}],
    "https://mock_geoco/search?q=Some+Place+aState+US&api_key=456fakegeokey":
        [{"lat": "-28.76","lon": "-141.79",}]}
    return data


@pytest.fixture(scope="module")
def mock_weather_data():
    data = {"https://mock_openweatherapi?lat=40.68&lon=-74.05&exclude=minutely&units=imperial&appid=123fakeweatherkey": mock_data.weather_data_1,
    "https://mock_openweatherapi?lat=-28.76&lon=-141.79&exclude=minutely&units=imperial&appid=123fakeweatherkey": mock_data.weather_data_2}
    return data

