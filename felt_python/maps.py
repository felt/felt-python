"""Maps"""

import requests

from .api import make_request, MAPS_TEMPLATE


def create_map(api_token: str | None = None, **json_args):
    """Create a new Felt map"""
    response = make_request(
        url=MAPS_TEMPLATE.expand(),
        method=requests.post,
        json=json_args,
        api_token=api_token,
    )
    return response.json()["data"]


def delete_map(map_id: str, api_token: str | None = None):
    """Delete a map"""
    response = make_request(
        url=MAPS_TEMPLATE.expand(map_id=map_id),
        method=requests.delete,
        api_token=api_token,
    )


def get_map_details(map_id: str, api_token: str | None = None):
    """Get details of a map"""
    response = make_request(
        url=MAPS_TEMPLATE.expand(map_id=map_id),
        method=requests.get,
        api_token=api_token,
    )
    return response.json()["data"]


def update_map(map_id: str, new_title: str, api_token: str | None = None):
    """Update a map's details (title only for now)"""
    response = make_request(
        url=MAPS_TEMPLATE.expand(map_id=map_id),
        method=requests.patch,
        json={"title": new_title},
        api_token=api_token,
    )
    return response.json()["data"]
