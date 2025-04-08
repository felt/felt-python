"""Layer groups"""

import json
from typing import Dict, Any, List, Union, Optional

from urllib.parse import urljoin

from .api import make_request, BASE_URL


MAP_LAYER_GROUPS_TEMPLATE = urljoin(BASE_URL, "maps/{map_id}/layer_groups/")
LAYER_GROUP_TEMPLATE = urljoin(MAP_LAYER_GROUPS_TEMPLATE, "{layer_group_id}")
PUBLISH_LAYER_GROUP_TEMPLATE = urljoin(LAYER_GROUP_TEMPLATE, "/publish")


def list_layer_groups(map_id: str, api_token: str | None = None):
    """List layer groups on a map

    Args:
        map_id: The ID of the map to list layer groups from
        api_token: Optional API token

    Returns:
        List of layer groups
    """
    response = make_request(
        url=MAP_LAYER_GROUPS_TEMPLATE.format(map_id=map_id),
        method="GET",
        api_token=api_token,
    )
    return json.load(response)


def get_layer_group_details(
    map_id: str,
    layer_group_id: str,
    api_token: str | None = None,
):
    """Get details of a layer group

    Args:
        map_id: The ID of the map containing the layer group
        layer_group_id: The ID of the layer group to get details for
        api_token: Optional API token

    Returns:
        Layer group details
    """
    response = make_request(
        url=LAYER_GROUP_TEMPLATE.format(
            map_id=map_id,
            layer_group_id=layer_group_id,
        ),
        method="GET",
        api_token=api_token,
    )
    return json.load(response)


def update_layer_groups(
    map_id: str,
    layer_group_params_list: List[Dict[str, Any]],
    api_token: str | None = None,
):
    """Update multiple layer groups at once

    Args:
        map_id: The ID of the map containing the layer groups
        layer_group_params_list: List of layer group parameters to update
                               Each dict must contain at least "name" key
                               Optional keys include "id", "caption", "ordering_key"
        api_token: Optional API token

    Returns:
        The updated layer groups
    """
    response = make_request(
        url=MAP_LAYER_GROUPS_TEMPLATE.format(map_id=map_id),
        method="POST",
        json=layer_group_params_list,
        api_token=api_token,
    )
    return json.load(response)


def delete_layer_group(
    map_id: str,
    layer_group_id: str,
    api_token: str | None = None,
):
    """Delete a layer group from a map

    Args:
        map_id: The ID of the map containing the layer group
        layer_group_id: The ID of the layer group to delete
        api_token: Optional API token
    """
    make_request(
        url=LAYER_GROUP_TEMPLATE.format(
            map_id=map_id,
            layer_group_id=layer_group_id,
        ),
        method="DELETE",
        api_token=api_token,
    )


def publish_layer_group(
    map_id: str,
    layer_group_id: str,
    name: str = None,
    api_token: str | None = None,
):
    """Publish a layer group to the Felt library

    Args:
        map_id: The ID of the map containing the layer group
        layer_group_id: The ID of the layer group to publish
        name: Optional name to publish the layer group under
        api_token: Optional API token

    Returns:
        The published layer group
    """
    json_payload = {}
    if name is not None:
        json_payload["name"] = name

    response = make_request(
        url=PUBLISH_LAYER_GROUP_TEMPLATE.format(
            map_id=map_id,
            layer_group_id=layer_group_id,
        ),
        method="POST",
        json=json_payload,
        api_token=api_token,
    )
    return json.load(response)
