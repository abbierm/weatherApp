# routes for the website
from fastapi import Request, Depends, Form
from app.website import website_router as r
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from ..dependencies import APIClient
from typing import Optional
from pydantic import BaseModel
import jinja2


jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader("app/templates"), auto_reload=True)

templates = Jinja2Templates(env=jinja_env)

# Homepage
@r.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


class LocationForm(BaseModel):
    city: str
    state: Optional[str]
    country: Optional[str]
    save_response: bool

    @classmethod
    def check_form(
        cls, 
        city: str = Form(...),
        state: str | None = Form(""),
        country: str | None = Form(""),
        save_response: str | None = Form("")
    ):
        save_response_bool = True if save_response == "on" else False
        city = city.replace(" ", "")
        state = state.replace(" ", "")
        country = country.replace(" ", "")
        return cls(city=city, state=state, country=country,
				                save_response=save_response_bool)
	

@r.post("/get_weather", response_class=HTMLResponse)
async def get_weather(
    request: Request,
    form_data: LocationForm = Depends(LocationForm.check_form),
    client: APIClient = Depends(APIClient)
):
	# config settings
    s = request.app.state.settings
    
    # Geo coordinates
    geo_form_string = f"{form_data.city}+{form_data.state}+{form_data.country}"
    geo_url = s.base_geocoding_url + geo_form_string + "&api_key=" + s.geocoding_api_key
    json_location = await client.query_url(url=geo_url)
	
	# Grab lat and lon
    try:
        lat, lon = json_location[0]['lat'], json_location[0]['lon']
        coordinates_string = f"lat={lat}&lon={lon}&appid={s.weather_api_key}"
    except KeyError:
        # TODO: Turn this into flash message
        return {"ERROR": f"{form_data.city} not found"}
	
	# Weather API
    weather_url = f"{s.base_weather_url}&exclude=minutely&{coordinates_string}"
    json_weather = await client.query_url(url=weather_url)
    return templates.TemplateResponse(
		"weather.html",
        {
            "request": request,
            "location": form_data.city,
            "info": json_weather
        }
    )