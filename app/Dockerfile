FROM python:3.10-slim

COPY . /app
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev python3-dev
RUN pip install poetry
RUN poetry config virtualenvs.create false

RUN poetry install --no-dev

EXPOSE 8080

CMD ["poetry", "run", "streamlit", "run", "streamlit_app.py", "--server.port", "8080"]

