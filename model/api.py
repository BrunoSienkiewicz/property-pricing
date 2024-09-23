import argparse
import os

from fastapi import FastAPI
from pydantic import BaseModel

from handler import InferenceHandler

app = FastAPI()


class InferenceRequest(BaseModel):
    inputs: dict


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict")
def predict(request: InferenceRequest):
    return InferenceHandler().predict(request.inputs)


if __name__ == "__main__":
    import uvicorn

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", default=8080)
    args = parser.parse_args()

    uvicorn.run(app, host=args.host, port=args.port)
