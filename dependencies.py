import httpx
from typing import Optional
from config import Settings
from functools import lru_cache


settings = Settings()

@lru_cache
def get_settings():
	return settings


class APIClient:
	httpx_client: Optional[httpx.AsyncClient] = None

	@classmethod
	def get_httpx_client(cls) -> httpx.AsyncClient:
		print("Opening httpx client")
		if cls.httpx_client is None:
			timeout = httpx.Timeout(timeout=2)
			limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
			cls.httpx_client = httpx.AsyncClient(
				timeout=timeout, 
				limits=limits, 
				http2=True
			)
		return cls.httpx_client
        
	@classmethod
	async def close_httpx_client(cls) -> None:
		print("Closing httpx client")
		if cls.httpx_client:
			await cls.httpx_client.aclose()
			cls.httpx_client = None

	@classmethod
	async def query_url(cls, url: str) -> dict:
		client = cls.get_httpx_client()
		try:
			response = await client.get(url)
			if response.status_code != 200:
				return {"ERROR OCCURED" + str(await response.text())}
			json_result = response.json()
		except Exception as e:
			return {"ERROR": e}
		return json_result


async def on_start_up() -> None:
	APIClient.get_httpx_client()
	
async def on_shutdown() -> None:
	await APIClient.close_httpx_client()
	
