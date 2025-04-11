"""Layers"""

import io
import json
import os
import tempfile
import typing
import urllib.request
import uuid
import typing

from urllib.parse import urljoin

from .api import make_request, BASE_URL
from .util import deprecated


LAYERS = urljoin(BASE_URL, "maps/{map_id}/layers")
LAYER = urljoin(BASE_URL, "maps/{map_id}/layers/{layer_id}")
LAYER_REFRESH = urljoin(BASE_URL, "maps/{map_id}/layers/{layer_id}/refresh")
LAYER_UPDATE_STYLE = urljoin(BASE_URL, "maps/{map_id}/layers/{layer_id}/update_style")
LAYER_UPLOAD = urljoin(BASE_URL, "maps/{map_id}/upload")
LAYER_EXPORT_LINK = urljoin(BASE_URL, "maps/{map_id}/layers/{layer_id}/get_export_link")
LAYER_PUBLISH = urljoin(BASE_URL, "maps/{map_id}/layers/{layer_id}/publish")
LAYER_CUSTOM_EXPORT = urljoin(BASE_URL, "maps/{map_id}/layers/{layer_id}/custom_export")
LAYER_CUSTOM_EXPORT_STATUS = urljoin(
    BASE_URL, "maps/{map_id}/layers/{layer_id}/custom_exports/{export_id}"
)
LAYER_DUPLICATE = urljoin(BASE_URL, "duplicate_layers")


def list_layers(map_id: str, api_token: str | None = None):
    """List layers on a map"""
    response = make_request(
        url=LAYERS.format(map_id=map_id),
        method="GET",
        api_token=api_token,
    )
    return json.load(response)


def upload_file(
    map_id: str,
    file_name: str,
    layer_name: str,
    metadata: dict[str, str] = None,
    hints: list[dict[str, str]] = None,
    lat: float = None,
    lng: float = None,
    zoom: float = None,
    api_token: str | None = None,
):
    """Upload a file to a Felt map

    Args:
        map_id: The ID of the map to upload to
        file_name: The path to the file to upload
        layer_name: The display name for the new layer
        metadata: Optional metadata for the layer
        hints: Optional list of hints for interpreting the data in the upload
        lat: Optional latitude of the image center (image uploads only)
        lng: Optional longitude of the image center (image uploads only)
        zoom: Optional zoom level of the image (image uploads only)
        api_token: Optional API token

    Returns:
        The upload response including layer ID and presigned upload details
    """
    json_payload = {"name": layer_name}

    if metadata is not None:
        json_payload["metadata"] = metadata
    if hints is not None:
        json_payload["hints"] = hints
    if lat is not None:
        json_payload["lat"] = lat
    if lng is not None:
        json_payload["lng"] = lng
    if zoom is not None:
        json_payload["zoom"] = zoom

    response = make_request(
        url=LAYER_UPLOAD.format(map_id=map_id),
        method="POST",
        api_token=api_token,
        json=json_payload,
    )

    return _upload_file(json.load(response), file_name)


def upload_dataframe(
    map_id: str,
    dataframe: "pd.DataFrame",
    layer_name: str,
    metadata: dict[str, str] = None,
    hints: list[dict[str, str]] = None,
    api_token: str | None = None,
):
    """Upload a Pandas DataFrame to a Felt map"""
    with tempfile.TemporaryDirectory() as tempdir:
        file_name = os.path.join(tempdir, "dataframe.csv")
        dataframe.to_csv(file_name)
        return upload_file(
            map_id,
            file_name,
            layer_name,
            metadata=metadata,
            hints=hints,
            api_token=api_token,
        )


def upload_geodataframe(
    map_id: str,
    geodataframe: "gpd.GeoDataFrame",
    layer_name: str,
    metadata: dict[str, str] = None,
    hints: list[dict[str, str]] = None,
    api_token: str | None = None,
):
    """Upload a GeoPandas GeoDataFrame to a Felt map"""
    with tempfile.TemporaryDirectory() as tempdir:
        file_name = os.path.join(tempdir, "geodataframe.gpkg")
        geodataframe.to_file(file_name)
        return upload_file(
            map_id,
            file_name,
            layer_name,
            metadata=metadata,
            hints=hints,
            api_token=api_token,
        )


