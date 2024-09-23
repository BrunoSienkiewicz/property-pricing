import os
from collections import OrderedDict

import requests
import streamlit as st

from utils import get_data, load_query

MODEL_NAME = os.getenv("MODEL_NAME")
PREDICT_URL = f"http://model:8081/predict"
CITIES_QUERY = load_query("queries/get_cities.sql")

st.set_page_config(layout="wide")

st.title("House Price Prediction")


def get_predict_request():
    city = st.sidebar.selectbox("City", get_data(CITIES_QUERY))
    regions_query = load_query("queries/get_regions.sql", city=city)
    region = st.sidebar.selectbox("Region", get_data(regions_query))
    floor = st.sidebar.number_input("Floor", min_value=1, max_value=100, value=1)
    rooms = st.sidebar.number_input("Rooms", min_value=1, max_value=100, value=1)
    year_built = st.sidebar.number_input(
        "Year Built", min_value=1900, max_value=2024, value=2024
    )
    area = st.sidebar.number_input(
        "Area (square meters)", min_value=1, max_value=10000, value=1
    )
    return OrderedDict(
        {
            "city": [city],
            "region": [region],
            "floor": [floor],
            "rooms": [rooms],
            "year_built": [year_built],
            "area": [area],
        }
    )


request_data = get_predict_request()
response = requests.post(PREDICT_URL, json={"inputs": request_data})

st.write(response.json())
