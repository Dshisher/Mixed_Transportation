"""
This file contains function for the data extracted from: https://data.gov.il/dataset/bus_stops/resource/e873e6a2-66c1-494f-a677-f5e77348edb0.

"""

# imports:
import os
import requests
#
import pandas as pd


def download_data(num_limit=500):
    """
    Download data from: https://data.gov.il/dataset/bus_stops/resource/e873e6a2-66c1-494f-a677-f5e77348edb0

    :param num_limit: Number of data values to fetch from the website.
    :return df: Dataframe containing the scrapped data.
    """

    if num_limit == 0:
        path_to_data = 'https://data.gov.il/api/3/action/datastore_search?resource_id=e873e6a2-66c1-494f-a677-f5e77348edb0'
    else:
        path_to_data = f'https://data.gov.il/api/3/action/datastore_search?resource_id=e873e6a2-66c1-494f-a677-f5e77348edb0&limit={num_limit}'  # &limit=5

    data = requests.get(path_to_data)

    output_json = data.json()
    lines = output_json['result']['records']
    df = pd.DataFrame.from_records(lines)

    return df


def check_if_data_cache_exists(num_limit=0, force_re_downloading=False):
    """
    If data already exists locally then read local file.

    :param num_limit: Number of data values to fetch from the website.
    :param force_re_downloading:
    :return Dataframe containing the scrapped data:
    """
    if not force_re_downloading and "bus_stations.csv" in os.listdir():
        df_bus_stations = pd.read_csv("bus_stations.csv")
    else:
        df_bus_stations = download_data()
        df_bus_stations.to_csv("bus_stations.csv")

    return df_bus_stations
