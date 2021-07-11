# Sunrise Sunset Calendar

This script fetches data from the [Sunrise Sunset API](https://sunrise-sunset.org/) and creates an [iCalendar](https://en.wikipedia.org/wiki/ICalendar) file so that it can be used in your Google, iCloud, or Outlook calendar.

Uses the [ICS Python Library](https://pypi.org/project/ics/) to create the .ics file.

## Installation and Usage
1. Clone this repo and navigate to it
2. `pip install -r requirements.txt`
3. `python3 main.py`
4. Open the generated .ics file 

## Future Work
- Add command line input that requests a zip code and looks up latitude and longitude and time zone automatically using [Google Geocoding API](https://developers.google.com/maps/documentation/geocoding/overview)
- Create calendar subscription using [Google Calendar API](https://developers.google.com/calendar/api/quickstart/python)
- Create a frontend that allows you to directly download a .ics file
