import os
import requests
import typing

from urllib.parse import urljoin

from uritemplate import URITemplate

from .exceptions import AuthError


V1_URL = "https://felt.com/api/v1/"
V2_URL = "https://felt.com/api/v2/"
MAPS_TEMPLATE = URITemplate(urljoin(V2_URL, "maps{/map_id}"))
LAYERS_TEMPLATE = URITemplate(urljoin(V1_URL, "maps{/map_id}/layers{/layer_id}"))
UPLOAD_TEMPLATE = URITemplate(urljoin(V2_URL, "maps{/map_id}/upload"))
URL_IMPORT_TEMPLATE = URITemplate(urljoin(V1_URL, "maps{/map_id}/layers/url_import"))
REFRESH_FILE_TEMPLATE = URITemplate(
    urljoin(V1_URL, "maps{/map_id}/refresh{/layer_id}/file")
)
REFRESH_URL_TEMPLATE = URITemplate(
    urljoin(V1_URL, "maps{/map_id}/refresh{/layer_id}/url")
)
LAYER_STYLE_TEMPLATE = URITemplate(
    urljoin(V1_URL, "maps{/map_id}/layers{/layer_id}/style")
)


def make_request(
    url: str,
    method: typing.Union[requests.get, requests.post, requests.patch, requests.delete],
    params: dict | None = None,
    json: dict | None = None,
    api_token: str | None = None,
):
    """Basic wrapper for requests that adds auth"""
    if not api_token:
        try:
            api_token = os.environ["FELT_API_TOKEN"]
        except KeyError:
            raise AuthError(
                "No API token found. Pass explicitly or set the FELT_API_TOKEN environment variable"
            )

    headers = {"Authorization": f"Bearer {api_token}"}
    response = method(url, params=params, json=json, headers=headers)
    if not response.ok:
        raise Exception(f"Request failed: {response.content}")
    return response
