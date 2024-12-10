"""Maps"""

import json

from urllib.parse import urljoin

from .api import make_request, BASE_URL


MAPS_ENDPOINT = urljoin(BASE_URL, "maps/")
MAP_TEMPLATE = urljoin(MAPS_ENDPOINT, "{map_id}/")
MAP_UPDATE_TEMPLATE = urljoin(MAPS_ENDPOINT, "{map_id}/update")
MAP_MOVE_TEMPLATE = urljoin(MAPS_ENDPOINT, "{map_id}/move")


def create_map(api_token: str | None = None, **json_args):
    """Create a new Felt map"""
    response = make_request(
        url=MAPS_ENDPOINT,
        method="POST",
        json=json_args,
        api_token=api_token,
    )
    return json.load(response)


def delete_map(map_id: str, api_token: str | None = None):
    """Delete a map"""
    make_request(
        url=MAP_TEMPLATE.format(map_id=map_id),
        method="DELETE",
        api_token=api_token,
    )


def get_map_details(map_id: str, api_token: str | None = None):
    """Get details of a map"""
    response = make_request(
        url=MAP_TEMPLATE.format(map_id=map_id),
        method="GET",
        api_token=api_token,
    )
    return json.load(response)


def update_map(map_id: str, new_title: str, api_token: str | None = None):
    """Update a map's details (title only for now)"""
    response = make_request(
        url=MAP_UPDATE_TEMPLATE.format(map_id=map_id),
        method="POST",
        json={"title": new_title},
        api_token=api_token,
    )
    return json.load(response)


def move_map(map_id: str, project_id: str, api_token: str | None = None):
    """Move a map to a different project"""
    response = make_request(
        url=MAP_MOVE_TEMPLATE.format(map_id=map_id),
        method="POST",
        json={"project_id": project_id},
        api_token=api_token,
    )
    return json.load(response)
