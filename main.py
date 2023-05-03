from database import Database, Listing
from sql_queries import custom_sql_get
from models import load_data_from_db_to_df, preprocessing_df, build_model_random_forest, fill_missing_columns
import mysql.connector
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

def main():
    # database = Database("localhost", "root", "mysql", "test", "warszawa", 2, 4)
    # database.scrape_listings()
    # database.format_listings()

    # database.insert_to_db()

    # df = load_data_from_db_to_df(1, 'localhost', 'root', 'mysql')
    # pass
    # df.to_csv('prediction.csv')
    df = pd.read_csv('data.csv')
    df = df.drop(['Unnamed: 0'], axis=1)
    df = df.dropna(subset=['Total Price'])

    features_to_ohe = ['City', 'Region', 'type of estate', 'MarketType', 'Building_type', 'Building_ownership', 'Building_material', 'Construction_status']
    features_to_drop = ['title', 'Estate_url', 'Date_added']
    feature_list_to_ohe = ['Equipment_types', 'Extras_types', 'Media_types', 'Security_types']

    predict_df = pd.read_csv('prediction.csv')
    predict_df = predict_df.drop(['Unnamed: 0'], axis=1)

    predict_df = preprocessing_df(predict_df, features_to_drop, features_to_ohe, feature_list_to_ohe)

    df = preprocessing_df(df, features_to_drop, features_to_ohe, feature_list_to_ohe)

    df, predict_df = fill_missing_columns(df, predict_df)
    
    model, mse = build_model_random_forest(df, 0.2, df.columns.values.tolist(), 'Total Price')
    print(np.sqrt(mse))

    price_pred = model.predict(predict_df)
    print(price_pred)


if __name__ == "__main__":
    main()