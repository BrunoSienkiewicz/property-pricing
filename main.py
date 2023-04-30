from database import Database, Listing
from sql_queries import custom_sql_get
from models import load_data_from_db_to_df, ohe_feature
import mysql.connector

def main():
    # database = Database("localhost", "root", "mysql", "test", "warszawa", 2, 4)
    # database.scrape_listings()
    # database.format_listings()

    # database.insert_to_db()

    df = load_data_from_db_to_df(50, 'localhost', 'root', 'mysql')
    pass
    df.to_csv('data.csv')

if __name__ == "__main__":
    main()