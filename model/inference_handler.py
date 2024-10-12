import os

import pandas as pd
import torch
from feast import FeatureStore

from model import CustomNet
from transform import get_ohe_encoding, get_ordinal_encoding, normalize
from artifacts_handler import DBArtifactHandler


class InferenceHandler:
    def __init__(self):
        super(InferenceHandler, self).__init__()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.fs = FeatureStore(repo_path=os.getenv("FEAST_REPO_DIR"))
        model_state_dict, config, ohe_encoder, ordinal_encoder, scaler = (
            DBArtifactHandler.load_model(
                model_name=os.getenv("MODEL_NAME"),
                model_version=os.getenv("MODEL_VERSION"),
                uri=os.getenv("DB_CONNECTION_STRING"),
            )
        )
        self.config = config
        self.model = CustomNet(**self.config["model_metadata"]["model_params"]).to(
            self.device
        )
        self.model.eval()
        self.model.load_state_dict(model_state_dict, map_location=self.device)
        self.ohe_encoder = ohe_encoder
        self.ordinal_encoder = ordinal_encoder
        self.scaler = scaler

    def preprocess(self, request: dict) -> torch.Tensor:
        # TODO: Add online features
        # feature_vector = self.fs.get_online_features(
        #     features=self.config["model_metadata"]["features"],
        #     entity_rows=data,
        # ).to_dict()
        df = pd.DataFrame([request])
        df, _ = get_ohe_encoding(
            df, self.config["model_metadata"]["ohe_features"], self.ohe_encoder
        )
        df, _ = get_ordinal_encoding(
            df, self.config["model_metadata"]["ordinal_features"], self.ordinal_encoder
        )
        df, _ = normalize(
            df, self.config["model_metadata"]["numerical_features"], self.scaler
        )
        return torch.tensor(df.values).float().to(self.device)

    def postprocess(self, data: torch.Tensor) -> int:
        return int(data.item())

    def predict(self, request: dict) -> list[dict]:
        data = self.preprocess(request)
        prediction = self.model(data)
        return self.postprocess(prediction)
