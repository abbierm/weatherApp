from fastapi import APIRouter

static_router = APIRouter(
    tags=["static"]
)

from app.static import mount