# tests the api weather routes

from fastapi.testclient import TestClient
import pytest
from . import mock_data
from httpx import Response
import respx



@respx.mock
def test_simple_valid_weather_request(test_client: TestClient):
	"""
	Ensures that with an active test_client and mocked 
	external APIs that a valid formatted request will get 
	returned a JSON payload with requested weather data.
	"""
	respx.get("https://mock_geoco/search?q=New+York+City+NY+US&api_key=456fakegeokey").mock(
		return_value=Response(200, json=[{"lat": "40.68","lon": "-74.05"}]))
	respx.get("https://mock_openweatherapi/?lat=40.68&lon=-74.05&units=imperial&language=en&appid=123fakeweatherkey").mock(return_value=Response(200, json=mock_data.weather_data_1))
	result = test_client.get(url="http://localhost:8080/api/weather?location=New+York+City+NY+US").json()
	assert result is not None
	assert result["lat"] == 40.68
	assert result["current"]["temp"] == 62.89


def test_api_no_location_key(test_client: TestClient):
	"""
	Ensures that with active test_client if the user doesn't 
	add the 'location' parameter in url (i.e '/api/weather?some+location' 
	instead of 'api/weather?location=some+location') that location 
	the user will get returned a 422 error & message saying as such
	"""
	results = test_client.get(url="http://localhost:8080/api/weather?New+York+City+NY+US")
	assert results.status_code == 422
	assert results.json()["message"] == "Missing required location parameter"


def test_api_no_location_value(test_client: TestClient):
	"""
	With an active test_client checks that if user doesn't
	add a location (value) (i.e '/api/weather?location=')
	the user will get returned a 422 error with message
	"""
	result = test_client.get(url="http://localhost:8080/api/weather?location=")
	assert result.status_code == 422
	assert result.json()["detail"] == "missing location"