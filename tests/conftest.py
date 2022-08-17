from typing import List, Literal, NoReturn
import pytest
import requests
import uvicorn

from multiprocessing import Process
from wordcloud import WordCloud
from fastapi.testclient import TestClient
from tenacity import retry, stop_after_delay, wait_fixed
from main import app

from main import (
    app,
    get_sentiment_polarities_per_sentence,
    get_sentiment_polarity,
    get_wordcloud,
    SentenceSentiment,
)

TEXT_FOR_ANALYSIS = """
    Lorem ipsum dolor sit amet consectetur adipisicing elit. 
    Porro quibusdam totam, accusantium omnis natus minima. 
    Illo fuga placeat aliquid consectetur.
"""
APP_HOST = "localhost"
APP_PORT = 5000
APP_URL = f"http://{APP_HOST}:{APP_PORT}"


def overridden_sentiment_polarities_per_sentence() -> List[SentenceSentiment]:
    return [
        # these sentences are very neutral, the sentiments are modified for some variety
        SentenceSentiment(
            "Lorem ipsum dolor sit amet consectetur adipisicing elit", 0.85
        ),
        SentenceSentiment(
            "Porro quibusdam totam, accusantium omnis natus minima", -0.2
        ),
        SentenceSentiment("Illo fuga placeat aliquid consectetur", 0.4),
    ]


def overridden_overall_sentiment_polarity() -> float:
    return 0.2


def overridden_wordcloud() -> WordCloud:
    return WordCloud().generate(TEXT_FOR_ANALYSIS)


app.dependency_overrides[
    get_sentiment_polarities_per_sentence
] = overridden_sentiment_polarities_per_sentence
app.dependency_overrides[get_sentiment_polarity] = overridden_overall_sentiment_polarity
app.dependency_overrides[get_wordcloud] = overridden_wordcloud


@pytest.fixture
def client() -> TestClient:
    client = TestClient(app)
    yield client


def run_uvicorn() -> None:
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)


@retry(stop=stop_after_delay(10), wait=wait_fixed(0.01))
def is_server_running() -> Literal[True] | NoReturn:
    if requests.get(APP_URL).ok:
        return True
    raise


# TODO: try to integrate pylenium with async server
@pytest.fixture(scope="session", autouse=True)
def run_server() -> None:
    process = Process(target=run_uvicorn, daemon=True)
    process.start()

    if is_server_running():
        yield
    process.kill()
