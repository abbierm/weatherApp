
from fastapi import Request, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import request_validation_exception_handler



async def custom_validation_exception_handler(request: Request, exc: RequestValidationError):
	return JSONResponse(
		status_code=422,
		content={
			"message": "Missing required location parameter",
			"example": "/api/weather/location={some+location+you+want+weather+for}",
			"details": exc.errors(),
		},
	)


def register_exception_handlers(app: FastAPI):
	app.add_exception_handler(RequestValidationError, custom_validation_exception_handler)