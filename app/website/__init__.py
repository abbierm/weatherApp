from fastapi import APIRouter


website_router = APIRouter(
    tags=["weather", "website"]
)

from app.website import routes