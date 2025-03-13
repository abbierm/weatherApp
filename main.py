from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers.routes import weather_router
import uvicorn
from dependencies import HTTPXClient
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	UVICORN_TIMEOUT_GRACEFUL_SHUTDOWN: int = 5



async def on_start_up() -> None:
	
	HTTPXClient.get_httpx_client()
	

async def on_shutdown() -> None:
	await HTTPXClient.close_httpx_client()


settings = Settings()
app = FastAPI(on_startup=[on_start_up], on_shutdown=[on_shutdown])



# Sets a header to tell browser not the cache the header
@app.get("/static/{filepath:path}")
async def get_static_file(filepath: str):
	response = FileResponse(f"static/{filepath}")
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	return response

@app.get("/get_info")
async def get_info():
	return {
		"UVICORN_TIMEOUT_GRACEFUL_SHUTDOWN": settings.UVICORN_TIMEOUT_GRACEFUL_SHUTDOWN
	}


app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(weather_router,
			responses={418: {"description": "I'm a teapot"}})


if __name__ == "__main__":
	uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)