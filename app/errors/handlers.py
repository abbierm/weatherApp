
from fastapi import Request, FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from .exceptions import (
	WeatherAPIError,
	NoLocationError,
	InvalidLocationError,
	OpenWeatherTimeOutError
)
from typing import Callable



def create_exception_handler(
	status_code: int,
	details: str
) -> Callable[[Request, WeatherAPIError], JSONResponse]:
	detail = {"message": details}

	async def exception_handler(
		r: Request, 
		exc: WeatherAPIError
	) -> JSONResponse:
		if exc.message:
			detail["message"] = exc.message

		return JSONResponse(
			status_code=status_code, content={"detail": detail["message"]}
		)

	return exception_handler


# async def custom_validation_exception_handler():
# 	return JSONResponse(
# 		status_code=422,
# 		content={
# 			"message": "Missing required location parameter",
# 			"example": "/api/weather/location={some+location+you+want+weather+for}",
# 			"details": exc.errors(),
# 		},
# 	)


def register_exception_handlers(app: FastAPI):
	app.add_exception_handler(
		exc_class_or_status_code=NoLocationError,
		handler=create_exception_handler(
			status.HTTP_400_BAD_REQUEST,
			"Missing required location parameter"
		),
	)
	app.add_exception_handler(
		exc_class_or_status_code=InvalidLocationError,
		handler=create_exception_handler(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			details="Location not found"
		),
	)
	app.add_exception_handler(
		exc_class_or_status_code=OpenWeatherTimeOutError,
		handler=create_exception_handler(
			status.HTTP_503_SERVICE_UNAVAILABLE,
			"External weather api not responding"
		),
	)