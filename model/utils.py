import json
import os
from pathlib import Path

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
    ohe_encoder: OneHotEncoder = None,
    ordinal_encoder: OrdinalEncoder = None,
    scaler: StandardScaler = None,
    model_directory: os.PathLike = Path(os.curdir) / "artifacts",
    connection_string: str = None,
):
    """
    Save model to disk and optionally to a database.
    """
    model_path = model_directory / f"{config['model_name']}_{config['model_version']}"
    if not os.path.exists(model_path):
        os.makedirs(model_path, exist_ok=True)

    torch.save(model.state_dict(), model_path / "model.pth")
    with open(model_path / "model.pth", "rb") as file:
        binary = file.read()

    df = pd.DataFrame(
        {
            "model_name": [config["model_name"]],
            "model_version": [config["model_version"]],
            "model_description": [config["model_description"]],
            "model_metadata": [json.dumps(config["model_metadata"])],
            "model_binary": [binary],
        }
    )

    if ohe_encoder:
        ohe_encoder_path = model_path / "ohe_encoder.pkl"
        joblib.dump(ohe_encoder, ohe_encoder_path)
        df["model_ohe_encoder"] = [joblib.load(ohe_encoder_path)]
    if ordinal_encoder:
        ordinal_encoder_path = model_path / "ordinal_encoder.pkl"
        joblib.dump(ordinal_encoder, ordinal_encoder_path)
        df["model_ordinal_encoder"] = [joblib.load(ordinal_encoder_path)]
    if scaler:
        scaler_path = model_path / "scaler.pkl"
        joblib.dump(scaler, scaler_path)
        df["model_scaler"] = [joblib.load(scaler_path)]

    if connection_string:
        df.to_sql(
            "models",
            connection_string,
            if_exists="append",
            index=False,
            schema="model_store",
        )


def load_model_from_db(
    model_name: str,
    model_version: str,
    connection_string: str,
    device: torch.device = torch.device("cpu"),
):
    df = pd.read_sql(
        f"SELECT * FROM model_store.models WHERE model_name='{model_name}' AND model_version='{model_version}'",
        connection_string,
    )

    model_state_dict = df["model_binary"].values[0]
    model = torch.load(model_state_dict, map_location=device)
    metadata = json.loads(df["model_metadata"].values[0])
    ohe_encoder = joblib.load(df["model_ohe_encoder"].values[0])
    ordinal_encoder = joblib.load(df["model_ordinal_encoder"].values[0])
    scaler = joblib.load(df["model_scaler"].values[0])

    return model, metadata, ohe_encoder, ordinal_encoder, scaler


def load_model_from_directory(
    model_directory: os.PathLike,
    device: torch.device = torch.device("cpu"),
):
    model_state_dict = torch.load(model_directory / "model.pth", map_location=device)
    ohe_encoder = joblib.load(model_directory / "ohe_encoder.pkl")
    ordinal_encoder = joblib.load(model_directory / "ordinal_encoder.pkl")
    scaler = joblib.load(model_directory / "scaler.pkl")

    return model_state_dict, ohe_encoder, ordinal_encoder, scaler
