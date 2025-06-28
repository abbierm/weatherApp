# routes for the website ./ & ./get_weather
# ./get_weather is the final form for /

from fastapi import Request, Depends, Form, HTTPException
from app.website import website_router as r
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from ..dependencies.api_client import APIClient
from ..dependencies.weather_data_util import format_weather_info
from pydantic import BaseModel
import jinja2



jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader("app/templates"),
                                auto_reload=True)

templates = Jinja2Templates(env=jinja_env)

# Homepage
@r.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


class LocationForm(BaseModel):
    location: str
    parsed_location: str | None = None # For geocoordinates api

    @classmethod
    def parse_location(
        cls,
        location: str = Form(...)
    ):
        """Turns location input into string formatted for api query"""
        parsed_location = location.replace(", ", "+").replace(" ", "+")
        return cls(location=location, parsed_location=parsed_location)
        
	
@r.post("/", response_class=HTMLResponse)
async def get_weather(
    request: Request,
    form_data: LocationForm = Depends(LocationForm.parse_location),
    client: APIClient = Depends(APIClient)
):
	# config settings
    s = request.app.state.settings
    
    # Geo coordinates
    geo_url = s.base_geocoding_url + form_data.parsed_location + "&api_key=" + s.geocoding_api_key
    json_location = await client.query_url(url=geo_url)
    if len(json_location) == 0:
        raise HTTPException(status_code=422, detail=f"{form_data.location} not found")


	# Grab lat and lon from geocoding response
    try:
        lat, lon = json_location[0]['lat'], json_location[0]['lon']
        coordinates_string = f"lat={lat}&lon={lon}&appid={s.weather_api_key}"
    except Exception as err:
        # TODO: Turn this into flash message
        return {"ERROR": f"{form_data.location} not found"}
    	
	# Weather API 
    weather_url = f"{s.base_weather_url}&units=metric&exclude=minutely&{coordinates_string}"
    json_weather = await client.query_url(url=weather_url)
    
    # Cull large weather response just for needed entities
    formatted_weather_dict = format_weather_info(json_weather, json_location[0]['display_name'])

    return templates.TemplateResponse(
		"weather_flex.html",
        {
            "request": request,
            "info": formatted_weather_dict
        }
    )