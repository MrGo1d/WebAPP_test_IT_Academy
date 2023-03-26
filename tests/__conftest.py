import pytest
from fastapi.testclient import TestClient
from ..main import app


# #
# # def pytest_addoption(parser):
# #     parser.addoption('--browser_name', action='store', default='chrome',
# #                      help="Choose browser: chrome or firefox")
#
#
@pytest.fixture(scope="function")
def client(client):
    client = TestClient(app)
    yield client
    print("\nclose client..")
