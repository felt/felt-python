"""Wrapper for API calls using requests"""

import http.client
import json as json_
import os
import typing
import urllib.request


try:
    import certifi
except ImportError:
    pass
else:
    os.putenv("SSL_CERT_FILE", certifi.where())

from .exceptions import AuthError


BASE_URL = "https://felt.com/api/v2/"


def make_request(
    url: str,
    method: typing.Literal["GET", "POST", "PATCH", "DELETE"],
    json: dict | None = None,
    api_token: str | None = None,
) -> http.client.HTTPResponse:
    """Basic wrapper for requests that adds auth"""
    if not api_token:
        try:
            api_token = os.environ["FELT_API_TOKEN"]
        except KeyError as exc:
            raise AuthError(
                "No API token found. Pass explicitly or set the FELT_API_TOKEN environment variable"
            ) from exc

    data, headers = None, {"Authorization": f"Bearer {api_token}"}
    if json is not None:
        data = json_.dumps(json).encode("utf8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    return urllib.request.urlopen(request)
