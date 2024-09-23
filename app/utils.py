import os

import pandas as pd
import redis


def load_query(path: os.PathLike, **kwargs) -> str:
    with open(path, "r") as file:
        query = file.read()
    return query.format(**kwargs)


def get_data(query: str) -> pd.DataFrame:
    redis_client = redis.Redis(
        host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT")
    )
    data = redis_client.get(query)

    if data:
        return pd.read_json(data)
    else:
        data = pd.read_sql(query, os.getenv("CONNECTION_STRING"))
        redis_client.set(query, data.to_json())
        return data
