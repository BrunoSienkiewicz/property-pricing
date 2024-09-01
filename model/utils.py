import os


def load_query(path: os.PathLike, **kwargs) -> str:
    with open(path, 'r') as file:
        query = file.read()
    return query.format(**kwargs)

