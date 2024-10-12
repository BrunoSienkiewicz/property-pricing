import io
import json
import os

import joblib


def load_query(path: os.PathLike, **kwargs) -> str:
    with open(path, "r") as file:
        query = file.read()
    return query.format(**kwargs)


def load_config(path: os.PathLike) -> dict:
    with open(path, "r") as file:
        config = json.load(file)
    return config


def serialize_object(obj):
    """
    Serialize an object to bytes.
    """
    with io.BytesIO() as stream:
        joblib.dump(obj, stream)
        stream.seek(0)
        return stream.read()


def deserialize_object(binary):
    """
    Deserialize an object from bytes.
    """
    with io.BytesIO(binary) as stream:
        stream.seek(0)
        return joblib.load(stream)
