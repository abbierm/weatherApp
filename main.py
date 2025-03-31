from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from dependencies import on_start_up, on_shutdown


app = FastAPI(on_startup=[on_start_up], on_shutdown=[on_shutdown])


# sets a no caching header for static files
# Should turn this off when deployed
@app.get("/static/{filepath:path}")
async def get_static_file(filepath: str):
	response = FileResponse(f"static/{filepath}")
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	return response


app.mount("/static", StaticFiles(directory="static"), name="static")


from routers.api import api_router
app.include_router(api_router)

from routers.weather import website_router
app.include_router(website_router)


if __name__ == "__main__":
	uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)