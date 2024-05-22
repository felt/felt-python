"""Elements and element groups"""
import json

import requests

from .api import (
    make_request,
    ELEMENTS_TEMPLATE,
    ELEMENT_GROUPS_TEMPLATE,
)


def list_elements(map_id: str, api_token: str | None = None):
    """List all elements on a map"""
    response = make_request(
        url=ELEMENTS_TEMPLATE.expand(map_id=map_id),
        method=requests.get,
        api_token=api_token,
    )
    return response.json()["data"]


def list_element_groups(map_id: str, api_token: str | None = None):
    """List all element groups on a map"""
    response = make_request(
        url=ELEMENT_GROUPS_TEMPLATE.expand(map_id=map_id),
        method=requests.get,
        api_token=api_token,
    )
    return response.json()["data"]


def list_elements_in_group(
    map_id: str, element_group_id: str, api_token: str | None = None
):
    """List all elements in a group"""
    response = make_request(
        url=ELEMENT_GROUPS_TEMPLATE.expand(
            map_id=map_id, element_group_id=element_group_id
        ),
        method=requests.get,
        api_token=api_token,
    )
    return response.json()["data"]


def post_elements(map_id: str, geojson_feature_collection: dict | str):
    """Post a GeoJSON FeatureCollection

    Each GeoJSON Feature represents an element. If a feature has an existing ID,
    that element will be updated. If a feature does not have an ID (or the one it
    has does not exist), a new element will be created.
    """
    if isinstance(geojson_feature_collection, str):
        geojson_feature_collection = json.loads(geojson_feature_collection)
    response = make_request(
        url=ELEMENTS_TEMPLATE.expand(map_id=map_id),
        method=requests.post,
        json=geojson_feature_collection,
    )
    return response.json()["data"]


def delete_element(map_id: str, element_id: str):
    """Delete an element"""
    make_request(
        url=ELEMENTS_TEMPLATE.expand(map_id=map_id, element_id=element_id),
        method=requests.delete,
    )
