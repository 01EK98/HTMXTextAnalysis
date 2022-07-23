import asyncio
from re import template
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from nltk.sentiment import SentimentIntensityAnalyzer


app = FastAPI()

app.mount("/assets", StaticFiles(directory="./assets"), name="assets")

templates = Jinja2Templates(directory="./")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/individual_sentiment", response_class=HTMLResponse)
async def individual_sentiment(request: Request, sentence: str):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(sentence)
    return templates.TemplateResponse(
        "fragments/individual_sentiment.html",
        {"request": request, "sentiment": sentiment},
    )
