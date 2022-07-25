from nltk import tokenize
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount("/assets", StaticFiles(directory="./assets"), name="assets")

templates = Jinja2Templates(directory="./")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/sentiment", response_class=HTMLResponse)
async def sentiment(hx_request: Request, text_for_analysis: str):
    sentences = tokenize.sent_tokenize(text_for_analysis)
    adjusted_sentiments = [
        (TextBlob(sentence).sentiment.polarity + 1) / 2 for sentence in sentences
    ]

    return templates.TemplateResponse(
        "fragments/sentiment.html",
        {
            "request": hx_request,
            "sentiments": adjusted_sentiments,
        },
    )


@app.get("/wordcloud", response_class=HTMLResponse)
async def wordcloud(hx_request: Request, text_for_analysis: str):
    try:
        wordcloud = WordCloud(
            min_font_size=10,
            background_color="black",
            width=300,
            height=300,
            stopwords=set(STOPWORDS),
            font_path="./assets/Oswald-Bold.ttf",
        ).generate(text_for_analysis)
    except ValueError as error:
        return templates.TemplateResponse(
            "fragments/wordcloud_error.html",
            {"request": hx_request, "error": error.args[0]},
        )

    return HTMLResponse(wordcloud.to_svg())
