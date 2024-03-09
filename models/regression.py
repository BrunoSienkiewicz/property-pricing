import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import Lasso, BayesianRidge, LassoLars, TweedieRegressor, Ridge, LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.pipeline import make_pipeline
from sklearn.datasets import fetch_openml, fetch_california_housing
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import json
from io import StringIO


def build_model(data, model, train_test_ratio, chosen_features, target, random_state=45):
    
    # dzielimy na train i test
    data_train, data_test = train_test_split(data, test_size=train_test_ratio, random_state=random_state)
    X_train, X_test = data_train[chosen_features], data_test[chosen_features]
    y_train, y_test = data_train[target], data_test[target]
    
    # cała regresja dzieje się tutaj
    model.fit(X_train, y_train)
    
    # przewidujemy wartość dla danych testowych
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    # liczymy MSE
    MSE_train = mean_squared_error(y_train, y_pred_train)
    MSE_test = mean_squared_error(y_test, y_pred_test)
    #print('MSE on training data:', MSE_train)
    #print('MSE on test data:', MSE_test)
    
    return model, MSE_test


def ordinal_encoder(data, features_to_encode, encoding):
    data_to_encode = data[features_to_encode]
    oe = OrdinalEncoder(categories=encoding)
    oe.fit(data_to_encode)
    ord_encoded = oe.transform(data_to_encode)
    data_to_encode = ord_encoded
    data[features_to_encode] = data_to_encode
    return data


def onehotencoder(data, features_to_encode):
    data_to_encode = data[features_to_encode]
    data_to_encode = pd.get_dummies(data_to_encode)
    data = data.drop(features_to_encode, axis=1)
    data = pd.concat([data, data_to_encode], axis=1)
    return data


def multiple_ohe(data, features_to_encode):
    for feature in features_to_encode:
        data_to_encode = encode_feature(data[feature], feature)
        data.drop(feature, axis=1, inplace=True)
        data = pd.concat([data, data_to_encode], axis=1)
    return data


def encode_feature(feature_col, feature):
    cat_dict = {}
    cat_list = []
    for index, values in feature_col.iteritems():
        values = values.split(', ')
        values.sort()
        cat_list.append(values)
        for v in values:
            cat_dict[v] = 0
    cols = list(cat_dict.keys())
    cols.sort()
    lst = []
    for values in cat_list:
        idx = 0
        formatted_values = []
        for c in cols:
            if len(values) == idx:
                idx-=1
            if values[idx] == c:
                formatted_values.append(1)
                idx+=1
            else:
                formatted_values.append(0)
        lst.append(formatted_values)
    encoded_data = pd.DataFrame(lst, columns=cols)
    return encoded_data


with open('listing_data.csv', 'r', encoding='utf-8') as file:
    csv_data = file.read()
data = pd.read_csv(StringIO(csv_data), sep=';')
original_data = data

oe_features = ['Room number']
oe_encoding = [['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX']]
ohe_features = ['type of estate', 'City', 'Region', 'Build_year', 'Building_material', 'Building_ownership', 'Building_type', 'Construction_status', 'Floor_no', 'Heating', 'MarketType']
multiple_ohe_features = ['Equipment_types', 'Extras_types', 'Media_types', 'Security_types']

data = ordinal_encoder(data, oe_features, oe_encoding)
data = onehotencoder(data, ohe_features)
data = multiple_ohe(data, multiple_ohe_features)

chosen_features = data.columns.values.tolist()
chosen_features.remove('title')
chosen_features.remove('Rent')
chosen_features.remove('Total Price')
chosen_features.remove('link')
target = ['Total Price']

model, MSE = build_model(data, RandomForestRegressor(), 0.2, chosen_features, target)

data_to_predict = data[chosen_features]
predictions = model.predict(data_to_predict)
predictions = pd.DataFrame(predictions, columns=['Total Price predicted'])
predicted_data = pd.concat([original_data, predictions], axis=1)
predicted_csv_data = pd.DataFrame.to_csv(predicted_data, sep=';')

print(f'Średnia pomyłka: {np.sqrt(MSE)}')
with open('predicted_data.csv', 'w', encoding="utf-8") as file:
    file.write(predicted_csv_data)

pass