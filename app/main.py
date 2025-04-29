from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .website import website_router
from .api import api_router
from .static import static_router
from pydantic_settings import BaseSettings
from config import Settings
from .dependencies.api_client import httpx_lifespan_client


def create_app(settings: BaseSettings = Settings):

    app = FastAPI(lifespan=httpx_lifespan_client)

    settings = settings()
    app.state.settings = settings

    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    if settings.dev == True:
        app.include_router(static_router)
    
    app.include_router(website_router)

    app.include_router(api_router)

    return app