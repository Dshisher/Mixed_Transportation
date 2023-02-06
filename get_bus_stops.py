"""
This script downloads the bus stops data.

"""

import requests
#
import numpy as np
#
import functions_bus_stops as fs


def calculate_distance_from_point(df, dict_coordinates):
    """
    Calculate the distance between every coordinate in df the destination (in Km).
    Took from: https://stackoverflow.com/questions/365826/calculate-distance-between-2-gps-coordinates
    :param df:
    :param dict_coordinates:
    :return:
    """
    earth_radius = 6371

    dict_coordinates['lat_rad'] = dict_coordinates['lat'] * np.pi / 180
    dict_coordinates['lng_rad'] = dict_coordinates['lng'] * np.pi / 180

    df['dlat'] = df['Lat']  * np.pi / 180 - dict_coordinates['lat_rad']
    df['dlng'] = df['Long'] * np.pi / 180 - dict_coordinates['lng_rad']
    df['pre1'] = np.sin(df['dlat']/2) * np.sin(df['dlat']/2) + \
        np.sin(df['dlng'] / 2) * np.sin(df['dlng'] / 2) * \
        np.cos(dict_coordinates['lat_rad']) * np.cos(df['Lat'] * np.pi / 180 / 2)
    df['pre2'] = 2 * np.arctan2(np.sqrt(df['pre1']), 1 - np.sqrt(df['pre1']))

    df['distance'] = earth_radius * df['pre2']

    df.drop(columns=['dlat', 'dlng', 'pre1', 'pre2'], inplace=True)
    return df


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


def detect_drop_stations(df, walking_radius):
    """

    :return df: list of bus stations that are within walking distance.
    """

    df = df.loc[df['distance'] < walking_radius / 1000]
    return df


def detect_main_lines():
    """

    :return:
    """
    ...


def main(destination, walking_radius=500):
    """
    :param destination:
    :param walking_radius: max distance between closest but station to destination.
    :return:
    """

    # Read API key:
    with open('key_google_api.txt') as f:
        api_key = f.readlines()[0]

    destination_data = get_destination_coordinates(api_key, destination)['results'][0]

    # extracting lon and lat:
    destination_coordinates = destination_data['geometry']['location']
    df_bus_stations = fs.check_if_data_cache_exists()

    # calculate distance from bus station:
    df_bus_stations = calculate_distance_from_point(df_bus_stations, destination_coordinates)

    drop_stations = detect_drop_stations(df_bus_stations, walking_radius)
    print(df_bus_stations)


if __name__ == '__main__':
    destination_test = "Madatech+Haifa"
    main(destination_test)
