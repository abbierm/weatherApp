from fastapi import APIRouter

api_router = APIRouter(
    tags=["api", "weather"],
    prefix="/api"
)

from app.api import routes