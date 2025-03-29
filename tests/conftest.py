import pytest
import httpx
from fastapi.testclient import TestClient
from main import app
from config import Settings
from pytest_httpx import HTTPXMock




class TestSettings(Settings):
    TESTING = True

@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as c:
        yield c




