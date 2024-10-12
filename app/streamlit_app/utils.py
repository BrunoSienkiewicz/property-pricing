import hashlib
import json
import os
from functools import wraps

import pandas as pd
import redis
from psycopg2.pool import SimpleConnectionPool

redis_pool = redis.ConnectionPool(
    host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT")
)
pg_pool = SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    dsn=os.getenv("CONNECTION_STRING"),
)


def load_query(path: os.PathLike, **kwargs) -> str:
    with open(path, "r") as file:
        query = file.read()
    return query.format(**kwargs)


def redis_cache(ttl=60):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            redis_client = redis.Redis(connection_pool=redis_pool)
            key = f"{func.__name__}:{hashlib.sha256(str(args).encode()).hexdigest()}"

            cached_result = redis_client.get(key)
            if cached_result:
                return json.loads(cached_result)

            result = func(*args, **kwargs)
            redis_client.setex(key, ttl, json.dumps(result))
            return result

        return wrapper

    return decorator


def get_data(query: str) -> pd.DataFrame:
    conn = pg_pool.getconn()
    with conn.cursor() as cur:
        cur.execute(query)
        data = cur.fetchall()
    pg_pool.putconn(conn)
    return pd.DataFrame(data)
