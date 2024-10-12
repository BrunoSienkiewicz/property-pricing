from abc import ABC, abstractmethod
import os
import json
import pickle
import joblib
import boto3
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
    
from pathlib import Path
from utils import serialize_object, deserialize_object


class ArtifactsHandler(ABC):
    @staticmethod
    @abstractmethod
    def save_model(
        model,
        config: dict,
        uri: str,
        ohe_encoder: OneHotEncoder = OneHotEncoder(),
        ordinal_encoder: OrdinalEncoder = OrdinalEncoder(),
        scaler: StandardScaler = StandardScaler(),
    ) -> None:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def load_model(
        model_name: str,
        model_version: str,
        uri: str,
    ) -> tuple:
        raise NotImplementedError


class LocalArtifactsHandler(ArtifactsHandler):
    @staticmethod
    def save_model(
        model,
        config: dict,
        uri: str,
        ohe_encoder: OneHotEncoder = OneHotEncoder(),
        ordinal_encoder: OrdinalEncoder = OrdinalEncoder(),
        scaler: StandardScaler = StandardScaler(),
    ) -> None:
        model_path = Path(uri) / f"{config['model_name']}_{config['model_version']}"
        if not os.path.exists(model_path):
            os.makedirs(model_path, exist_ok=True)

        model_state_dict = serialize_object(model.state_dict())
        joblib.dump(model_state_dict, model_path / "model.pth")

        config_path = model_path / "config.json"
        config_path.write_text(json.dumps(config))

        if ohe_encoder:
            ohe_encoder_path = model_path / "ohe_encoder.pkl"
            joblib.dump(ohe_encoder, ohe_encoder_path)

        if ordinal_encoder:
            ordinal_encoder_path = model_path / "ordinal_encoder.pkl"
            joblib.dump(ordinal_encoder, ordinal_encoder_path)

        if scaler:
            scaler_path = model_path / "scaler.pkl"
            joblib.dump(scaler, scaler_path)

    @staticmethod
    def load_model(
        model_name: str,
        model_version: str,
        uri: str,
    ) -> tuple:
        model_path = Path(uri) / f"{model_name}_{model_version}"
        model_state_dict = joblib.load(model_path / "model.pth")

        config = json.loads((model_path / "config.json").read_text())

        ohe_encoder = (
            joblib.load(model_path / "ohe_encoder.pkl")
            if (model_path / "ohe_encoder.pkl").exists()
            else None
        )
        ordinal_encoder = (
            joblib.load(model_path / "ordinal_encoder.pkl")
            if (model_path / "ordinal_encoder.pkl").exists()
            else None
        )
        scaler = (
            joblib.load(model_path / "scaler.pkl")
            if (model_path / "scaler.pkl").exists()
            else None
        )

        return model_state_dict, config, ohe_encoder, ordinal_encoder, scaler


class DBArtifactsHandler(ArtifactsHandler):
    @staticmethod
    def save_model(
        model,
        config: dict,
        uri: str,
        ohe_encoder: OneHotEncoder = OneHotEncoder(),
        ordinal_encoder: OrdinalEncoder = OrdinalEncoder(),
        scaler: StandardScaler = StandardScaler(),
    ) -> None:
        model_state_dict = serialize_object(model.state_dict())
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

        df.to_sql("model_store.models", uri, if_exists="append", index=False)

    @staticmethod
    def load_model(
        model_name: str,
        model_version: str,
        uri: str,
    ) -> tuple:
        df = pd.read_sql(
            f"SELECT * FROM model_store.models WHERE model_name='{model_name}' AND model_version='{model_version}'",
            uri,
        )

        model_state_dict = deserialize_object(df["model_binary"].values[0])
        config = json.loads(df["model_metadata"].values[0])
        ohe_encoder = deserialize_object(df["model_ohe_encoder"].values[0])
        ordinal_encoder = deserialize_object(df["model_ordinal_encoder"].values[0])
        scaler = deserialize_object(df["model_scaler"].values[0])

        return model_state_dict, config, ohe_encoder, ordinal_encoder, scaler


class S3ArtifactsHandler(ArtifactsHandler):
    @staticmethod
    def save_model(
        model,
        config: dict,
        uri: str,
        ohe_encoder: OneHotEncoder = OneHotEncoder(),
        ordinal_encoder: OrdinalEncoder = OrdinalEncoder(),
        scaler: StandardScaler = StandardScaler(),
    ) -> None:
        s3 = boto3.client("s3")
        model_state_dict = pickle.dumps(model.state_dict())
        model_key = f"{config['model_name']}_{config['model_version']}/model.pth"
        s3.put_object(Bucket=uri, Key=model_key, Body=model_state_dict)

        if ohe_encoder:
            ohe_encoder_binary = pickle.dumps(ohe_encoder)
            ohe_encoder_key = f"{config['model_name']}_{config['model_version']}/ohe_encoder.pkl"
            s3.put_object(Bucket=uri, Key=ohe_encoder_key, Body=ohe_encoder_binary)

        if ordinal_encoder:
            ordinal_encoder_binary = pickle.dumps(ordinal_encoder)
            ordinal_encoder_key = f"{config['model_name']}_{config['model_version']}/ordinal_encoder.pkl"
            s3.put_object(Bucket=uri, Key=ordinal_encoder_key, Body=ordinal_encoder_binary)

        if scaler:
            scaler_binary = pickle.dumps(scaler)
            scaler_key = f"{config['model_name']}_{config['model_version']}/scaler.pkl"
            s3.put_object(Bucket=uri, Key=scaler_key, Body=scaler_binary)

    @staticmethod
    def load_model(
        model_name: str,
        model_version: str,
        uri: str,
    ) -> tuple:
        s3 = boto3.client("s3")
        model_key = f"{model_name}_{model_version}/model.pth"
        model_binary = s3.get_object(Bucket=uri, Key=model_key)["Body"].read()
        model_state_dict = pickle.loads(model_binary)

        config_key = f"{model_name}_{model_version}/config.json"
        config_binary = s3.get_object(Bucket=uri, Key=config_key)["Body"].read()
        config = json.loads(config_binary)

        ohe_encoder_key = f"{model_name}_{model_version}/ohe_encoder.pkl"
        ohe_encoder_binary = s3.get_object(Bucket=uri, Key=ohe_encoder_key)["Body"].read()
        ohe_encoder = pickle.loads(ohe_encoder_binary)

        ordinal_encoder_key = f"{model_name}_{model_version}/ordinal_encoder.pkl"
        ordinal_encoder_binary = s3.get_object(Bucket=uri, Key=ordinal_encoder_key)["Body"].read()
        ordinal_encoder = pickle.loads(ordinal_encoder_binary)

        scaler_key = f"{model_name}_{model_version}/scaler.pkl"
        scaler_binary = s3.get_object(Bucket=uri, Key=scaler_key)["Body"].read()
        scaler = pickle.loads(scaler_binary)

        return model_state_dict, config, ohe_encoder, ordinal_encoder, scaler


