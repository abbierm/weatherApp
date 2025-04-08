from fastapi import FastAPI
import httpx
from typing import Optional
from contextlib import asynccontextmanager



class APIClient:
    httpx_client: Optional[httpx.AsyncClient] = None

    @classmethod
    def get_httpx_client(cls) -> httpx.AsyncClient:
        if cls.httpx_client is None:
            timeout = httpx.Timeout(timeout=2)
            limits = httpx.Limits(max_keepalive_connections=5,
								    max_connections=10)
            cls.httpx_client = httpx.AsyncClient(timeout=timeout,
                                    limits=limits, http2=True)
        return cls.httpx_client
        
    @classmethod
    async def close_httpx_client(cls) -> None:
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
            return {"ERROR": str(e)}
        return json_result


@asynccontextmanager
async def httpx_lifespan_client(app: FastAPI):
    APIClient.get_httpx_client()
    
    yield

    await APIClient.close_httpx_client()
	
