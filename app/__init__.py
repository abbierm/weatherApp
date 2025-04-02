from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .main import main_router
from .api import api_router
from pydantic_settings import BaseSettings
from config import Settings
from .dependencies import on_start_up, on_shutdown


def create_app(settings: BaseSettings = Settings):

    app = FastAPI(on_startup=[on_start_up], on_shutdown=[on_shutdown])

    settings = settings()
    app.state.settings = settings

    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    app.include_router(main_router)

    app.include_router(api_router)

    return app