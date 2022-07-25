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
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/sentiment", response_class=HTMLResponse)
async def sentiment(hx_request: Request, text_for_analysis: str):
    sentences = tokenize.sent_tokenize(text_for_analysis)

    return templates.TemplateResponse(
        "fragments/sentiment.html",
        {
            "request": hx_request,
            "sentiments": [TextBlob(sentence).sentiment for sentence in sentences],
        },
    )


@app.get("/wordcloud", response_class=HTMLResponse)
async def wordcloud(hx_request: Request, text_for_analysis: str):
    wordcloud = WordCloud(
        min_font_size=10,
        background_color="white",
        width=200,
        height=200,
        stopwords=set(STOPWORDS),
    ).generate(text_for_analysis)

    return HTMLResponse(wordcloud.to_svg())
