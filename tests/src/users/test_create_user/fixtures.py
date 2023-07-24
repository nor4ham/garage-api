import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def user(client: TestClient):
    assert False , "mow from fixture"
