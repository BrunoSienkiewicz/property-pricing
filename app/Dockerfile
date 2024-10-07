FROM python:3.10-slim

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

COPY . /app
WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev python3-dev && \
    pip install poetry && \
    poetry install --no-dev --no-interaction --no-ansi && \
    apt-get remove -y gcc libpq-dev python3-dev && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* $POETRY_CACHE_DIR

EXPOSE 8080

CMD ["poetry", "run", "streamlit", "run", "streamlit_app.py", "--server.port", "8080"]

