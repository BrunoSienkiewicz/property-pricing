import torch
import torch.utils.data
import torch.nn.functional as F
import pandas as pd
import numpy as np

from imblearn.over_sampling import SMOTE


def get_dummies(data: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    cat_values = data[columns]
    cat_values = pd.get_dummies(cat_values)
    data = data.drop(columns, axis=1)
    data = pd.concat([data, cat_values], axis=1)
    return data


def normalize(data: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    data[columns] = (data[columns] - data[columns].mean()) / data[columns].std()
    return data


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
