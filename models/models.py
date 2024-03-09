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


def preprocessing_df(df, features_to_drop, features_to_ohe, features_to_ohe_list):
    df = df.drop(features_to_drop, axis=1)
    for feature in features_to_ohe:
        df = ohe_feature(df, feature)
    for feature in features_to_ohe_list:
        df = ohe_list_feature(df, feature)
    df_columns = df.columns.values.tolist()
    for column in df_columns:
        if not df[column].isnull().values.any():
            continue
        df[column].replace(np.nan, df[column].median(), inplace=True)
    return df


def fill_missing_columns(df1, df2):
    for col in df1.columns:
        if col not in df2.columns:
            df2[col] = 0

    for col in df2.columns:
        if col not in df1.columns:
            df1[col] = 0

    cols = df1.columns.tolist()
    df2 = df2[cols]
    return df1, df2


class RandomForestModel:
    def __init__(self, train_data_source, train_test_ratio, target, chosen_features=None, random_state=45):
        self.model = RandomForestRegressor(random_state=random_state)
        self.train_data_source = train_data_source
        self.train_test_ratio = train_test_ratio
        self.target = target
        self.random_state = random_state

        self.train_data_df = pd.read_csv(self.train_data_source)
        self.train_data_df = self.train_data_df.drop(['Unnamed: 0'], axis=1)
        self.train_data_df = self.train_data_df.dropna(subset=[target])

        if chosen_features is None:
            self.chosen_features = self.train_data_df.columns.tolist()
            self.chosen_features.remove(target)

    def preprocess(self, features_to_drop, features_to_ohe, features_to_ohe_list):
        self.train_data_df = preprocessing_df(self.train_data_df, features_to_drop, features_to_ohe, features_to_ohe_list)

    def build_model(self):
        self.model, self.MSE = build_model_sk(self.train_data_df, self.model, self.train_test_ratio, self.chosen_features, self.target, self.random_state)
        
    def predict(self, data):
        self.train_data_df, data = fill_missing_columns(self.train_data_df, data)
        return self.model.predict(data)