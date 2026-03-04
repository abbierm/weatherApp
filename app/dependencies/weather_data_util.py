from datetime import datetime, timedelta, timezone
from .us_lookups import states
from .api_client import APIClient as client

"""
Helper functions that take the data returned 
from OpenWeather's api and put them in format 
used on 'weather.html' result's widget
"""

weather_api_icons = {
    "01n": "night-clear",
    "01d": "day-sunny",

    "02n": "night-cloudy",
    "02d": "day-cloudy",

    "03n": "night-cloudy-high",
    "03d": "day-cloudy-high",

    "04n": "cloudy",
    "04d": "cloudy",

    "09n": "night-rain",
    "09d": "day-showers",

    "10n": "showers",
    "10d": "showers",

    "11n": "night-alt-thunderstorm",
    "11d": "day-thunderstorm",

    "13n": "night-snow",
    "13d": "day-snow",

    "50n": "night-fog",
    "50d": "day-fog"  
}

iconify_parameters = {
    "daily": "height=54",
    "hourly": "height=60",
    "current": "height=110"
}


def select_icon(description: str, time: int) -> str:
    """Returns the html for adding the icon to the homepage. """
    t = 0
    if time >= 22 or time <= 6:
        t = 1
    try:
        icon = io_icons[description][t]
        icon_string = f'<ion-icon name="{icon}"'
        return icon_string
    except KeyError:
            return ""


async def get_icon(id: str, type: str):
    if type not in iconify_parameters.keys():
        # TODO: make some type of error
        return ""
    try:
        icon = weather_api_icons[id]
    except KeyError:
        return ""
    
    url = f"https://api.iconify.design/wi/{icon}.svg?" \
            + iconify_parameters[type] + "&color=%23ccd0c3"
    icon = await client.query_url(url=url)
 
    # TODO: Check for error
    return icon
    
        

def get_wind_direction(deg: int) -> str:
    """
    Returns a string direction for the wind speed
    (i.e 0 -> 'N', 45 -> 'NE', etc.)
    """
    directions = {
                    0: "N",
                    45: "NE",
                    90: "E",
                    135: "SE",
                    180: "S",
                    225: "SW",
                    270: "W",
                    315: "NW",
                    360: "N"
    }
    if not isinstance(deg, float) and not isinstance(deg, int):
        return 'N/A'
    if deg > 360 or deg < 0:
        return 'N/A'
    deg_mod = round(deg) % 45
    if deg_mod > 22:
        return directions[abs((45 - deg_mod) + deg)]
    else:
        return directions[abs(deg - deg_mod)]
    
    
async def format_weather_info(
        w: dict, 
        location: str
) -> dict:    
    # Current Weather
    weather: dict = {"hourly": {}, "daily": {}}
    weather["temp"] = w["current"]["temp"]
    weather["humidity"] = w["current"]["humidity"]    
    weather["description"] = w["current"]["weather"][0]["description"]
    weather["dt"] = w["current"]["dt"]
    weather["pressure"] = w["current"]["pressure"]
    weather["feels_like"] = w["current"]["feels_like"]
    tz = timezone(timedelta(hours=int(w["timezone_offset"] / 3600)))
    dt = datetime.fromtimestamp(weather["dt"], tz)
    weather["hours"] = dt.hour
    c_icon = await get_icon(w["current"]["weather"][0]["icon"], "current")
    weather["icon"] = c_icon
    
    weather["readable_time"] = dt.strftime("%I:%M %p")
    weather["date"] = dt.strftime("%a, %b, %d")
    weather["location"] = format_location(location)
    weather["windspeed"] = w["current"]["wind_speed"]
    weather["wind_direction"] = get_wind_direction(w["current"]["wind_deg"])
    
    #  Hourly
    for i in range(1, 25):
        h = w["hourly"][i]
        new = {}
        ht = datetime.fromtimestamp(h["dt"], tz)
        new["time"] = ht.strftime("%I %p")
        new["temp"] = h["temp"]
        h_icon = await get_icon(h["weather"][0]["icon"], "hourly")
        new["icon"] = h_icon
        weather["hourly"][i + 1] = new

    # daily
    for i in range(1, 8):
        d = w["daily"][i]
        new_day = {}
        date_time = datetime.fromtimestamp(d["dt"])
        new_day["day_name"] = date_time.strftime("%a")
        new_day["month"] = date_time.strftime("%b")
        new_day["day"] = date_time.strftime("%d")
        new_day["high"] = d["temp"]["max"]
        new_day["low"] = d["temp"]["min"]
        # new_day["icon"] = select_icon(d["weather"][0]["main"], 12) + 'class="daily-ion-icon"></ion-icon>'
        d_icon = await get_icon(d["weather"][0]["icon"], "daily")
        new_day["icon"] = d_icon
        weather["daily"][i + 1] = new_day

    return weather

    
def format_location(location_input: str) -> str:
    jurisdictions = location_input.split(", ")
    new_location = jurisdictions[0]
    if jurisdictions[-1].lower() == "united states":
        try:
            state = states[jurisdictions[-2]]
            return new_location + ", " + state
        except KeyError:
            pass
    return new_location + ", " + jurisdictions[-1]
    