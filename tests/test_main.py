from bs4 import BeautifulSoup
from fastapi.testclient import TestClient
import pytest
from main import app


@pytest.fixture
def client() -> TestClient:
    client = TestClient(app)
    yield client


def test_root_returns_index_template(client):
    response = client.get("/")
    soup = BeautifulSoup(response.text, "lxml")
    assert soup.title.text == "Document"
