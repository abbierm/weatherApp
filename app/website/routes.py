# routes for the website
from fastapi import Request, Depends, Form
from app.website import website_router as r
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from ..dependencies import APIClient, cull_weather_info
from pydantic import BaseModel
import jinja2
import pprint


jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader("app/templates"), auto_reload=True)

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
        parsed_location = location.replace(", ", "+").replace(" ", "+")
        return cls(location=location, parsed_location=parsed_location)
        
	
@r.post("/get_weather", response_class=HTMLResponse)
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

	# Grab lat and lon
    try:
        lat, lon = json_location[0]['lat'], json_location[0]['lon']
        coordinates_string = f"lat={lat}&lon={lon}&appid={s.weather_api_key}"
    except KeyError or IndexError:
        # TODO: Turn this into flash message
        return {"ERROR": f"{form_data.location} not found"}
	
	# Weather API
    weather_url = f"{s.base_weather_url}&units=metric&exclude=minutely&{coordinates_string}"
    json_weather = await client.query_url(url=weather_url)
    
    # TODO: Parse Weather into JUST the stuff needed 
    formatted_weather_dict = cull_weather_info(json_weather, form_data.location)

    pprint.pprint(formatted_weather_dict)
    return templates.TemplateResponse(
		"weather.html",
        {
            "request": request,
            "info": formatted_weather_dict
        }
    )