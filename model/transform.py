import numpy as np
import pandas as pd
import torch.nn.functional as F
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler


def get_ohe_encoding(
    data: pd.DataFrame, ohe_columns: list[str], ohe_encoder: OneHotEncoder = None
) -> tuple[pd.DataFrame, OneHotEncoder]:
    ohe_values = data[ohe_columns]
    if ohe_encoder is None:
        ohe_encoder = OneHotEncoder()
        ohe_encoder.fit(ohe_values)
    data_encoded = pd.DataFrame(
        ohe_encoder.transform(ohe_values).toarray(),
        columns=ohe_encoder.get_feature_names_out(ohe_columns),
        index=data.index,
    )
    data = pd.concat([data.drop(ohe_columns, axis=1), data_encoded], axis=1)
    return data, ohe_encoder


def get_ordinal_encoding(
    data: pd.DataFrame,
    ordinal_columns: list[str],
    ordinal_encoder: OrdinalEncoder = None,
) -> tuple[pd.DataFrame, OrdinalEncoder]:
    ordinal_values = data[ordinal_columns]
    if ordinal_encoder is None:
        ordinal_encoder = OrdinalEncoder()
        ordinal_encoder.fit(ordinal_values)
    data_encoded = pd.DataFrame(
        ordinal_encoder.transform(ordinal_values),
        index=data.index,
    )
    data = pd.concat([data.drop(ordinal_columns, axis=1), data_encoded], axis=1)
    return data, ordinal_encoder


def normalize(
    data: pd.DataFrame, columns: list[str], scaler: StandardScaler = None
) -> tuple[pd.DataFrame, StandardScaler]:
    if scaler is None:
        scaler = StandardScaler()
        scaler.fit(data[columns])
    data_scaled = pd.DataFrame(
        scaler.transform(data[columns]),
        columns=columns,
        index=data.index,
    )
    data = pd.concat([data.drop(columns, axis=1), data_scaled], axis=1)
    return data, scaler


def equalize_classes(data: pd.DataFrame, target: str) -> pd.DataFrame:
    smote = SMOTE()
    x = data.drop(target, axis=1)
    y = data[target]
    x_smote, y_smote = smote.fit_resample(x, y)
    data = pd.concat([x_smote, y_smote], axis=1)
    return data


def remove_corr_features(data: pd.DataFrame, target: str, threshold=0.9):
    corr_matrix = data.corr().abs()
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    to_drop = [column for column in upper.columns if any(upper[column] > threshold)]
    if target in to_drop:
        to_drop.remove(target)
    data = data.drop(to_drop, axis=1)
    return data
