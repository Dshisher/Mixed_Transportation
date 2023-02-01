"""
This script downloads the bus stops data.

"""

import requests
#
import pandas as pd


def download_data():
    """
    Download data from: https://data.gov.il/dataset/bus_stops/resource/e873e6a2-66c1-494f-a677-f5e77348edb0

    :return df: Dataframe containing the scrapped data.
    """

    path_to_data = 'https://data.gov.il/api/3/action/datastore_search?resource_id=e873e6a2-66c1-494f-a677-f5e77348edb0&limit=500'  # &limit=5
    data = requests.get(path_to_data)

    output_json = data.json()
    lines = output_json['result']['records']
    df = pd.DataFrame.from_records(lines)

    return df


if __name__ == '__main__':
    download_data()

