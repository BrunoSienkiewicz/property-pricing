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
            "model_metadata": [json.dumps(config)],
            "model_binary": [binary],
        }
    )

    if ohe_encoder:
        ohe_encoder_path = model_path / "ohe_encoder.pkl"
        joblib.dump(ohe_encoder, ohe_encoder_path)
        with open(ohe_encoder_path, "rb") as file:
            ohe_binary = file.read()
        df["model_ohe_encoder"] = [ohe_binary]
    if ordinal_encoder:
        ordinal_encoder_path = model_path / "ordinal_encoder.pkl"
        joblib.dump(ordinal_encoder, ordinal_encoder_path)
        with open(ordinal_encoder_path, "rb") as file:
            ordinal_binary = file.read()
        df["model_ordinal_encoder"] = [ordinal_binary]
    if scaler:
        scaler_path = model_path / "scaler.pkl"
        joblib.dump(scaler, scaler_path)
        with open(scaler_path, "rb") as file:
            scaler_binary = file.read()
        df["model_scaler"] = [scaler_binary]

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
    config = json.loads(df["model_metadata"].values[0])
    ohe_encoder = joblib.load(df["model_ohe_encoder"].values[0])
    ordinal_encoder = joblib.load(df["model_ordinal_encoder"].values[0])
    scaler = joblib.load(df["model_scaler"].values[0])

    return model, config, ohe_encoder, ordinal_encoder, scaler


def load_model_from_directory(
    model_directory: os.PathLike,
    device: torch.device = torch.device("cpu"),
):
    model_state_dict = torch.load(model_directory / "model.pth", map_location=device)

    ohe_encoder = (
        joblib.load(model_directory / "ohe_encoder.pkl")
        if (model_directory / "ohe_encoder.pkl").exists()
        else None
    )
    ordinal_encoder = (
        joblib.load(model_directory / "ordinal_encoder.pkl")
        if (model_directory / "ordinal_encoder.pkl").exists()
        else None
    )
    scaler = (
        joblib.load(model_directory / "scaler.pkl")
        if (model_directory / "scaler.pkl").exists()
        else None
    )

    return model_state_dict, ohe_encoder, ordinal_encoder, scaler
