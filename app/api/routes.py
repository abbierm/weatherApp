# routes for the api
# /api/weather?location={city+state+country+whatever}

from fastapi import Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.api import api_router as r
from ..dependencies.api_client import APIClient
from typing import Optional, Literal
from pydantic import BaseModel
from ..errors.exceptions import(
    NoLocationError, 
    InvalidLocationError, 
    OpenWeatherTimeOutError
)


# Possible Queries
class QueryParameters(BaseModel):
    # location: str
    exclude: Optional[Literal["current", "minutely", "hourly", "daily", "alerts"]] = None
    units: Optional[Literal["standard", "metric", "imperial"]] = "imperial"
    lang: Optional[Literal["en", "es", "sp"]] = "en"

 
def make_weather_query(
        lat: str,
        lon: str,
        exclude: Optional[str] = None,
        units: str = "standard",
        language: str = "en"
) -> str:
    if exclude is None:
        return f"lat={lat}&lon={lon}&units={units}&language={language}&appid="
    else:
        return f"lat={lat}&lon={lon}&units={units}&lang={language}&exclude={exclude}&appid="
    

@r.get("/weather/{location}")
async def weather(
    location: str,
    request: Request,
    client = Depends(APIClient),
    q = Depends(QueryParameters)
):
    
    # Gets app settings
    s = request.app.state.settings
    
    # extracts location from query
    location = location.replace(" ", "+")
    
    # Geo API
    geo_url = s.base_geocoding_url + \
                    location + "&api_key=" + s.geocoding_api_key
    
    json_location =  await client.query_url(url=geo_url)

    if "ERROR" in json_location:
        raise InvalidLocationError("Location Not Found")
    
    lat, lon = json_location[0]['lat'], json_location[0]['lon']
    weather_query = make_weather_query(lat, lon, q.exclude, q.units, q.lang)
    weather_url = s.base_weather_url + weather_query + s.weather_api_key
    
    # Weather API
    weather_results = await client.query_url(weather_url)
    if "ERROR" in weather_results:
        raise OpenWeatherTimeOutError("Unable to access weather at this time")
    return weather_results

    
      
@r.get("/weather/")
def weather_no_location():
    raise NoLocationError("Missing location")