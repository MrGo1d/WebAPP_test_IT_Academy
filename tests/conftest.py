import pytest
from fastapi.testclient import TestClient
from WebAPP_test_IT_Academy.main import app


@pytest.fixture(scope="function")
def client(app):
    client = TestClient(app)
    yield client
    print("\nclose client..")
