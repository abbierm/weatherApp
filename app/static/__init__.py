from fastapi import APIRouter
from fastapi.responses import FileResponse

static_router = APIRouter(
    tags=["static"]
)

@static_router.get("/static/{filepath:path}")
async def get_static_file(filepath: str):
    response = FileResponse(f"app/static/{filepath}")
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response