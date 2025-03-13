from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dependencies import HTTPXClient, remove_names
from typing import Annotated, Optional, Union
from pydantic import BaseModel
import ast



templates = Jinja2Templates(
	directory="./templates/", 
	auto_reload=True)


weather_router = APIRouter(
	tags=["weather"])


#==============================================================================
# Weather Page Routes
#==============================================================================
@weather_router.get("/", response_class=HTMLResponse)
def index(request: Request):
	return templates.TemplateResponse(request=request, name="index.html")


class ConfirmLocationGeo(BaseModel):
	geo_location: dict
	location: str
	save_response: bool

	@classmethod
	def as_form(
		cls,
		geocoordinates: str = Form(...),
		save_response: Union[str, None] = Form(None)
	):
		save_response_bool = True if save_response == "on" else False
		geo_response = ast.literal_eval(geocoordinates)
		geo_location = {}
		geo_location['lat'], geo_location['lon'] = geo_response['lat'], geo_response['lon']
		return cls(geo_location=geo_location, save_response=save_response_bool, location=geo_response['location'])


@weather_router.post("/local_weather/", response_class=HTMLResponse)
async def local_weather(
	request: Request,
	form_data: ConfirmLocationGeo = Depends(ConfirmLocationGeo.as_form)
):
	lat, lon = form_data.geo_location['lat'], form_data.geo_location['lon']
	location = form_data.location

	json_response = await HTTPXClient.build_request(lat=lat, lon=lon,
	 													location=location)
	# for thing in json_response:
	# 	print(thing)

	print(type(json_response))
	
	return templates.TemplateResponse(
		"weather.html", 
		{
			"request": request, 
			"location": location,
			"info": json_response
		}
	)


#==============================================================================
# Location Route
#==============================================================================
class LocationFormData(BaseModel):
	location: str


@weather_router.post("/confirm-location/", response_class=HTMLResponse)
async def location(
	request: Request,
	location: Annotated[str, Form()]
):
	"""Use geo-api to get lat and lon for user's location input. """
	
	locations_with_names = await HTTPXClient.build_request(location=location)
	
	if len(locations_with_names) == 0:
		flash = {"messages": []}
		flash["messages"].append(f"Unable to find {location}")
		return templates.TemplateResponse("index.html", {"request": request,"flash": flash})
		
	locations = remove_names(locations_with_names)

	return templates.TemplateResponse(
		"confirmLocation.html", 
		{
			"request": request, 
			"locations": locations
		}
	)
