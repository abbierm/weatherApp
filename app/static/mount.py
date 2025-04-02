from fastapi.responses import FileResponse

from app.static import static_router as r


# sets a no caching header for static files
# Should turn this off when deployed
@r.get("/static/{filepath:path}")
async def get_static_file(filepath: str):
	response = FileResponse(f"static/{filepath}")
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	return response