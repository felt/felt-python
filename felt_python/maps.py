"""Maps"""

import json

from urllib.parse import urljoin

from .api import make_request, BASE_URL
from .util import deprecated


MAPS = urljoin(BASE_URL, "maps")
MAP = urljoin(BASE_URL, "maps/{map_id}")
MAP_UPDATE = urljoin(BASE_URL, "maps/{map_id}/update")
MAP_MOVE = urljoin(BASE_URL, "maps/{map_id}/move")
MAP_EMBED_TOKEN = urljoin(BASE_URL, "maps/{map_id}/embed_token")
MAP_ADD_SOURCE_LAYER = urljoin(BASE_URL, "maps/{map_id}/add_source_layer")
MAP_DUPLICATE = urljoin(BASE_URL, "maps/{map_id}/duplicate")


def create_map(
    title: str | None = None,
    description: str | None = None,
    public_access: str | None = None,
    basemap: str | None = None,
    lat: float | None = None,
    lon: float | None = None,
    zoom: float | None = None,
    layer_urls: list[str] | None = None,
    workspace_id: str | None = None,
    api_token: str | None = None,
):
    """Create a new Felt map

    Args:
        title: The title to be used for the map. Defaults to "Untitled Map"
        description: A description to display in the map legend
        public_access: The level of access to grant to the map.
            Options are "private", "view_only", "view_and_comment",
            or "view_comment_and_edit". Defaults to "view_only".
        basemap: The basemap to use for the new map. Defaults to "default".
            Valid values are "default", "light", "dark", "satellite",
            a valid raster tile URL with {x}, {y}, and {z} parameters,
            or a hex color string like #ff0000.
        lat: If no data has been uploaded to the map, the initial latitude
            to center the map display on.
        lon: If no data has been uploaded to the map, the initial longitude
            to center the map display on.
        zoom: If no data has been uploaded to the map, the initial zoom level
            for the map to display.
        layer_urls: An array of urls to use to create layers in the map.
            Only tile URLs for raster layers are supported at the moment.
        workspace_id: The workspace to create the map in.
            Defaults to the latest used workspace.
        api_token: Optional API token

    Returns:
        The created map
    """
    json_args: dict = {}

    if title is not None:
        json_args["title"] = title
    if description is not None:
        json_args["description"] = description
    if public_access is not None:
        json_args["public_access"] = public_access
    if basemap is not None:
        json_args["basemap"] = basemap
    if lat is not None:
        json_args["lat"] = lat
    if lon is not None:
        json_args["lon"] = lon
    if zoom is not None:
        json_args["zoom"] = zoom
    if layer_urls is not None:
        json_args["layer_urls"] = layer_urls
    if workspace_id is not None:
        json_args["workspace_id"] = workspace_id

    response = make_request(
        url=MAPS,
        method="POST",
        json=json_args,
        api_token=api_token,
    )
    return json.load(response)


def delete_map(map_id: str, api_token: str | None = None):
    """Delete a map"""
    make_request(
        url=MAP.format(map_id=map_id),
        method="DELETE",
        api_token=api_token,
    )


def get_map(map_id: str, api_token: str | None = None):
    """Get details of a map"""
    response = make_request(
        url=MAP.format(map_id=map_id),
        method="GET",
        api_token=api_token,
    )
    return json.load(response)


@deprecated(reason="Please use `get_map` instead")
def get_map_details(map_id: str, api_token: str | None = None):
    get_map(map_id, api_token)


