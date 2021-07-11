#!/usr/bin/env python3
"""
Module Docstring
"""
import requests

__author__ = "Josh Winton"
__version__ = "0.1.0"
__license__ = "MIT"

latitude = 40.6302887
longitude = -73.9029366


def getData(latitude, longitude):
    location = {'lat': latitude, 'lng': longitude}
    r = requests.get("https://api.sunrise-sunset.org/json", params=location)
    utc_sunrise = r.json()['results']['sunrise']
    utc_sunset = r.json()['results']['sunset']
    return (utc_sunrise, utc_sunset)


def main():
    """ Main entry point of the app """
    print(f"Sunrise Sunset Calendar v{__version__}")
    print("Location:")
    print(f"\tLatitude:\t{latitude}")
    print(f"\tLongitude:\t{longitude}")
    print("Getting data...")
    data = getData(latitude, longitude)
    print(f"\tUTC Sunrise:\t{data[0]}")
    print(f"\tUTC Sunset: \t{data[1]}")


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
