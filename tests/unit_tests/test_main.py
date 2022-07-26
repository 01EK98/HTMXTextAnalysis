from typing import List
from bs4 import BeautifulSoup
from fastapi.testclient import TestClient
from main import app
from tests.conftest import TEXT_FOR_ANALYSIS


def test_root_returns_index_template(client: TestClient):
    response = client.get("/")
    soup = BeautifulSoup(response.text, "lxml")

    assert response.status_code == 200
    assert soup.title.text == "Basic Text Analysis"


def test_sentiments_returns_correct_html(client: TestClient):
    response = client.post("/sentiments", data={"text_for_analysis": TEXT_FOR_ANALYSIS})
    soup = BeautifulSoup(response.text, "lxml")

    sentiment_polarity_percentages = [
        tag_with_percentage.text.strip()
        for tag_with_percentage in soup.select_one(
            # overall sentiment is moved via hyperscript so we omit it here
            "#sentiments ul"
        ).find_all("h3")
    ]

    sentiment_polarity_sentences = [
        tag_with_sentence.text.strip()
        for tag_with_sentence in soup.select_one(
            # overall sentiment is moved via hyperscript so we omit it here
            "#sentiments ul"
        ).find_all("p")
    ]

    overall_sentiment_progress = (
        soup.select_one("#overall-sentiment").select_one("div").text.strip()
    )
    print(soup.select_one("#overall-sentiment").prettify())

    assert response.status_code == 200
    # TODO: add some variety to the test data
    assert overall_sentiment_progress == "60.0%"
    assert sentiment_polarity_percentages == ["92.5%", "40.0%", "70.0%"]
    assert sentiment_polarity_sentences == [
        "Lorem ipsum dolor sit amet consectetur adipisicing elit",
        "Porro quibusdam totam, accusantium omnis natus minima",
        "Illo fuga placeat aliquid consectetur",
    ]


def test_wordcloud_endpoint_returns_generated_wordcloud(client: TestClient):
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


def test_wordcloud_endpoint_displays_error_when_no_text_was_provided(
    client: TestClient, mocker
):
    app.dependency_overrides = {}
    mocker.patch(
        "main.WordCloud.generate",
        side_effect=ValueError("We need at least 1 word to plot a word cloud, got 0."),
    )

    response = client.post("/wordcloud", data={"text_for_analysis": ""})
    soup = BeautifulSoup(response.text, "lxml")

    expected_error_text = soup.select_one("#error-toast-text").text

    assert response.status_code == 200
    assert "We need at least 1 word to plot a word cloud, got 0." in expected_error_text
