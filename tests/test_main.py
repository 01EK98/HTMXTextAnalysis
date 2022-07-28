from typing import List
from bs4 import BeautifulSoup
from fastapi.testclient import TestClient
from wordcloud import WordCloud
from main import app, get_sentiment_polarities_per_sentence, get_wordcloud

client = TestClient(app)

# TODO: should make own class of with a dependency overriding mechanism
# @pytest.fixture
# def client() -> TestClient:
#     client = TestClient(app)
#     yield client

TEXT_FOR_ANALYSIS = """
    Lorem ipsum dolor sit amet consectetur adipisicing elit. 
    Porro quibusdam totam, accusantium omnis natus minima. 
    Illo fuga placeat aliquid consectetur.
"""


def overridden_polarities() -> List[float]:
    return [0.0, 0.0, 0.0]


def overridden_wordcloud() -> WordCloud:
    return WordCloud().generate(TEXT_FOR_ANALYSIS)


app.dependency_overrides[get_sentiment_polarities_per_sentence] = overridden_polarities
app.dependency_overrides[get_wordcloud] = overridden_wordcloud


def test_root_returns_index_template():
    response = client.get("/")
    soup = BeautifulSoup(response.text, "lxml")
    assert soup.title.text == "Basic Text Analysis"


def test_sentiments_returns_correct_html():
    response = client.get(f"/sentiments?{TEXT_FOR_ANALYSIS}")
    soup = BeautifulSoup(response.text, "lxml")

    sentiment_polarities = [
        sentiment.text.strip() for sentiment in soup.select("div > div")
    ]

    assert soup.find("p").text == "Sentiment per sentence:"
    assert sentiment_polarities == ["50.0%", "50.0%", "50.0%"]


def test_wordcloud_endpoint_returns_generated_wordcloud():
    response = client.get(f"/wordcloud?{TEXT_FOR_ANALYSIS}")
    soup = BeautifulSoup(response.text, "lxml")

    expected_text_in_svg_nodes = sorted(
        set(TEXT_FOR_ANALYSIS.replace(".", " ").replace(",", " ").split())
    )
    actual_text_in_svg_nodes = sorted(
        [node.text.split()[0] for node in soup.find("svg").find_all("text")]
    )

    assert expected_text_in_svg_nodes == actual_text_in_svg_nodes


def test_wordcloud_endpoint_displays_error_when_no_text_was_provided(mocker):
    app.dependency_overrides = {}
    mocker.patch(
        "main.WordCloud.generate",
        side_effect=ValueError("We need at least 1 word to plot a word cloud, got 0."),
    )
    response = client.get("/wordcloud?text_for_analysis=")
    soup = BeautifulSoup(response.text, "lxml")

    error_message = soup.find("p").text

    assert error_message == "We need at least 1 word to plot a word cloud, got 0."
