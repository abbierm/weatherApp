from pydantic_settings import BaseSettings
from content import WEATHER_API_KEY, GEOCODING_API_KEY
from pathlib import Path
import os


here = Path.cwd()
BASEDIR = os.path.abspath(os.path.dirname(__file__))



class Settings(BaseSettings):
    UVICORN_TIMEOUT_GRACEFUL_SHUTDOWN: int = 5
    testing: bool = False
    base_geocoding_url: str = "https://geocode.maps.co/search?q="
    base_weather_url: str = "https://api.openweathermap.org/data/3.0/onecall?"
    weather_api_key: str = WEATHER_API_KEY
    geocoding_api_key: str = GEOCODING_API_KEY