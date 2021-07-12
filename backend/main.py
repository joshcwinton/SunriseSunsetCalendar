#!/usr/bin/env python3
"""
Used for creating a calendar file with sunrise and sunset times.

This script fetches sunrise and sunset data from the API here: 
 https://api.sunrise-sunset.org/json. It then uses that data to create an
 iCal file that displays the time of sunrise and sunset everyday.
"""
from io import IncrementalNewlineDecoder
import requests
from datetime import datetime
from dateutil import tz
from ics import Calendar, Event
import time
import progressbar
from pyzipcode import ZipCodeDatabase

__author__ = "Josh Winton"
__version__ = "0.1.0"
__license__ = "MIT"

def getLatLongFromZip(zip: IncrementalNewlineDecoder):
    """Converts Zip code to latitude and longitude.
    
    Args:
        zip: Zip code to convert.
        
    Returns:
        Tuple containing latitude and longitude in degrees"""
    # Convert zip to lat long
    zcdb = ZipCodeDatabase()
    zip_info = zcdb[zip]
    lat = zip_info.latitude
    long = zip_info.longitude

    # Call lat long function
    return (lat, long)

def getSunriseSunsetDataLatLong(latitude: str, longitude: str, daysFromNow: int = 0):
    """Fetches data from sunrise-sunset API.
    
    Args:
        latitude: Latitude in degrees.

        longitude: Longitude in degrees.

        daysFromNow: Specify fetching data for a date N days in the future. 

    Returns:
        Tuple containing sunrise and sunset in ISO format.
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
        The time in local time based on POSIX TZ variable.
    """
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz() # May want to get local time for lat long in the future
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
        time.sleep(0.2) # Wait between requests to avoid API usage limit
        utc_sunrise, utc_sunset = getSunriseSunsetDataLatLong(latitude, longitude, i)
        local_sunrise = convertTimeToLocal(utc_sunrise)
        local_sunset = convertTimeToLocal(utc_sunset)
        createCalendarEvent(calendar, local_sunrise, local_sunset) 

    with open(filename, 'w') as f:
        f.write(str(calendar))



def main():
    """ Main entry point of the app """
    print(f"Sunrise Sunset Calendar v{__version__}\n")
    zip = input("Enter your ZIP code: ")
    filename = input("Enter filename to save to (default 'sunrise-sunset.ics'): ")
    if filename == "":
        filename = "sunrise-sunset.ics"
    print("Getting data...")
    lat, long = getLatLongFromZip(int(zip))
    generateCalendarFile(lat, long, filename)
    print(f"Calendar file saved to {filename}.")

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
