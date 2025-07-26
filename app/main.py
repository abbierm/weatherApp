from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from .website import website_router
from .api import api_router
from .static import static_router
from pydantic_settings import BaseSettings
from config import Settings
from .dependencies.api_client import httpx_lifespan_client
from .errors.handlers import register_exception_handlers
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware



def create_app(settings: BaseSettings = Settings):

    settings = settings()
    
    middleware = [Middleware(SessionMiddleware, secret_key=settings.secret_key)]
    
    app = FastAPI(lifespan=httpx_lifespan_client, middleware=middleware)

    app.state.settings = settings

    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    if settings.dev == True:
        app.include_router(static_router)
    
    app.include_router(website_router)

    app.include_router(api_router)

    register_exception_handlers(app)

    return app