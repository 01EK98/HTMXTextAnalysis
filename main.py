from typing import Dict, List, Optional
from nltk import tokenize
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount("/assets", StaticFiles(directory="./assets"), name="assets")

templates = Jinja2Templates(directory="./")


async def get_sentiment_polarity(text_for_analysis: Optional[str] = Form("")) -> float:
    return TextBlob(text_for_analysis).sentiment.polarity


async def get_sentiment_polarities_per_sentence(
    text_for_analysis: Optional[str] = Form(""),
) -> List[float]:
    sentences = tokenize.sent_tokenize(text_for_analysis)
    return [await get_sentiment_polarity(sentence) for sentence in sentences]


async def get_wordcloud(
    text_for_analysis: Optional[str] = Form(""),
) -> WordCloud | Dict[str, str]:
    try:
        return WordCloud(
            min_font_size=14,
            background_color="black",
            width=250,
            height=250,
            stopwords=set(STOPWORDS),
            font_path="./assets/Oswald-Bold.ttf",
        ).generate(text_for_analysis)
    except ValueError as error:
        return {"error": error.args[0]}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/sentiments", response_class=HTMLResponse)
async def sentiments(
    hx_request: Request,
    sentiment_polarities_per_sentence: List[float] = Depends(
        get_sentiment_polarities_per_sentence
    ),
    overall_sentiment_polarity: float = Depends(get_sentiment_polarity),
):
    adjusted_sentiments_per_sentence = [
        round(100 * (sentiment_polarity + 1) / 2, 2)
        for sentiment_polarity in sentiment_polarities_per_sentence
    ]

    adjusted_overall_sentiment_polarity = round(
        100 * (overall_sentiment_polarity + 1) / 2, 2
    )

    return templates.TemplateResponse(
        "partials/sentiments.html",
        {
            "request": hx_request,
            "sentiments": adjusted_sentiments_per_sentence,
            "overall_sentiment": adjusted_overall_sentiment_polarity,
        },
        headers={"HX-Trigger": "generatedSentiments"},  # trigger HTMX custom  event
    )


@app.post("/wordcloud", response_class=HTMLResponse)
async def wordcloud(hx_request: Request, wordcloud: WordCloud = Depends(get_wordcloud)):
    if type(wordcloud) is WordCloud:
        return HTMLResponse(
            wordcloud.to_svg(), headers={"HX-Trigger": "generatedWordcloud"}
        )

    return templates.TemplateResponse(
        "partials/wordcloud_error.html",
        {"request": hx_request, "error": wordcloud["error"]},
        headers={"HX-Trigger": "wordcloudError"},
    )
