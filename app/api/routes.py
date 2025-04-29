# routes for the api via /api/weather?city={userscity}
from fastapi import Request, Depends
from app.api import api_router as r
from ..dependencies.api_client import APIClient
from typing import Optional, Literal
from pydantic import BaseModel


# Possible Queries
class QueryParameters(BaseModel):
    location: str
    exclude: Optional[Literal["current", "minutely", "hourly", "daily", "alerts"]] = None
    units: Optional[Literal["standard", "metric", "imperial"]] = "standard"
    lang: Optional[Literal["en", "es", "sp"]] = "en"

 
def make_weather_url(
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
    


@r.get("/weather")
async def weather(
    request: Request,
    client = Depends(APIClient),
    q = Depends(QueryParameters)
):
    if "Error" in q:
        return q
    
    # Gets app settings
    s = request.app.state.settings
    
    # makes geo_location_url with query location
    location = q.location
    
    # Geo API
    geo_url = s.base_geocoding_url + \
                    location + "&api_key=" + s.geocoding_api_key
    json_location =  await client.query_url(url=geo_url)
    try:
        lat, lon = json_location[0]['lat'], json_location[0]['lon']
        weather_query = make_weather_url(lat, lon, q.exclude, q.units, q.lang)
        weather_url = s.base_weather_url + weather_query + s.weather_api_key
    except KeyError:
        return {"ERROR": f"{q.location} not found"}
    
    # Weather API
    return await client.query_url(weather_url)

    
      
