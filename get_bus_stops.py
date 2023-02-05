"""
This script downloads the bus stops data.

"""

import requests
#
import functions_bus_stops as fs


def get_destination_coordinates(api_key, destination):
    """

    :param api_key:
    :param destination:
    :return destination_data: dictionary with destination data.
    """
    places_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={destination}&key={api_key}"
    destination_response = requests.get(places_url)
    destination_data     = destination_response.json()
    return destination_data


def main(destination, walking_radius=500):
    """
    :param destination:
    :param walking_radius: max distance between closest but station to destination.
    :return:
    """

    # Read API key:
    with open('key_google_api.txt') as f:
        api_key = f.readlines()[0]

    get_destination_coordinates(api_key, destination)

    df_bus_stations = fs.check_if_data_cache_exists()
    # df_bus_stations['distance'] =


if __name__ == '__main__':
    destination_test = "qiryat+shemona"
    main(destination_test)
