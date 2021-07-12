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
from ics import Calendar, Event
import time
import progressbar

__author__ = "Josh Winton"
__version__ = "0.1.0"
__license__ = "MIT"

# Constants for making API request
LATITUDE = 40.6302887
LONGITUDE = -73.9029366
DAYS_AHEAD = 10
# TIME_ZONE = 'America/New_York'
WRITE_FILE = 'sunrise-sunset.ics'


def getSunriseSunsetDataZip(zip: str, daysFromNow: int):
    return 0
    """"""
    # Convert zip to lat long
    # Convert zip to time zone
    # Call lat long function

def getSunriseSunsetDataLatLong(latitude: str, longitude: str, daysFromNow: int = 0):
    """Fetches data from sunrise-sunset API.
    
    Args:
        latitude: Latitude in degrees.

        longitude: Longitude in degrees.

        daysFromNow: Specify fetching data for a date N days in the future. 

    Returns:
        Tuple containing sunrise and sunset in ISO format
    """
    # Send request to API for lat and long unformatted, daysFromNow days into the future
    r = requests.get("https://api.sunrise-sunset.org/json", params={'lat': latitude, 'lng': longitude, 'formatted': 0, 'date': f"{daysFromNow} days"})
    
    # Extract sunrise and sunset from result
    utc_sunrise = r.json()['results']['sunrise']
    utc_sunset = r.json()['results']['sunset']

    return (utc_sunrise, utc_sunset)


def convertTimeToLocal(time: str):
    """Converts an ISO format UTC time to a local time.
    
    Args:
        time: UTC time to be converted in ISO format.
        
    Returns:
        The time in local time based on PSIX TZ variable.
    """
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz()
    utc = datetime.fromisoformat(time)
    utc = utc.replace(tzinfo=from_zone)
    local = utc.astimezone(to_zone)
    return local

def createCalendarEvent(calendar, sunrise: str, sunset: str):
    """Generates and adds a sunrise and sunset event to `calendar`.
    
    Args:
        calendar: ICS Calendar object.
        
        sunrise: ISO format sunrise time.

        sunset: ISO format sunset time.
    """
    sunrise_event = Event()
    sunrise_event.name = f"☀️ {sunrise.strftime('%I')}:{sunrise.strftime('%M')}"
    sunrise_event.begin = sunrise
    calendar.events.add(sunrise_event)

    sunset_event = Event()
    sunset_event.name = f"🌙 {sunset.strftime('%I')}:{sunset.strftime('%M')}"
    sunset_event.begin = sunset
    calendar.events.add(sunset_event)

def generateCalendarFile(latitude: str, longitude: str, filename: str, daysAhead: int = 30):
    """Fetches data and writes it to a .ics file.

    Args:
        latitude: Latitude in degrees.

        longitude: Longitude in degrees.

        filename: .ics filename to write calendar to.

        daysAhead: How many day into the future to generate the calendar.
    """
    calendar = Calendar() 

    for i in progressbar.progressbar(range(daysAhead)):
        time.sleep(1) # Wait between requests to avoid API usage limit
        utc_sunrise, utc_sunset = getSunriseSunsetDataLatLong(latitude, longitude, i)
        local_sunrise = convertTimeToLocal(utc_sunrise)
        local_sunset = convertTimeToLocal(utc_sunset)
        createCalendarEvent(calendar, local_sunrise, local_sunset) 

    with open(filename, 'w') as f:
        f.write(str(calendar))



def main():
    """ Main entry point of the app """
    print(f"Sunrise Sunset Calendar v{__version__}\n")
    # TODO: Take zip code as a command line argument and look up lat long
    print("Location:")
    print(f"\tLatitude:\t{LATITUDE}")
    print(f"\tLongitude:\t{LONGITUDE}")

    print("Getting data...")
    generateCalendarFile(LATITUDE, LONGITUDE, WRITE_FILE)

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
