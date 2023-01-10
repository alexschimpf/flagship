import httpx
from typing import Union, Dict, Any
from fastapi import FastAPI, testclient

from rest_api_tester.client import BaseTestClient


class FastAPITestClient(BaseTestClient):

    def __init__(self, app: FastAPI):
        self.client = testclient.TestClient(app)

    def get(  # type: ignore
        self,
        url: str,
        timeout: int,
        allow_redirects: bool,
        headers: Union[Dict[str, Any], None] = None,
        cookies: Union[Dict[str, Any], None] = None
    ) -> httpx.Response:
        return self.client.get(
            url=url,
            timeout=timeout,
            allow_redirects=allow_redirects,
            headers=headers,
            cookies=cookies
        )

    def post(  # type: ignore
        self,
        url: str,
        data: str,
        timeout: int,
        allow_redirects: bool,
        headers: Union[Dict[str, Any], None] = None,
        cookies: Union[Dict[str, Any], None] = None
    ) -> httpx.Response:
        return self.client.post(
            url=url,
            content=data,
            timeout=timeout,
            allow_redirects=allow_redirects,
            headers=headers,
            cookies=cookies
        )

    def put(  # type: ignore
        self,
        url: str,
        data: str,
        timeout: int,
        allow_redirects: bool,
        headers: Union[Dict[str, Any], None] = None,
        cookies: Union[Dict[str, Any], None] = None
    ) -> httpx.Response:
        return self.client.put(
            url=url,
            content=data,
            timeout=timeout,
            allow_redirects=allow_redirects,
            headers=headers,
            cookies=cookies
        )

    def patch(  # type: ignore
        self,
        url: str,
        data: str,
        timeout: int,
        allow_redirects: bool,
        headers: Union[Dict[str, Any], None] = None,
        cookies: Union[Dict[str, Any], None] = None
    ) -> httpx.Response:
        return self.client.patch(
            url=url,
            content=data,
            timeout=timeout,
            allow_redirects=allow_redirects,
            headers=headers,
            cookies=cookies
        )

    def delete(  # type: ignore
        self,
        url: str,
        timeout: int,
        allow_redirects: bool,
        headers: Union[Dict[str, Any], None] = None,
        cookies: Union[Dict[str, Any], None] = None
    ) -> httpx.Response:
        return self.client.delete(
            url=url,
            timeout=timeout,
            allow_redirects=allow_redirects,
            headers=headers,
            cookies=cookies
        )
