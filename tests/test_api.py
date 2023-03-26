from fastapi.testclient import TestClient
import pytest
from WebAPP_test_IT_Academy import base
from WebAPP_test_IT_Academy import main

#
# import sys
# print(sys.path)
# print(base.SQLALCHEMY_DATABASE_URL)

def test_main_url(client):
    response = client.get('/')
    assert response.status_code == '200'
