import argparse
import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from handler import InferenceHandler

app = FastAPI()
inference_handler = InferenceHandler()


class InferenceRequest(BaseModel):
    city: str
    region: str
    floor: int
    rooms: int
    year_built: int
    area: int


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict")
def predict(request: InferenceRequest):
    try:
        response = inference_handler.predict(request.model_dump())
        return {"predictions": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


if __name__ == "__main__":
    import uvicorn

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", default=8080)
    args = parser.parse_args()

    uvicorn.run(app, host=args.host, port=int(args.port))
