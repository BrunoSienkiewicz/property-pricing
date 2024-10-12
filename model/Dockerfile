FROM python:3.10-slim as builder

WORKDIR /home/model-server

ARG FEAST_REPO_DIR

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

COPY $FEAST_REPO_DIR ./feast

COPY ./api.py ./handler.py ./model.py ./utils.py ./transform.py ./
COPY poetry.lock pyproject.toml poetry.toml ./

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev python3-dev && \
    pip install poetry

RUN poetry build && \
    pip install dist/*.whl

RUN apt-get remove -y gcc libpq-dev python3-dev && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* $POETRY_CACHE_DIR

FROM python:3.10-slim

WORKDIR /home/model-server

ENV VIRTUAL_ENV=/home/model-server/.venv \
    PATH=/home/model-server/.venv/bin:$PATH

COPY --from=builder /home/model-server /home/model-server

ARG MODEL_NAME
ARG MODEL_VERSION

ENV MODEL_NAME=$MODEL_NAME \
    MODEL_VERSION=$MODEL_VERSION \
    FEAST_REPO_DIR=./feast \

EXPOSE 8081

CMD ["python", "api.py", "--port", "8081"]

