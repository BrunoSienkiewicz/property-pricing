from database import Database, Listing
from sql_queries import custom_sql_get
from models import load_data_from_db_to_df, ohe_feature, ohe_list_feature, build_model_random_forest
import mysql.connector
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def main():
    # database = Database("localhost", "root", "mysql", "test", "warszawa", 2, 4)
    # database.scrape_listings()
    # database.format_listings()

    # database.insert_to_db()

    df = load_data_from_db_to_df(1, 'localhost', 'root', 'mysql')
    pass
    df.to_csv('prediction.csv')
    # df = pd.read_csv('data.csv')
    # df = df.drop(['Unnamed: 0'], axis=1)
    # df = df.dropna(subset=['Total Price'])

    # features_to_ohe = ['City', 'Region', 'type of estate', 'MarketType', 'Building_type', 'Building_ownership', 'Building_material', 'Construction_status']
    # df = df.drop(['title', 'Estate_url', 'Date_added'], axis=1)
    # feature_list_to_ohe = ['Equipment_types', 'Extras_types', 'Media_types', 'Security_types']

    # for feature in features_to_ohe:
    #     df = ohe_feature(df, feature)

    # for feature in feature_list_to_ohe:
    #     df = ohe_list_feature(df, feature)
    
    # print(df.columns)
    # model, mse = build_model_random_forest(df, 0.2, df.columns, 'Total Price')
    # print(mse)
    # pass

if __name__ == "__main__":
    main()