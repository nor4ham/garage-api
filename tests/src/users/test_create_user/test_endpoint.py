from .fixtures import *  # noqa
from fastapi.testclient import TestClient


def test(client: TestClient, user):
    assert False , "mow from test "
