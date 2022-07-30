from typing import List
from bs4 import BeautifulSoup
from fastapi.testclient import TestClient
import pytest
from wordcloud import WordCloud
from main import app, get_sentiment_polarities_per_sentence, get_wordcloud

TEXT_FOR_ANALYSIS = """
    Lorem ipsum dolor sit amet consectetur adipisicing elit. 
    Porro quibusdam totam, accusantium omnis natus minima. 
    Illo fuga placeat aliquid consectetur.
"""


@pytest.fixture
def client() -> TestClient:
    client = TestClient(app)
    yield client


def overridden_polarities() -> List[float]:
    return [0.0, 0.0, 0.0]


def overridden_wordcloud() -> WordCloud:
    return WordCloud().generate(TEXT_FOR_ANALYSIS)


app.dependency_overrides[get_sentiment_polarities_per_sentence] = overridden_polarities
app.dependency_overrides[get_wordcloud] = overridden_wordcloud


def test_root_returns_index_template(client):
    response = client.get("/")
    soup = BeautifulSoup(response.text, "lxml")

    assert response.status_code == 200
    assert soup.title.text == "Basic Text Analysis"


def test_sentiments_returns_correct_html(client):
    response = client.post("/sentiments", data={"text_for_analysis": TEXT_FOR_ANALYSIS})
    soup = BeautifulSoup(response.text, "lxml")

    sentiment_polarities = [
        sentiment.text.strip() for sentiment in soup.select("div > div")
    ]

    assert response.status_code == 200
    assert soup.find("p").text == "Sentiment per sentence:"
    assert sentiment_polarities == ["50.0%", "50.0%", "50.0%"]


def test_wordcloud_endpoint_returns_generated_wordcloud(client):
    response = client.post(f"/wordcloud", data={"text_for_analysis": TEXT_FOR_ANALYSIS})
    soup = BeautifulSoup(response.text, "lxml")

    expected_text_in_svg_nodes: List[str] = sorted(
        set(TEXT_FOR_ANALYSIS.replace(".", " ").replace(",", " ").split())
    )
    actual_text_in_svg_nodes: List[str] = sorted(
        [node.text.strip() for node in soup.find("svg").find_all("text")]
    )

    assert response.status_code == 200
    assert expected_text_in_svg_nodes == actual_text_in_svg_nodes


def test_wordcloud_endpoint_displays_error_when_no_text_was_provided(client, mocker):
    app.dependency_overrides = {}
    mocker.patch(
        "main.WordCloud.generate",
        side_effect=ValueError("We need at least 1 word to plot a word cloud, got 0."),
    )

    response = client.post("/wordcloud", data={"text_for_analysis": ""})
    soup = BeautifulSoup(response.text, "lxml")

    expected_error_text = soup.find("p").text

    assert response.status_code == 200
    assert "We need at least 1 word to plot a word cloud, got 0." in expected_error_text
