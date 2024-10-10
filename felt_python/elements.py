"""Elements and element groups"""

import json

from urllib.parse import urljoin

from .api import make_request, BASE_URL


MAP_ELEMENTS_TEMPLATE = urljoin(BASE_URL, "maps/{map_id}/elements/")
ELEMENT_TEMPLATE = urljoin(MAP_ELEMENTS_TEMPLATE, "{element_id}")
MAP_ELEMENT_GROUPS_TEMPLATE = urljoin(BASE_URL, "maps/{map_id}/element_groups/")
ELEMENT_GROUP_TEMPLATE = urljoin(MAP_ELEMENT_GROUPS_TEMPLATE, "{element_group_id}")


def list_elements(map_id: str, api_token: str | None = None):
    """List all elements on a map"""
    response = make_request(
        url=MAP_ELEMENTS_TEMPLATE.format(map_id=map_id),
        method="GET",
        api_token=api_token,
    )
    return json.load(response)


def list_element_groups(map_id: str, api_token: str | None = None):
    """List all element groups on a map"""
    response = make_request(
        url=MAP_ELEMENT_GROUPS_TEMPLATE.format(map_id=map_id),
        method="GET",
        api_token=api_token,
    )
    return json.load(response)


def list_elements_in_group(
    map_id: str, element_group_id: str, api_token: str | None = None
):
    """List all elements in a group"""
    response = make_request(
        url=ELEMENT_GROUP_TEMPLATE.format(
            map_id=map_id, element_group_id=element_group_id
        ),
        method="GET",
        api_token=api_token,
    )
    return json.load(response)


def post_elements(map_id: str, geojson_feature_collection: dict | str):
    """Post a GeoJSON FeatureCollection

    Each GeoJSON Feature represents an element. If a feature has an existing ID,
    that element will be updated. If a feature does not have an ID (or the one it
    has does not exist), a new element will be created.
    """
    if isinstance(geojson_feature_collection, str):
        geojson_feature_collection = json.loads(geojson_feature_collection)
    response = make_request(
        url=MAP_ELEMENTS_TEMPLATE.format(map_id=map_id),
        method="POST",
        json=geojson_feature_collection,
    )
    return json.load(response)


def delete_element(map_id: str, element_id: str):
    """Delete an element"""
    make_request(
        url=ELEMENT_TEMPLATE.format(map_id=map_id, element_id=element_id),
        method="DELETE",
    )


def post_element_group(
    map_id: str,
    json_element: dict | str,
    api_token: str | None = None,
):
    """Post a new element group"""
    response = make_request(
        url=MAP_ELEMENT_GROUPS_TEMPLATE.format(map_id=map_id),
        method="POST",
        json=json_element,
        api_token=api_token,
    )
    return json.load(response)
