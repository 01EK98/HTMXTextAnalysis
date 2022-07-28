from typing import Dict, List
from nltk import tokenize
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount("/assets", StaticFiles(directory="./assets"), name="assets")

templates = Jinja2Templates(directory="./")


async def get_sentiment_polarities_per_sentence(text_for_analysis: str) -> List[float]:
    sentences = tokenize.sent_tokenize(text_for_analysis)
    return [TextBlob(sentence).sentiment.polarity for sentence in sentences]


async def get_wordcloud(text_for_analysis: str) -> WordCloud | Dict[str, str]:
    try:
        return WordCloud(
            min_font_size=10,
            background_color="black",
            width=300,
            height=300,
            stopwords=set(STOPWORDS),
            font_path="./assets/Oswald-Bold.ttf",
        ).generate(text_for_analysis)
    except ValueError as error:
        return {"error": error.args[0]}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/sentiments", response_class=HTMLResponse)
async def sentiments(
    hx_request: Request,
    sentiment_polarities_per_sentence: List[float] = Depends(
        get_sentiment_polarities_per_sentence
    ),
):
    adjusted_sentiments = [
        (sentiment_polarity + 1) / 2
        for sentiment_polarity in sentiment_polarities_per_sentence
    ]

    return templates.TemplateResponse(
        "fragments/sentiment.html",
        {
            "request": hx_request,
            "sentiments": adjusted_sentiments,
        },
    )


@app.get("/wordcloud", response_class=HTMLResponse)
async def wordcloud(hx_request: Request, wordcloud: WordCloud = Depends(get_wordcloud)):
    if type(wordcloud) == dict and wordcloud.get("error") is not None:
        return templates.TemplateResponse(
            "fragments/wordcloud_error.html",
            {"request": hx_request, "error": wordcloud["error"]},
        )
    return HTMLResponse(wordcloud.to_svg())
