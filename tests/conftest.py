import asyncio
from typing import List
import pytest
import uvicorn

from multiprocessing import Process
from wordcloud import WordCloud
from fastapi.testclient import TestClient
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


@pytest.fixture(scope="session")
def client() -> TestClient:
    client = TestClient(app)
    yield client


@pytest.fixture(scope="session")
async def server() -> None:
    process = Process(
        target=lambda: uvicorn.run(app, host="127.0.0.1", port=5000), daemon=True
    )
    process.start()
    # TODO: find a cleaner way to do this
    await asyncio.sleep(0.2)  # wait for server to start
    yield
    process.kill()
