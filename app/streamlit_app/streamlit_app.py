import os
from collections import OrderedDict

import requests
import streamlit as st

from utils import get_data, load_query, redis_cache

MODEL_NAME = os.getenv("MODEL_NAME")
PREDICT_URL = os.getenv("PREDICT_URL")
CITIES_QUERY = load_query("queries/get_cities.sql")

st.set_page_config(layout="wide")

st.title("House Price Prediction")


@redis_cache(ttl=60)
def get_cities():
    return get_data(CITIES_QUERY)[0].tolist()


@redis_cache(ttl=60)
def get_regions(city):
    regions_query = load_query("queries/get_regions.sql", city=city)
    return get_data(regions_query)[0].tolist()


def get_predict_request():
    city = st.sidebar.selectbox("City", get_cities())
    region = st.sidebar.selectbox("Region", get_regions(city))
    floor = st.sidebar.number_input("Floor", min_value=1, max_value=100, value=1)
    rooms = st.sidebar.number_input("Rooms", min_value=1, max_value=100, value=1)
    year_built = st.sidebar.number_input(
        "Year Built", min_value=1900, max_value=2024, value=2024
    )
    area = st.sidebar.number_input(
        "Area (square meters)", min_value=1, max_value=10000, value=1
    )
    return {
        "city": city,
        "region": region,
        "floor": floor,
        "rooms": rooms,
        "year_built": year_built,
        "area": area,
    }


request_data = get_predict_request()


@redis_cache(ttl=60)
def predict(request_data=request_data):
    response = requests.post(PREDICT_URL, json=request_data)
    return response.json()


st.sidebar.button("Predict", on_click=predict)
st.write("### Prediction:")
try:
    prediction = predict()
    st.write(prediction["prediction"])
except requests.exceptions.HTTPError as e:
    st.error(f"An error occurred: {e}")
