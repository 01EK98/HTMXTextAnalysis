# JS-less Text Analysis App

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)

This app could be really useful when analyzing articles \
or publications and trying to assess the biases \
and sentiments contained in them.

The app utilizes htmx in order to have reactivity \
within the app, but not have to use JavaScript to achieve it. \
Hyperscript is utilized when in need of some DOM manipulation :)

## Setup

### Linux:

Run the following from terminal:

```bash
source setup.sh
```

### Windows:

Run the following from terminal:

```bash
python -m virtualenv venv
.\venv\Scripts\activate

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

## Run tests

```bash
pytest
```

with coverage:

```bash
pytest --cov=.
```

### Powered by:

- FastAPI https://fastapi.tiangolo.com/
- htmx https://htmx.org/
- \_hyperscript https://hyperscript.org/
- Tailwind CSS https://tailwindcss.com/
- Flowbite https://flowbite.com/
