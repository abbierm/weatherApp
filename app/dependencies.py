from fastapi import FastAPI
import httpx
from typing import Optional
from contextlib import asynccontextmanager
from datetime import datetime


class APIClient:
    httpx_client: Optional[httpx.AsyncClient] = None

    @classmethod
    def get_httpx_client(cls) -> httpx.AsyncClient:
        if cls.httpx_client is None:
            timeout = httpx.Timeout(timeout=2)
            limits = httpx.Limits(max_keepalive_connections=5,
								    max_connections=10)
            cls.httpx_client = httpx.AsyncClient(timeout=timeout,
                                    limits=limits, http2=True)
        return cls.httpx_client
        
    @classmethod
    async def close_httpx_client(cls) -> None:
        if cls.httpx_client:
            await cls.httpx_client.aclose()
            cls.httpx_client = None

    @classmethod
    async def query_url(cls, url: str) -> dict:
        client = cls.get_httpx_client()
        try:
            response = await client.get(url)
            if response.status_code != 200:
                return {"ERROR OCCURED" + str(await response.text())}
            json_result = response.json()
        except Exception as e:
            return {"ERROR": str(e)}
        return json_result


@asynccontextmanager
async def httpx_lifespan_client(app: FastAPI):
    APIClient.get_httpx_client()
    
    yield

    await APIClient.close_httpx_client()


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
    if not isinstance(deg, float) or not isinstance(deg, int):
        return 'N/A'
    if deg > 360 or deg < 0:
        return 'N/A'
    deg_mod = round(deg) % 45
    if deg_mod > 22:
        return directions[abs((45 - deg_mod) + deg)]
    else:
        return directions[abs(deg - deg_mod)]


def cull_weather_info(
        w: dict, 
        location: str
) -> dict:
    """
    {
        
        "temp": int C,
        "humidity": int,
        "conditions": str,
        "icon": str,
        "time": "str",
        "date": str,
        "location" str,
        "windspeed": int, 
        "wind-direction": str,
        "hourly": 
                {1: {"time": str,"temp": int,"icon": str}, ...},
        "Daily": 
                {1: {"high-temp": int, "low-temp": int,"icon": str}, ...}
    }
    """
    # Current Weather
    weather: dict = {"hourly": {}, "daily": {}}
    weather["temp"] = w["current"]["temp"]    
    weather["humidity"] = w["current"]["humidity"]    
    weather["description"] = w["current"]["weather"][0]["description"]
    dt = datetime.fromtimestamp(w["current"]["dt"])
    # always putting in normal time format
    weather["time"] = dt.strftime("%new_dayI:%M %p")
    weather["date"] = dt.strftime("%a, %b, %d %Y")
    weather["location"] = location
    weather["windspeed"] = w["current"]["wind_speed"]
    weather["wind-direction"] = get_wind_direction(w["current"]["wind_deg"])
    
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


    