def update_map(
    map_id: str,
    title: str | None = None,
    description: str | None = None,
    public_access: str | None = None,
    basemap: str | None = None,
    table_settings: dict | None = None,
    viewer_permissions: dict | None = None,
    api_token: str | None = None,
):
    """Update a map's details

    Args:
        map_id: The ID of the map to update
        title: Optional new title for the map
        description: Optional new description for the map
        public_access: Optional new public access setting
            Options are "private", "view_only", "view_and_comment",
            or "view_comment_and_edit"
        basemap: The basemap to use for the map. Defaults to "default".
            Valid values are "default", "light", "dark", "satellite",
            a valid raster tile URL with {x}, {y}, and {z} parameters,
            or a hex color string like #ff0000.
        table_settings: Optional data table settings
            Dict with keys:
            - "default_table_layer_id": str | None - The layer ID to open by default in table view
            - "viewers_can_open_table": bool - Whether viewers can open the data table
        viewer_permissions: Optional viewer permission settings
            Dict with keys:
            - "can_duplicate_map": bool - Whether viewers can duplicate the map and data
            - "can_export_data": bool - Whether viewers can export map data
            - "can_see_map_presence": bool - Whether viewers can see who else is viewing the map
        api_token: Optional API token

    Returns:
        The updated map
    """
    json_args: dict = {}
    if title is not None:
        json_args["title"] = title
    if description is not None:
        json_args["description"] = description
    if public_access is not None:
        json_args["public_access"] = public_access
    if basemap is not None:
        json_args["basemap"] = basemap
    if table_settings is not None:
        json_args["table_settings"] = table_settings
    if viewer_permissions is not None:
        json_args["viewer_permissions"] = viewer_permissions

    response = make_request(
        url=MAP_UPDATE.format(map_id=map_id),
        method="POST",
        json=json_args,
        api_token=api_token,
    )
    return json.load(response)


def move_map(
    map_id: str,
    project_id: str | None = None,
    folder_id: str | None = None,
    api_token: str | None = None,
):
    """Move a map to a different project or folder

    Args:
        map_id: The ID of the map to move
        project_id: The ID of the project to move the map to (mutually exclusive with folder_id)
        folder_id: The ID of the folder to move the map to (mutually exclusive with project_id)
        api_token: Optional API token

    Returns:
        The moved map
    """
    if project_id is not None and folder_id is not None:
        raise ValueError("Cannot specify both project_id and folder_id")
    if project_id is None and folder_id is None:
        raise ValueError("Must specify either project_id or folder_id")

    json_args = {}
    if project_id is not None:
        json_args["project_id"] = project_id
    if folder_id is not None:
        json_args["folder_id"] = folder_id

    response = make_request(
        url=MAP_MOVE.format(map_id=map_id),
        method="POST",
        json=json_args,
        api_token=api_token,
    )
    return json.load(response)


def create_embed_token(
    map_id: str, user_email: str | None = None, api_token: str | None = None
):
    """Create an embed token for a map

    Args:
        map_id: The ID of the map to create an embed token for
        user_email: Optionally assign the token to a user email address.
            Providing an email will enable the viewer to export data
            if the Map allows it.
        api_token: Optional API token

    Returns:
        The created embed token with expiration time
    """
    url = MAP_EMBED_TOKEN.format(map_id=map_id)
    if user_email:
        url = f"{url}?user_email={user_email}"

    response = make_request(
        url=url,
        method="POST",
        api_token=api_token,
    )
    return json.load(response)


def add_source_layer(
    map_id: str, source_layer_params: dict[str, str], api_token: str | None = None
):
    """Add a layer from a source to a map

    Args:
        map_id: The ID of the map to add the layer to
        source_layer_params: Parameters defining the source layer to add.
            Must include "from" key with one of these values:
            - "dataset": requires "dataset_id"
            - "sql": requires "source_id" and "query"
            - "stac": requires "source_id" and "stac_asset_url"
        api_token: Optional API token

    Returns:
        Acceptance status and links to the created resources
    """
    response = make_request(
        url=MAP_ADD_SOURCE_LAYER.format(map_id=map_id),
        method="POST",
        json=source_layer_params,
        api_token=api_token,
    )
    return json.load(response)


def duplicate_map(
    map_id: str,
    title: str | None = None,
    project_id: str | None = None,
    folder_id: str | None = None,
    api_token: str | None = None,
):
    """Duplicate a map

    Args:
        map_id: The ID of the map to duplicate
        title: Optional title for the duplicated map
        project_id: The ID of the project to place the duplicated map in
            (mutually exclusive with folder_id)
        folder_id: The ID of the folder to place the duplicated map in
            (mutually exclusive with project_id)
        api_token: Optional API token

    Returns:
        The duplicated map
    """
    if project_id is not None and folder_id is not None:
        raise ValueError("Cannot specify both project_id and folder_id")

    json_args: dict = {}
    if title is not None:
        json_args["title"] = title

    if project_id is not None:
        json_args["destination"] = {"project_id": project_id}
    elif folder_id is not None:
        json_args["destination"] = {"folder_id": folder_id}

    response = make_request(
        url=MAP_DUPLICATE.format(map_id=map_id),
        method="POST",
        json=json_args,
        api_token=api_token,
    )
    return json.load(response)
