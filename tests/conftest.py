import pytest
from app.main import create_app
from config import Settings
from fastapi.testclient import TestClient

class TestSettings(Settings):
    testing: bool = True


@pytest.fixture(scope="module")
def test_client():
    fastapi_app = create_app(TestSettings)
    
    with TestClient(fastapi_app) as c:
        yield c 