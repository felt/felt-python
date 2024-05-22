"""Wrapper for API calls using requests"""
import os
import typing

from urllib.parse import urljoin

import requests

from uritemplate import URITemplate

from .exceptions import AuthError


BASE_URL = "https://felt.com/api/v2/"
MAPS_TEMPLATE = URITemplate(urljoin(BASE_URL, "maps{/map_id}"))
LAYERS_TEMPLATE = URITemplate(urljoin(BASE_URL, "maps{/map_id}/layers{/layer_id}"))
UPLOAD_TEMPLATE = URITemplate(urljoin(BASE_URL, "maps{/map_id}/upload"))
REFRESH_TEMPLATE = URITemplate(
    urljoin(BASE_URL, "maps{/map_id}/layers{/layer_id}/refresh")
)
UPDATE_STYLE_TEMPLATE = URITemplate(
    urljoin(BASE_URL, "maps{/map_id}/layers{/layer_id}/update_style")
)
ELEMENTS_TEMPLATE = URITemplate(
    urljoin(BASE_URL, "maps{/map_id}/elements{/element_id}")
)
ELEMENT_GROUPS_TEMPLATE = URITemplate(
    urljoin(BASE_URL, "maps{/map_id}/element_groups{/element_group_id}")
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
        except KeyError as exc:
            raise AuthError(
                "No API token found. Pass explicitly or set the FELT_API_TOKEN environment variable"
            ) from exc

    headers = {"Authorization": f"Bearer {api_token}"}
    response = method(url, params=params, json=json, headers=headers)
    if not response.ok:
        raise Exception(f"Request failed: {response.content}")
    return response
