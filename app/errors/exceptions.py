

class WeatherAPIError(Exception):
	"""Base exception class"""

	def __init__(self, message: str = "Error Occurred"):
		self.message = message
		super().__init__(self.message)


class NoLocationError(WeatherAPIError):
	"""User didn't enter a location"""
	pass

class InvalidLocationError(WeatherAPIError):
	"""Location wasn't found from geo api"""
	pass

class OpenWeatherTimeOutError(WeatherAPIError):
	"""Open WeatherAPI took over 5s to respond resulting in a timeout"""
	pass

