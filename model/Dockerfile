FROM python:3.10-slim as builder

WORKDIR /home/model-server

ARG ARTIFACTS_DIR
ARG FEAST_REPO_DIR
ARG CONFIG_PATH
ARG MODEL_NAME
ARG MODEL_VERSION

COPY $ARTIFACTS_DIR ./artifacts
COPY $FEAST_REPO_DIR ./feast
COPY $CONFIG_PATH ./config.json
COPY ./api.py .
COPY ./handler.py .
COPY ./utils.py .
COPY ./transform.py .
COPY ./poetry.lock .
COPY ./pyproject.toml .
COPY ./poetry.toml .

ENV MODEL_NAME=$MODEL_NAME
ENV MODEL_VERSION=$MODEL_VERSION
ENV FEAST_REPO_DIR=./feast
ENV ARTIFACTS_DIR=./artifacts
ENV CONFIG_PATH=./config.json

RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev python3-dev
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

EXPOSE 8081

CMD ["poetry", "run", "python", "api.py", "--port", "8081"]

