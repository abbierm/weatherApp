from datetime import datetime, timedelta, timezone
from .us_lookups import states

"""
Helper functions that take the data returned 
from OpenWeather's api and put them in format 
used on 'weather.html' result's widget
"""

io_icons = {
    # clear
    "clear": ("sunny", "moon"),
    "clear sky": ("sunny", ""),  
    "few clouds": ("sunny", "moon"), 

    # cloudy
    "scattered clouds": ("cloudy", "cloudy-night"),
    "broken clouds": ("cloudy", "cloudy-night"),
    "overcast clouds": ("cloudy", "cloudy"),   


    # rainy
    "shower rain": ("rainy", "umbrella"), 
    "rain": ("rainy", "umbrella"),
    "light rain": ("rainy", "umbrella"),
    "moderate rain": ("rainy", "umbrella"), 
    "heavy intensity rain": ("rainy", "umbrella"),
    
    

    # thunderstormy
    "thunderstorm": ("thunderstorm", "thunderstorm"),
    "thunderstorm with heavy rain":  ("thunderstorm", "thunderstorm"),
    "thunderstorm with rain":  ("thunderstorm", "thunderstorm"),


    # snowy
    "snow": ("snow", "snow"), 


    # foggy
    "mist": ("menu", "menu"),  
    "haze": ("menu", "menu"), 

    
    
}

icons = {
    "heavy intensity rain": ("heavyRain.svg", "NightRainHeavy.svg"),
    "shower rain": ("heavyRain.svg", "NightRainHeavy.svg"), 
    "rain": ("heavyRain.svg", "NightRainHeavy.svg"),
    "moderate rain": ("heavyRain.svg", "NightRainHeavy.svg"),
    "light rain": ("heavyRain.svg", "NightRainHeavy.svg"),
    "thunderstorm": ("heavyRain.svg", "NightRainHeavy.svg"),
    "very heavy rain": ("heavyRain.svg", "NightRainHeavy.svg"),
}

def select_icon(description: str, time: int) -> str:
    """Returns the html for adding the icon to the homepage. """
    t = 0
    print(description)
    if time >= 21 or time < 6:
        t = 1
    try:
        icon = icons[description][t]
        return f'<img src="../../static/icons/{icon}" class="big-icon">'
    except KeyError:
        try:
            icon = io_icons[description][t]
            icon_string = f'<ion-icon name="{icon}" class="big-io-icon"></ion-icon>'
            return icon_string
        except KeyError:
            return ""
        

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
    
    
def format_weather_info(
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
    weather["icon"] = select_icon(weather["description"], weather["hours"])
    # always putting in normal time format
    weather["readable_time"] = dt.strftime("%I:%M %p")
    
    weather["date"] = dt.strftime("%a, %b, %d")
    weather["location"] = format_location(location)
    weather["windspeed"] = w["current"]["wind_speed"]
    weather["wind_direction"] = get_wind_direction(w["current"]["wind_deg"])
    
    #  Hourly
    for i in range(5):
        h = w["hourly"][i]
        new = {}
        ht = datetime.fromtimestamp(h["dt"])
        new["time"] = ht.strftime("%I %p")
        new["temp"] = h["temp"]
        new["icon"] = h["weather"][0]["description"]
        weather["hourly"][i + 1] = new

    # daily
    for i in range(7):
        d = w["daily"][i]
        new_day = {}
        date_time = datetime.fromtimestamp(d["dt"])
        new_day["month_abr"] = date_time.strftime("%a")
        new_day["month"] = date_time.strftime("%m")
        new_day["day"] = date_time.strftime("%d")
        new_day["high"] = d["temp"]["max"]
        new_day["low"] = d["temp"]["min"]
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
    