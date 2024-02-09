import aiohttp
from enum import Enum


class Method(Enum):
    GET = 'GET'
    POST = 'POST'
    DELETE = 'DELETE'
    PATCH = 'PATCH'
    PUT = 'PUT'


class HTTPClient:
    def __init__(self, base_url: str | None = None):
        self._base_url = base_url

    async def api_request(
            self, url: str,
            method: Method = Method.GET,
            data: dict | None = None,
            params: dict | None = None,
            headers: dict | None = None,
            ok_status_code: int = 200
    ):
        async with aiohttp.ClientSession(base_url=self._base_url) as session:
            async with session.request(
                    method=method.value,
                    url=url,
                    data=data,
                    params=params,
                    headers=headers
            ) as response:
                if response.status == ok_status_code:
                    return await response.json()