def refresh_file_layer(
    map_id: str, layer_id: str, file_name: str, api_token: str | None = None
):
    """Refresh a layer originated from a file upload

    Args:
        map_id: The ID of the map containing the layer
        layer_id: The ID of the layer to refresh
        file_name: The path to the file to upload as the new data
        api_token: Optional API token

    Returns:
        The refresh response including presigned upload details
    """
    response = make_request(
        url=LAYER_REFRESH.format(map_id=map_id, layer_id=layer_id),
        method="POST",
        api_token=api_token,
    )
    return _upload_file(json.load(response), file_name)


def upload_url(
    map_id: str,
    layer_url: str,
    layer_name: str,
    metadata: dict[str, str] = None,
    hints: list[dict[str, str]] = None,
    api_token: str | None = None,
):
    """Upload a URL to a Felt map

    Args:
        map_id: The ID of the map to upload to
        layer_url: The URL containing geodata to import
        layer_name: The display name for the new layer
        metadata: Optional metadata for the layer
        hints: Optional list of hints for interpreting the data
        api_token: Optional API token

    Returns:
        The upload response
    """
    json_payload = {
        "import_url": layer_url,
        "name": layer_name,
    }

    if metadata is not None:
        json_payload["metadata"] = metadata
    if hints is not None:
        json_payload["hints"] = hints

    response = make_request(
        url=LAYER_UPLOAD.format(map_id=map_id),
        method="POST",
        api_token=api_token,
        json=json_payload,
    )
    return json.load(response)


def refresh_url_layer(map_id: str, layer_id: str, api_token: str | None = None):
    """Refresh a layer originated from a URL upload"""
    response = make_request(
        url=LAYER_REFRESH.format(
            map_id=map_id,
            layer_id=layer_id,
        ),
        method="POST",
        api_token=api_token,
    )
    return json.load(response)


@deprecated(reason="Please use `get_layer` instead")
def get_layer_details(map_id: str, api_token: str | None = None):
    get_layer(map_id, api_token)


def get_layer(
    map_id: str,
    layer_id: str,
    api_token: str | None = None,
):
    """Get details of a layer"""
    response = make_request(
        url=LAYER.format(
            map_id=map_id,
            layer_id=layer_id,
        ),
        method="GET",
        api_token=api_token,
    )
    return json.load(response)


def update_layer_style(
    map_id: str,
    layer_id: str,
    style: dict,
    api_token: str | None = None,
):
    """Update a layer's style"""
    response = make_request(
        url=LAYER_UPDATE_STYLE.format(
            map_id=map_id,
            layer_id=layer_id,
        ),
        method="POST",
        json={"style": style},
        api_token=api_token,
    )
    return json.load(response)


def get_export_link(
    map_id: str,
    layer_id: str,
    api_token: str | None = None,
):
    """Get a download link for a layer

    Vector layers will be downloaded in GPKG format. Raster layers will be GeoTIFFs.
    """
    response = make_request(
        url=LAYER_EXPORT_LINK.format(map_id=map_id, layer_id=layer_id),
        method="GET",
        api_token=api_token,
    )
    return json.load(response)["export_link"]


def download_layer(
    map_id: str,
    layer_id: str,
    file_name: str | None = None,
    api_token: str | None = None,
) -> str:
    """Download a layer to a file.

    Vector layers will be downloaded in GPKG format. Raster layers will be GeoTIFFs.
    If a specific file name is not provided, the default file name will be saved to
    the current working directory.
    """
    export_link = get_export_link(map_id, layer_id, api_token)
    with urllib.request.urlopen(export_link) as response:
        if file_name is None:
            parsed_url = urllib.parse.urlparse(response.url)
            file_name = os.path.basename(parsed_url.path)
        with open(file_name, "wb") as file_obj:
            file_obj.write(response.read())
    return file_name


def update_layers(
    map_id: str,
    layer_params_list: list[dict[str, object]],
    api_token: str | None = None,
):
    """Update multiple layers at once

    Args:
        map_id: The ID of the map containing the layers
        layer_params_list: List of layer parameters to update
                           Each dict must contain at least an "id" key
                           Optional keys include "name", "caption",
                           "metadata", "ordering_key", "refresh_period"
        api_token: Optional API token

    Returns:
        The updated layers
    """
    response = make_request(
        url=LAYERS.format(map_id=map_id),
        method="POST",
        json=layer_params_list,
        api_token=api_token,
    )
    return json.load(response)


def delete_layer(
    map_id: str,
    layer_id: str,
    api_token: str | None = None,
):
    """Delete a layer from a map"""
    make_request(
        url=LAYER.format(map_id=map_id, layer_id=layer_id),
        method="DELETE",
        api_token=api_token,
    )


