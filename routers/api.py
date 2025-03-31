# routes for the api via /api/weather?city={userscity}

from fastapi import APIRouter, Depends
from dependencies import APIClient, get_settings
from typing import Optional, Literal
from pydantic import BaseModel


api_router = r = APIRouter(
    prefix="/api",
    tags=["weatherAPI"]
)

# Possible Queries
class QueryParameters(BaseModel):
    location: str
    exclude: Optional[Literal["current", "minutely", "hourly", "daily", "alerts"]] = None
    units: Optional[Literal["standard", "metric", "imperial"]] = "standard"
    lang: Optional[Literal["en", "sp"]] = "en"



@r.get("/weather")
async def weather(
    client = Depends(APIClient),
    q = Depends(QueryParameters),
    settings = Depends(get_settings)
):
    if "Error" in q:
        return q
    
    # makes geo_location_url with query location
    location = q.location
    
    # Geo API
    geo_url = settings.base_geocoding_url + \
                    location + "&api_key=" + settings.geocoding_api_key
    json_location =  await client.query_url(url=geo_url)
    try:
        lat, lon = json_location[0]['lat'], json_location[0]['lon']
        coordinates_string = f"lat={lat}&lon={lon}&appid={settings.weather_api_key}"
    except KeyError:
        return {"ERROR": f"{q.location} not found"}
    
    # Weather API
    weather_url = settings.base_weather_url + coordinates_string
    return await client.query_url(weather_url)

    
      
