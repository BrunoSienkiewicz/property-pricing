import os
from pathlib import Path

import pandas as pd
import torch
from feast import FeatureStore

from transform import get_ohe_encoding, get_ordinal_encoding, normalize
from utils import load_config, load_model_from_directory


class InferenceHandler:
    def __init__(self):
        super(InferenceHandler, self).__init__()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.fs = FeatureStore(repo_path=os.getenv("FEAST_REPO_DIR"))
        self.config = load_config(os.getenv("CONFIG_PATH"))
        model, ohe_encoder, ordinal_encoder, scaler = load_model_from_directory(
            Path(os.getenv("ARTIFACTS_DIR")),
            device=self.device,
        )
        self.model = model
        self.ohe_encoder = ohe_encoder
        self.ordinal_encoder = ordinal_encoder
        self.scaler = scaler

    def preprocess(self, request: dict) -> torch.Tensor:
        # TODO: Add online features
        # feature_vector = self.fs.get_online_features(
        #     features=self.config["model_metadata"]["features"],
        #     entity_rows=data,
        # ).to_dict()
        df = pd.DataFrame.from_records(request)
        df, _ = get_ohe_encoding(df, self.config["ohe_features"], self.ohe_encoder)
        df, _ = get_ordinal_encoding(
            df, self.config["ordinal_features"], self.ordinal_encoder
        )
        df, _ = normalize(df, self.config["numerical_features"], self.scaler)
        return torch.tensor(df.values).float().to(self.device)

    def postprocess(self, data: torch.Tensor) -> list[dict]:
        return [{"prediction": int(p)} for p in data]

    def predict(self, request: dict) -> list[dict]:
        data = self.preprocess(request)
        prediction = self.model(data)
        return self.postprocess(prediction)