def publish_layer(
    map_id: str,
    layer_id: str,
    name: str = None,
    api_token: str | None = None,
):
    """Publish a layer to the Felt library

    Args:
        map_id: The ID of the map containing the layer
        layer_id: The ID of the layer to publish
        name: Optional name to publish the layer under
        api_token: Optional API token

    Returns:
        The published layer
    """
    json_payload = {}
    if name is not None:
        json_payload["name"] = name

    response = make_request(
        url=LAYER_PUBLISH.format(map_id=map_id, layer_id=layer_id),
        method="POST",
        json=json_payload,
        api_token=api_token,
    )
    return json.load(response)


def create_custom_export(
    map_id: str,
    layer_id: str,
    output_format: str,
    filters: list = None,
    email_on_completion: bool = True,
    api_token: str | None = None,
):
    """Create a custom export of a layer

    Args:
        map_id: The ID of the map containing the layer
        layer_id: The ID of the layer to export
        output_format: The format to export in.
                     Options are "csv", "gpkg", or "geojson"
        filters: Optional list of filters in Felt Style Language filter format
        email_on_completion: Whether to send an email when the export completes.
                           Defaults to True.
        api_token: Optional API token

    Returns:
        Export request details including ID and polling endpoint
    """
    json_payload = {
        "output_format": output_format,
        "email_on_completion": email_on_completion,
    }

    if filters is not None:
        json_payload["filters"] = filters

    response = make_request(
        url=LAYER_CUSTOM_EXPORT.format(map_id=map_id, layer_id=layer_id),
        method="POST",
        json=json_payload,
        api_token=api_token,
    )
    return json.load(response)


def get_custom_export_status(
    map_id: str,
    layer_id: str,
    export_id: str,
    api_token: str | None = None,
):
    """Check the status of a custom export

    Args:
        map_id: The ID of the map containing the layer
        layer_id: The ID of the layer being exported
        export_id: The ID of the export request
        api_token: Optional API token

    Returns:
        Export status including download URL when complete
    """
    response = make_request(
        url=LAYER_CUSTOM_EXPORT_STATUS.format(
            map_id=map_id,
            layer_id=layer_id,
            export_id=export_id,
        ),
        method="GET",
        api_token=api_token,
    )
    return json.load(response)


def duplicate_layers(
    duplicate_params: list[dict[str, str]], api_token: str | None = None
):
    """Duplicate layers from one map to another

    Args:
        duplicate_params: List of layer duplication parameters. Each dict must contain:
                        - For duplicating a single layer:
                          - "source_layer_id": ID of the layer to duplicate
                          - "destination_map_id": ID of the map to duplicate to
                        - For duplicating a layer group:
                          - "source_layer_group_id": ID of the layer group to duplicate
                          - "destination_map_id": ID of the map to duplicate to
        api_token: Optional API token

    Returns:
        The duplicated layers and layer groups
    """
    response = make_request(
        url=LAYER_DUPLICATE,
        method="POST",
        json=duplicate_params,
        api_token=api_token,
    )
    return json.load(response)


def _upload_file(presigned_upload, file_name):
    url = presigned_upload["url"]
    presigned_attributes = presigned_upload["presigned_attributes"]

    with open(file_name, "rb") as file_obj:
        request = _multipart_request(url, presigned_attributes, file_obj)
        urllib.request.urlopen(request)
    return presigned_upload


def _multipart_request(
    url: str, presigned_attributes: dict[str, str], file_obj: typing.IO[bytes]
) -> urllib.request.Request:
    """Make a multipart/form-data request with the given file"""
    boundary = "-" * 20 + str(uuid.uuid4())
    headers = {"Content-Type": f'multipart/form-data; boundary="{boundary}"'}
    fname = os.path.basename(file_obj.name)

    data = io.BytesIO()
    text = io.TextIOWrapper(data, encoding="latin-1")
    for key, value in presigned_attributes.items():
        text.write(f"--{boundary}\r\n")
        text.write(f'Content-Disposition: form-data; name="{key}"\r\n\r\n')
        text.write(f"{value}\r\n")
    text.write(f"--{boundary}\r\n")
    text.write(f'Content-Disposition: form-data; name="file"; filename="{fname}"\r\n')
    text.write("Content-Type: application/octet-stream\r\n\r\n")
    text.flush()
    data.write(file_obj.read())
    data.write(f"\r\n--{boundary}".encode("latin-1"))
    body = data.getvalue()

    return urllib.request.Request(url, data=body, headers=headers, method="POST")
