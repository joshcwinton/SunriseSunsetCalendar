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
latitude = 40.6302887
longitude = -73.9029366
daysAhead = 10
timeZone = 'America/New_York'
writefile = 'sunrise-sunset.ics'

def getSunriseSunsetData(latitude: str, longitude: str, daysFromNow: int):
    """Fetches data from sunrise-sunset API."""
    # Send request to API for lat and long unformatted
    r = requests.get("https://api.sunrise-sunset.org/json", params={'lat': latitude, 'lng': longitude, 'formatted': 0, 'date': f"{daysFromNow} days"})
    # Extract sunrise and sunset from result
    utc_sunrise = r.json()['results']['sunrise']
    utc_sunset = r.json()['results']['sunset']

    return (utc_sunrise, utc_sunset)


def convertToLocal(time: str):
    """Converts an ISO format UTC time to a local time."""
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz(timeZone)
    utc = datetime.fromisoformat(time)
    utc = utc.replace(tzinfo=from_zone)
    local = utc.astimezone(to_zone)
    return(local)

def createCalendarEvent(calendar, sunrise: str, sunset: str):
    """Generates and adds a sunrise and sunset event to `calendar`."""
    sunrise_event = Event()
    sunrise_event.name = f"☀️ {sunrise.strftime('%I')}:{sunrise.strftime('%M')}"
    sunrise_event.begin = sunrise
    calendar.events.add(sunrise_event)

    sunset_event = Event()
    sunset_event.name = f"🌙 {sunset.strftime('%I')}:{sunset.strftime('%M')}"
    sunset_event.begin = sunset
    calendar.events.add(sunset_event)

def main():
    """ Main entry point of the app """
    print(f"Sunrise Sunset Calendar v{__version__}\n")
    # TODO: Take zip code as a command line argument and look up lat long
    print("Location:")
    print(f"\tLatitude:\t{latitude}")
    print(f"\tLongitude:\t{longitude}")

    print("Getting data...")
    c = Calendar() # Calendar object to store all events

    for i in progressbar.progressbar(range(daysAhead)):
        time.sleep(1) # Wait between requests to avoid usage limit
        utc_sunrise, utc_sunset = getSunriseSunsetData(latitude, longitude, i)
        local_sunrise = convertToLocal(utc_sunrise)
        local_sunset = convertToLocal(utc_sunset)
        createCalendarEvent(c, local_sunrise, local_sunset) 


    with open(writefile, 'w') as f:
        f.write(str(c))

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
