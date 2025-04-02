from fastapi import APIRouter

api_router = APIRouter(
    tags=["weatherAPI"],
    prefix="/api"
)

from app.api import routes