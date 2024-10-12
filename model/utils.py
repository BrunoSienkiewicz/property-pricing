import io
import json
import os
import pickle
from pathlib import Path

import joblib
import boto3
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler


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


def save_model_to_dir(
    model,
    config: dict,
    ohe_encoder: OneHotEncoder = OneHotEncoder(),
    ordinal_encoder: OrdinalEncoder = OrdinalEncoder(),
    scaler: StandardScaler = StandardScaler(),
    model_directory: os.PathLike = Path(os.curdir) / "artifacts",
):
    model_path = model_directory / f"{config['model_name']}_{config['model_version']}"
    if not os.path.exists(model_path):
        os.makedirs(model_path, exist_ok=True)

    torch.save(model.state_dict(), model_path / "model.pth")

    if ohe_encoder:
        ohe_encoder_path = model_path / "ohe_encoder.pkl"
        joblib.dump(ohe_encoder, ohe_encoder_path)

    if ordinal_encoder:
        ordinal_encoder_path = model_path / "ordinal_encoder.pkl"
        joblib.dump(ordinal_encoder, ordinal_encoder_path)

    if scaler:
        scaler_path = model_path / "scaler.pkl"
        joblib.dump(scaler, scaler_path)


def save_model_to_db(
    model,
    config: dict,
    connection_string: str,
    ohe_encoder: OneHotEncoder = OneHotEncoder(),
    ordinal_encoder: OrdinalEncoder = OrdinalEncoder(),
    scaler: StandardScaler = StandardScaler(),
):
    model_state_dict = torch.save(model.state_dict(), io.BytesIO())
    df = pd.DataFrame(
        {
            "model_name": [config["model_name"]],
            "model_version": [config["model_version"]],
            "model_description": [config["model_description"]],
            "model_metadata": [json.dumps(config)],
            "model_binary": [model_state_dict],
        }
    )

    if ohe_encoder:
        ohe_encoder_binary = serialize_object(ohe_encoder)
        df["model_ohe_encoder"] = [ohe_encoder_binary]
    if ordinal_encoder:
        ordinal_encoder_binary = serialize_object(ordinal_encoder)
        df["model_ordinal_encoder"] = [ordinal_encoder_binary]
    if scaler:
        scaler_binary = serialize_object(scaler)
        df["model_scaler"] = [scaler_binary]

    df.to_sql("model_store.models", connection_string, if_exists="append", index=False)


def save_model_to_s3(
        model,
        config: dict,
        bucket: str,
        ohe_encoder: OneHotEncoder = OneHotEncoder(),
        ordinal_encoder: OrdinalEncoder = OrdinalEncoder(),
        scaler: StandardScaler = StandardScaler(),
        ):
    s3 = boto3.client("s3")
    model_state_dict = pickle.dumps(model.state_dict())
    model_key = f"{config['model_name']}_{config['model_version']}/model.pth"
    s3.put_object(Bucket=bucket, Key=model_key, Body=model_state_dict)

    if ohe_encoder:
        ohe_encoder_binary = pickle.dumps(ohe_encoder)
        ohe_encoder_key = f"{config['model_name']}_{config['model_version']}/ohe_encoder.pkl"
        s3.put_object(Bucket=bucket, Key=ohe_encoder_key, Body=ohe_encoder_binary)

    if ordinal_encoder:
        ordinal_encoder_binary = pickle.dumps(ordinal_encoder)
        ordinal_encoder_key = f"{config['model_name']}_{config['model_version']}/ordinal_encoder.pkl"
        s3.put_object(Bucket=bucket, Key=ordinal_encoder_key, Body=ordinal_encoder_binary)

    if scaler:
        scaler_binary = pickle.dumps(scaler)
        scaler_key = f"{config['model_name']}_{config['model_version']}/scaler.pkl"
        s3.put_object(Bucket=bucket, Key=scaler_key, Body=scaler_binary)


def load_model_from_db(
    model_name: str,
    model_version: str,
    connection_string: str,
):
    df = pd.read_sql(
        f"SELECT * FROM model_store.models WHERE model_name='{model_name}' AND model_version='{model_version}'",
        connection_string,
    )

    model_state_dict = deserialize_object(df["model_binary"].values[0])
    config = json.loads(df["model_metadata"].values[0])
    ohe_encoder = deserialize_object(df["model_ohe_encoder"].values[0])
    ordinal_encoder = deserialize_object(df["model_ordinal_encoder"].values[0])
    scaler = deserialize_object(df["model_scaler"].values[0])

    return model_state_dict, config, ohe_encoder, ordinal_encoder, scaler


def load_model_from_dir(
    model_directory: os.PathLike,
):
    model_state_dict = joblib.load(model_directory / "model.pth")

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


def load_model_from_s3(
        model_name: str,
        model_version: str,
        bucket: str,
        ):
    s3 = boto3.client("s3")
    model_key = f"{model_name}_{model_version}/model.pth"
    model_binary = s3.get_object(Bucket=bucket, Key=model_key)["Body"].read()
    model_state_dict = pickle.loads(model_binary)

    ohe_encoder_key = f"{model_name}_{model_version}/ohe_encoder.pkl"
    ohe_encoder_binary = s3.get_object(Bucket=bucket, Key=ohe_encoder_key)["Body"].read()
    ohe_encoder = pickle.loads(ohe_encoder_binary)

    ordinal_encoder_key = f"{model_name}_{model_version}/ordinal_encoder.pkl"
    ordinal_encoder_binary = s3.get_object(Bucket=bucket, Key=ordinal_encoder_key)["Body"].read()
    ordinal_encoder = pickle.loads(ordinal_encoder_binary)

    scaler_key = f"{model_name}_{model_version}/scaler.pkl"
    scaler_binary = s3.get_object(Bucket=bucket, Key=scaler_key)["Body"].read()
    scaler = pickle.loads(scaler_binary)

    return model_state_dict, ohe_encoder, ordinal_encoder, scaler

