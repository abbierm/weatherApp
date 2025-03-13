from content import API_KEY
import httpx
import asyncio
from typing import List, Optional, Any, Dict

BASE_URL = "https://api.openweathermap.org/"


class HTTPXClient:
	httpx_client: Optional[httpx.AsyncClient] = None
	


	@classmethod
	def get_httpx_client(cls) -> httpx.AsyncClient:
		print("Opening httpx client")
		if cls.httpx_client is None:
			timeout = httpx.Timeout(timeout=2)
			limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
			cls.httpx_client = httpx.AsyncClient(
				timeout=timeout, 
				limits=limits, 
				http2=True
			)
		return cls.httpx_client

	@classmethod
	async def close_httpx_client(cls) -> None:
		print("Closing httpx client")
		if cls.httpx_client:
			await cls.httpx_client.aclose()
			cls.httpx_client = None

	

	@classmethod
	async def query_url(cls, url: str) -> Any:
		client = cls.get_httpx_client()
		try:
			response = await client.get(url)
			if response.status_code != 200:
				return {"ERROR OCCURED" + str(await response.text())}
				
			json_result = response.json()
		except Exception as e:
			return {"ERROR": e}
		
		return json_result

	@classmethod
	async def build_request(cls, **kwargs):
		if 'lat' in kwargs:
			lat, lon = kwargs['lat'], kwargs['lon']
			url = BASE_URL + f"data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely&units=imperial&appid={API_KEY}"
		elif 'location' in kwargs:
			location = kwargs['location']
			url = BASE_URL + f"geo/1.0/direct?q={location}&limit=5&appid={API_KEY}"
		
		else:
			return {"ERROR": "Invalid form data"}
		return await cls.query_url(url)
		
		

	@classmethod
	async def get_weather_request(cls, lon: str | int, lat: str | int) -> Any:
		url = base_url +  f"data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely&units=imperial&appid={API_KEY}"
		# response = cls.query_url(HTTPXClient, url)
		client = cls.get_httpx_client()
		try:
			response = await client.get(url)
			if response.status_code != 200:
				return {"ERROR OCCURED" + str(await resopnse.text())}

			json_result = response.json()
		except Exception as e:
			return {"Error": e}
		return json_result
		

	@classmethod
	async def get_geolocation_request(cls, location: str) -> Any:
		location = location.replace(", ", ",")
		url = BASE + f"geo/1.0/direct?q={location}&limit=5&appid={API_KEY}"
		client = cls.get_httpx_client()
		try:
			response = await client.get(url)
			if response.status_code != 200:
				return {"ERROR OCCURED" + str(await resopnse.text())}

			json_result = response.json()
		except Exception as e:
			return {"Error": e}
		return json_result


	

def remove_names(locations: list) -> dict:
	"""Removes 'local_names' key from the json geo api call. """
	locations_dict = []
	for location in locations:
		new_dict = {"name": None, "lat": None, "lon": None, "country": None, "state": None}
		for key in new_dict.keys():
			new_dict[key] = location[key]
		locations_dict.append(new_dict)
	return locations_dict
