#!/usr/bin/env python3
"""
Used for creating a calendar file with sunrise and sunset times.

This script fetches sunrise and sunset data from the API here: 
 https://api.sunrise-sunset.org/json. It then uses that data to create an
 iCal file that displays the time of sunrise and sunset everyday.
"""
import requests
from datetime import datetime
from dateutil import tz

__author__ = "Josh Winton"
__version__ = "0.1.0"
__license__ = "MIT"

# Constants for making API request
latitude = 40.6302887
longitude = -73.9029366


def getSunriseSunsetData(latitude: str, longitude: str):
    """Fetches data from sunrise-sunset API."""
    # Send request to API for lat and long unformatted
    r = requests.get("https://api.sunrise-sunset.org/json", params={'lat': latitude, 'lng': longitude, 'formatted': 0})
    # Extract sunrise and sunset from result
    utc_sunrise = r.json()['results']['sunrise']
    utc_sunset = r.json()['results']['sunset']

    return (utc_sunrise, utc_sunset)


def convertToLocal(time: str):
    """Converts an ISO format UTC time to a local time."""
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/New_York')
    utc = datetime.fromisoformat(time)
    utc = utc.replace(tzinfo=from_zone)
    local = utc.astimezone(to_zone).strftime("%X")
    return(local)


def main():
    """ Main entry point of the app """
    print(f"Sunrise Sunset Calendar v{__version__}")
    # TODO: Take zip code as a command line argument and look up lat long
    print("Location:")
    print(f"\tLatitude:\t{latitude}")
    print(f"\tLongitude:\t{longitude}")

    print("Getting data...")
    sunrise, sunset = getSunriseSunsetData(latitude, longitude)
    local_sunrise = convertToLocal(sunrise)
    local_sunset = convertToLocal(sunset)
    print(f"\tLocal Sunrise:\t{local_sunrise}")
    print(f"\tLocal Sunset: \t{local_sunset}")


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
