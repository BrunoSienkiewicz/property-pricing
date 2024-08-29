import torch
import torch.utils.data
import torch.nn.functional as F
import pandas as pd
import numpy as np

from imblearn.over_sampling import SMOTE


def get_dummies(data, columns):
    cat_values = data[columns]
    cat_values = pd.get_dummies(cat_values)
    data = data.drop(columns, axis=1)
    data = pd.concat([data, cat_values], axis=1)
    return data


def equalize_classes(df, target):
    smote = SMOTE()
    x = df.drop(target, axis=1)
    y = df[target]
    x_smote, y_smote = smote.fit_resample(x, y)
    df = pd.concat([x_smote, y_smote], axis=1)
    return df


def remove_corr_features(data, target, threshold=0.9):
    corr_matrix = data.corr().abs()
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    to_drop = [column for column in upper.columns if any(upper[column] > threshold)]
    if target in to_drop:
        to_drop.remove(target)
    data = data.drop(to_drop, axis=1)
    return data
