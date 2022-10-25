# JS-less Text Analysis App

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)

This app could be really useful when analyzing articles or publications and trying to \
assess the biases and sentiments contained in them. 

I thought I could find some technologies to do all the JavaScripty stuff \
without all the JavaScript for a challenge :P \
It utilizes htmx in order to load HTML partials without refreshing the page \
and not depend on JavaScript to achieve that effect. \
\_hyperscript is utilized when in need of some DOM manipulation and Web API usage :)

## Setup

Run the following from terminal:

```bash
python -m virtualenv venv
.\venv\Scripts\activate # source venv/bin/activate in bash

pip install -r requirements.txt
python nltk_resource_setup.py
```

## Run

```bash
uvicorn main:app
```

or if you wish to have hot reload (useful when in development)

```bash
uvicorn main:app --reload
```

## Run unit tests

```bash
pytest
```

with coverage:

```bash
pytest --cov=.
```

## Run functional tests

```bash
pytest .\tests\functional_tests\functional_tests.py # pytest tests/functional_tests/* in bash
```

### Powered by:

- FastAPI https://fastapi.tiangolo.com/
- htmx https://htmx.org/
- \_hyperscript https://hyperscript.org/
- Tailwind CSS https://tailwindcss.com/
- Flowbite https://flowbite.com/
