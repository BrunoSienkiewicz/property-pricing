# database query and insert functions to database
import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(os.environ.get('DATABASE_URL'))
DBSession = sessionmaker(bind=engine)
session = DBSession()


def load_query(path: os.PathLike, **kwargs) -> str:
    with open(path, 'r') as file:
        query = file.read()
    return query.format(**kwargs)


def query_db(query: str, **kwargs) -> pd.DataFrame:
    query = query.format(**kwargs)
    return pd.read_sql(query, engine)

