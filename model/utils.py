import json
import os

import joblib
import pandas as pd
import torch
import torch.nn as nn
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler


def load_query(path: os.PathLike, **kwargs) -> str:
    with open(path, "r") as file:
        query = file.read()
    return query.format(**kwargs)


def load_config(path: os.PathLike) -> dict:
    with open(path, "r") as file:
        config = json.load(file)
    return config


def save_model(
    model: nn.Module,
    config: dict,
    connection_string: str,
    ohe_encoder: OneHotEncoder = None,
    ordinal_encoder: OrdinalEncoder = None,
    scaler: StandardScaler = None,
):
    torch.save(
        model.state_dict(), f"{config['model_name']}_{config['model_version']}.pth"
    )
    with open(f"{config['model_name']}_{config['model_version']}.json", "w") as file:
        binary = file.read()
    if ohe_encoder:
        ohe_encoder_path = (
            f"{config['model_name']}_{config['model_version']}_ohe_encoder.pkl"
        )
        joblib.dump(ohe_encoder, ohe_encoder_path)
    if ordinal_encoder:
        ordinal_encoder_path = (
            f"{config['model_name']}_{config['model_version']}_ordinal_encoder.pkl"
        )
        joblib.dump(ordinal_encoder, ordinal_encoder_path)
    if scaler:
        scaler_path = f"{config['model_name']}_{config['model_version']}_scaler.pkl"
        joblib.dump(scaler, scaler_path)

    df = pd.DataFrame(
        {
            "model_name": [config["model_name"]],
            "model_version": [config["model_version"]],
            "model_description": [config["model_description"]],
            "model_metadata": [json.dumps(config["model_metadata"])],
            "model_binary": [binary],
            "model_ohe_encoder": [ohe_encoder],
            "model_ordinal_encoder": [ordinal_encoder],
            "model_scaler": [scaler],
        }
    )
    df.to_sql(
        "models",
        connection_string,
        if_exists="append",
        index=False,
        schema="model_store",
    )
