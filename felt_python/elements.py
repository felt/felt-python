"""Elements and element groups"""

import json

from urllib.parse import urljoin

from .api import make_request, BASE_URL
from .util import deprecated


ELEMENTS = urljoin(BASE_URL, "maps/{map_id}/elements")
ELEMENT = urljoin(BASE_URL, "maps/{map_id}/elements/{element_id}")
ELEMENT_GROUPS = urljoin(BASE_URL, "maps/{map_id}/element_groups")
ELEMENT_GROUP = urljoin(BASE_URL, "maps/{map_id}/element_groups/{element_group_id}")


def list_elements(map_id: str, api_token: str | None = None):
    """List all elements on a map

    Args:
        map_id: The ID of the map to list elements from
        api_token: Optional API token

    Returns:
        GeoJSON FeatureCollection of all elements
    """
    response = make_request(
        url=ELEMENTS.format(map_id=map_id),
        method="GET",
        api_token=api_token,
    )
    return json.load(response)


def list_element_groups(map_id: str, api_token: str | None = None):
    """List all element groups on a map

    Args:
        map_id: The ID of the map to list element groups from
        api_token: Optional API token

    Returns:
        List of element groups
    """
    response = make_request(
        url=ELEMENT_GROUPS.format(map_id=map_id),
        method="GET",
        api_token=api_token,
    )
    return json.load(response)


def get_element_group(map_id: str, element_group_id: str, api_token: str | None = None):
    """Get contents of an element group

    Args:
        map_id: The ID of the map containing the group
        element_group_id: The ID of the element group to list elements from
        api_token: Optional API token

    Returns:
        GeoJSON FeatureCollection of all elements in the group
    """
    response = make_request(
        url=ELEMENT_GROUP.format(map_id=map_id, element_group_id=element_group_id),
        method="GET",
        api_token=api_token,
    )
    return json.load(response)


@deprecated(reason="Please use `get_element_group` instead")
def list_elements_in_group(
    map_id: str, element_group_id: str, api_token: str | None = None
):
    get_element_group(map_id, element_group_id, api_token)


@deprecated(reason="Please use `upsert_elements` instead")
def post_elements(
    map_id: str, geojson_feature_collection: dict | str, api_token: str | None = None
):
    upsert_elements(map_id, geojson_feature_collection, api_token)


def upsert_elements(
    map_id: str, geojson_feature_collection: dict | str, api_token: str | None = None
):
    """Create elements

    Each GeoJSON Feature represents an element. If a feature has an existing ID,
    that element will be updated. If a feature does not have an ID (or the one it
    has does not exist), a new element will be created.

    Args:
        map_id: The ID of the map to create or update elements on
        geojson_feature_collection: GeoJSON FeatureCollection as dict or JSON string
        api_token: Optional API token

    Returns:
        GeoJSON FeatureCollection of the created or updated elements
    """
    if isinstance(geojson_feature_collection, str):
        geojson_feature_collection = json.loads(geojson_feature_collection)
    response = make_request(
        url=ELEMENTS.format(map_id=map_id),
        method="POST",
        json=geojson_feature_collection,
        api_token=api_token,
    )
    return json.load(response)


def delete_element(map_id: str, element_id: str, api_token: str | None = None):
    """Delete an element

    Args:
        map_id: The ID of the map containing the element
        element_id: The ID of the element to delete
        api_token: Optional API token
    """
    make_request(
        url=ELEMENT.format(map_id=map_id, element_id=element_id),
        method="DELETE",
        api_token=api_token,
    )


@deprecated(reason="Please use `upsert_element_groups` instead")
def post_element_group(
    map_id: str,
    json_element: dict | str,
    api_token: str | None = None,
):
    upsert_element_groups(map_id, json_element, api_token)


def upsert_element_groups(
    map_id: str,
    element_groups: list[dict[str, str]],
    api_token: str | None = None,
):
    """Post multiple element groups

    Args:
        map_id: The ID of the map to create the element groups on
        element_groups: List of element group objects
        api_token: Optional API token

    Returns:
        The created or updated element groups
    """
    response = make_request(
        url=ELEMENT_GROUPS.format(map_id=map_id),
        method="POST",
        json=element_groups,
        api_token=api_token,
    )
    return json.load(response)
