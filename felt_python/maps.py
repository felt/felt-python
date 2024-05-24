"""Maps"""

import json

from .api import make_request, MAPS_TEMPLATE


def create_map(api_token: str | None = None, **json_args):
    """Create a new Felt map"""
    response = make_request(
        url=MAPS_TEMPLATE.expand(),
        method="POST",
        json=json_args,
        api_token=api_token,
    )
    return json.load(response)


def delete_map(map_id: str, api_token: str | None = None):
    """Delete a map"""
    make_request(
        url=MAPS_TEMPLATE.expand(map_id=map_id),
        method="DELETE",
        api_token=api_token,
    )


def get_map_details(map_id: str, api_token: str | None = None):
    """Get details of a map"""
    response = make_request(
        url=MAPS_TEMPLATE.expand(map_id=map_id),
        method="GET",
        api_token=api_token,
    )
    return json.load(response)["data"]


def update_map(map_id: str, new_title: str, api_token: str | None = None):
    """Update a map's details (title only for now)"""
    response = make_request(
        url=MAPS_TEMPLATE.expand(map_id=map_id),
        method="PATCH",
        json={"title": new_title},
        api_token=api_token,
    )
    return json.load(response)["data"]
