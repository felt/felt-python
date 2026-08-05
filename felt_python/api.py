"""Wrapper for API calls using requests"""

import http.client
import json as json_
import os
import typing
import urllib.parse
import urllib.request
from importlib.metadata import version, PackageNotFoundError

try:
    import certifi
except ImportError:
    pass
else:
    os.putenv("SSL_CERT_FILE", certifi.where())

from .exceptions import AuthError


BASE_URL = os.getenv("FELT_BASE_URL", "https://felt.com/api/v2/")


def build_url(template: str, **path_params) -> str:
    """Fill a URL template, percent-encoding each value as one path segment.

    Ids reach these functions from user code, config files and other API
    responses, so they cannot be assumed URL-safe. Interpolating them directly
    means an id containing a space raises http.client.InvalidURL before the
    request is sent, and one containing "?", "#" or "/" silently changes the
    path or query the server sees. Encoding each value with safe="" keeps a
    bad id a plain 404.

        >>> build_url(BASE_URL + "maps/{map_id}", map_id="a b/c")
        'https://felt.com/api/v2/maps/a%20b%2Fc'
    """
    return template.format(
        **{
            key: urllib.parse.quote(str(value), safe="")
            for key, value in path_params.items()
        }
    )


def build_query(url: str, **params) -> str:
    """Append a percent-encoded query string, skipping None values."""
    present = {key: value for key, value in params.items() if value is not None}
    if not present:
        return url
    separator = "&" if "?" in url else "?"
    return f"{url}{separator}{urllib.parse.urlencode(present)}"


def make_request(
    url: str,
    method: typing.Literal["GET", "POST", "PATCH", "DELETE"],
    json: dict | list | None = None,
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

    try:
        package_version = version("felt_python")
    except PackageNotFoundError:
        package_version = "local"

    data, headers = (
        None,
        {
            "Authorization": f"Bearer {api_token}",
            "User-Agent": f"felt-python/{package_version}",
        },
    )
    if json is not None:
        data = json_.dumps(json).encode("utf8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    return urllib.request.urlopen(request)
