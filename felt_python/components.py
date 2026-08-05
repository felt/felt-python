"""Layer components"""

import json

from urllib.parse import urljoin

from .api import make_request, BASE_URL


COMPONENTS = urljoin(BASE_URL, "maps/{map_id}/layers/{layer_id}/components")
COMPONENT = urljoin(
    BASE_URL, "maps/{map_id}/layers/{layer_id}/components/{component_id}"
)


def list_layer_components(map_id: str, layer_id: str, api_token: str | None = None):
    """List all components on a layer

    Args:
        map_id: The ID of the map containing the layer
        layer_id: The ID of the layer to list components from
        api_token: Optional API token

    Returns:
        List of layer components
    """
    response = make_request(
        url=COMPONENTS.format(map_id=map_id, layer_id=layer_id),
        method="GET",
        api_token=api_token,
    )
    return json.load(response)


def create_layer_component(
    map_id: str,
    layer_id: str,
    component_type: str,
    data: dict,
    title: str | None = None,
    config: dict | None = None,
    api_token: str | None = None,
):
    """Create a component on a layer

    Args:
        map_id: The ID of the map containing the layer
        layer_id: The ID of the layer to create the component on
        component_type: The type of component to create. Immutable after
            creation. Options are "statistic", "histogram", "bar_chart",
            "time_series", or "filter".
        data: How the component computes its result. The expected shape
            depends on the component type. For example, a "statistic"
            component takes either a feature count
            ({"aggregate": "count"}) or an attribute aggregation
            ({"aggregate": "avg", "aggregate_by": "some_attribute"}).
        title: Optional display title (max 256 characters)
        config: Optional component configuration. Common keys include
            "reactive" (whether the component reacts to other components'
            selections) and "viewport_mode" ("global" or "viewport").
        api_token: Optional API token

    Returns:
        The created layer component
    """
    json_payload: dict = {"type": component_type, "data": data}
    if title is not None:
        json_payload["title"] = title
    if config is not None:
        json_payload["config"] = config

    response = make_request(
        url=COMPONENTS.format(map_id=map_id, layer_id=layer_id),
        method="POST",
        json=json_payload,
        api_token=api_token,
    )
    return json.load(response)


def get_layer_component(
    map_id: str,
    layer_id: str,
    component_id: str,
    api_token: str | None = None,
):
    """Get details of a layer component

    Args:
        map_id: The ID of the map containing the layer
        layer_id: The ID of the layer containing the component
        component_id: The ID of the component to get details for
        api_token: Optional API token

    Returns:
        Layer component details
    """
    response = make_request(
        url=COMPONENT.format(
            map_id=map_id, layer_id=layer_id, component_id=component_id
        ),
        method="GET",
        api_token=api_token,
    )
    return json.load(response)


def update_layer_component(
    map_id: str,
    layer_id: str,
    component_id: str,
    data: dict | None = None,
    title: str | None = None,
    config: dict | None = None,
    api_token: str | None = None,
):
    """Update a layer component

    The component's type is immutable after creation.

    Args:
        map_id: The ID of the map containing the layer
        layer_id: The ID of the layer containing the component
        component_id: The ID of the component to update
        data: Optionally change how the component computes its result.
            Replaces the current value as a unit when provided; partial
            updates are not supported.
        title: Optional new display title (max 256 characters)
        config: Optional component configuration updates. Provided keys are
            updated; omitted keys keep their current value.
        api_token: Optional API token

    Returns:
        The updated layer component
    """
    json_payload: dict = {}
    if data is not None:
        json_payload["data"] = data
    if title is not None:
        json_payload["title"] = title
    if config is not None:
        json_payload["config"] = config

    response = make_request(
        url=COMPONENT.format(
            map_id=map_id, layer_id=layer_id, component_id=component_id
        ),
        method="POST",
        json=json_payload,
        api_token=api_token,
    )
    return json.load(response)


def delete_layer_component(
    map_id: str,
    layer_id: str,
    component_id: str,
    api_token: str | None = None,
):
    """Delete a component from a layer

    Args:
        map_id: The ID of the map containing the layer
        layer_id: The ID of the layer containing the component
        component_id: The ID of the component to delete
        api_token: Optional API token
    """
    make_request(
        url=COMPONENT.format(
            map_id=map_id, layer_id=layer_id, component_id=component_id
        ),
        method="DELETE",
        api_token=api_token,
    )
