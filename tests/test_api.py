import httpx
import pytest
from pytest_httpx import HTTPXMock
from dependencies import APIClient
import json


@pytest.markasyncio
def test_api_weather(test_client, httpx_mock: HTTPXMock):
    """
    GIVEN flask app and mocked httpx api client
    WHEN '/api/weather?city=seattle' is requested
    THEN check if response is correct
    """
    httpx_mock.add_response(
        method="GET", 
        url="http://localhost:8080/api/weather?city=torino", 
        status_cose=200, 
        content=json.dumps({
                                "weather": [{
                                                "id": 501,
                                                "main": "Rain",
                                                "description": "moderate rain",
                                                "icon": "10d"
                                            }]
                            }).encode('utf-8')
        )
    result = test_client.get(url="/api/weather?city=torino")
    assert result is not None
    