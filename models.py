import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import mysql.connector
from sql_queries import get_all_property_info
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, MultiLabelBinarizer
import tensorflow as tf
from tensorflow import keras
from keras import layers


def build_model_sk(data, model, train_test_ratio, chosen_features, target, random_state=45):

    data_train, data_test = train_test_split(data, test_size=train_test_ratio, random_state=random_state)
    X_train, X_test = data_train[chosen_features], data_test[chosen_features]
    y_train, y_test = data_train[target], data_test[target]

    model.fit(X_train, y_train)
    
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    MSE_train = mean_squared_error(y_train, y_pred_train)
    MSE_test = mean_squared_error(y_test, y_pred_test)
    
    return model, [MSE_test, MSE_train]


def build_model_random_forest(data, train_test_ratio, chosen_features, target, random_state=45):
    model = RandomForestRegressor(random_state=random_state)
    return build_model_sk(data, model, train_test_ratio, chosen_features, target, random_state)


def load_data_from_db_to_df(amt, host, user, password):
    db = mysql.connector.connect(
        host = host,
        user = user,
        password = password,
        database = 'estate'
    )
    cursor = db.cursor(buffered=True)

    get_all_property_info(1, cursor)

    df = pd.DataFrame(columns=cursor.column_names)
    for i in range(1, amt+1):
        prop = get_all_property_info(i, cursor)
        prop = pd.Series(prop, index=df.columns)
        df = df.append(prop, ignore_index=True)

    return df


def ohe_feature(df, feature_name):
    encoder = OneHotEncoder()
    encoded_feature = encoder.fit_transform(df[[feature_name]])
    df_encoded = pd.concat([df.drop([feature_name], axis=1), pd.DataFrame(encoded_feature.toarray(), columns=encoder.get_feature_names_out([feature_name]))], axis=1)
    return df_encoded


def ohe_list_feature(df, feature):
    mlb = MultiLabelBinarizer()
    df[feature] = df[feature].apply(lambda x: 'none_' + feature if pd.isna(x) else x)
    df[feature] = df[feature].apply(lambda x: x.split(','))
    encoded_feature = mlb.fit_transform(df[feature])
    df_encoded = pd.concat([df.drop([feature], axis=1), pd.DataFrame(encoded_feature, columns=mlb.classes_)], axis=1)
    return df_encoded
