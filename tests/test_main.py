from tkinter.tix import TEXT
from bs4 import BeautifulSoup
from fastapi.testclient import TestClient
from numpy import False_
import pytest
from main import app, get_sentiment_polarities_per_sentence

client = TestClient(app)

# TODO: should make own class of with a dependency overriding mechanism
# @pytest.fixture
# def client() -> TestClient:
#     client = TestClient(app)
#     yield client

TEXT_FOR_ANALYSIS = "Google, which has a dominant share in the markets for internet search, \
    navigation and video streaming, is considered a bellwether for the strength of online \
    advertising. The slowdown, after disappointing results from social-media companies \
    Twitter Inc. and Snap Inc. last week, suggests further weakness in an industry \
    critical to the health of many internet companies."


def overridden_polarities():
    return [0.0, -0.019999999999999997]


app.dependency_overrides[get_sentiment_polarities_per_sentence] = overridden_polarities


def test_root_returns_index_template():
    response = client.get("/")
    soup = BeautifulSoup(response.text, "lxml")
    assert soup.title.text == "Document"


def test_sentiments_returns_correct_html():
    response = client.get(f"/sentiments?{TEXT_FOR_ANALYSIS}")
    soup = BeautifulSoup(response.text, "lxml")
    sentiment_polarities = [
        sentiment.text.strip() for sentiment in soup.select("div > div")
    ]

    assert soup.find("p").text == "Sentiment per sentence:"
    assert sentiment_polarities == ["50.0%", "49.0%"]
