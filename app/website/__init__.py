from fastapi import APIRouter


website_router = APIRouter(
    tags=["weather"]
)

from app.website import routes