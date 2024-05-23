"""Layers"""

import json
import os
import tempfile

from .api import (
    make_request,
    LAYERS_TEMPLATE,
    REFRESH_TEMPLATE,
    UPDATE_STYLE_TEMPLATE,
    UPLOAD_TEMPLATE,
)


def list_layers(map_id: str, api_token: str | None = None):
    """List layers on a map"""
    response = make_request(
        url=LAYERS_TEMPLATE.expand(map_id=map_id),
        method="GET",
        api_token=api_token,
    )
    return json.load(response)["data"]


def _request_and_upload(
    url: str,
    file_name: str,
    layer_name: str | None = None,
    api_token: str | None = None,
):
    """Upload or refresh a file

    Both upload_file and refresh_file_layer use this function to handle the
    request and file upload. The only difference is that the upload endpoint
    requires a layer name while the refresh endpoint does not.
    """
    json_payload = {"name": layer_name} if layer_name else None
    layer_response = make_request(
        url=url, method="POST", api_token=api_token, json=json_payload
    )
    presigned_upload = layer_response.json()

    url = presigned_upload["data"]["attributes"]["url"]
    presigned_attributes = presigned_upload["data"]["attributes"][
        "presigned_attributes"
    ]
    with open(file_name, "rb") as file_obj:
        requests.post(
            url,
            # Order is important, file should come at the end
            files={**presigned_attributes, "file": file_obj},
        )
    return layer_response.json()["data"]


def upload_file(
    map_id: str,
    file_name: str,
    layer_name: str,
    api_token: str | None = None,
):
    """Upload a file to a Felt map"""
    return _request_and_upload(
        url=UPLOAD_TEMPLATE.expand(map_id=map_id),
        file_name=file_name,
        layer_name=layer_name,
        api_token=api_token,
    )


def upload_dataframe(
    map_id: str,
    dataframe: "pd.DataFrame",
    layer_name: str,
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
            api_token,
        )


def upload_geodataframe(
    map_id: str,
    geodataframe: "gpd.GeoDataFrame",
    layer_name: str,
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
            api_token,
        )


def refresh_file_layer(
    map_id: str, layer_id: str, file_name: str, api_token: str | None = None
):
    """Refresh a layer originated from a file upload"""
    return _request_and_upload(
        url=REFRESH_TEMPLATE.expand(map_id=map_id, layer_id=layer_id),
        file_name=file_name,
        api_token=api_token,
    )


def upload_url(
    map_id: str,
    layer_url: str,
    layer_name: str,
    api_token: str | None = None,
):
    """Upload a URL to a Felt map"""
    layer_response = make_request(
        url=UPLOAD_TEMPLATE.expand(map_id=map_id),
        method="POST",
        api_token=api_token,
        json={
            "import_url": layer_url,
            "name": layer_name,
        },
    )
    return layer_response.json()["data"]


def refresh_url_layer(map_id: str, layer_id: str, api_token: str | None = None):
    """Refresh a layer originated from a URL upload"""
    layer_response = make_request(
        url=REFRESH_TEMPLATE.expand(
            map_id=map_id,
            layer_id=layer_id,
        ),
        method="POST",
        api_token=api_token,
    )
    return layer_response.json()["data"]


def get_layer_details(
    map_id: str,
    layer_id: str,
    api_token: str | None = None,
):
    """Get style of a layer"""
    response = make_request(
        url=LAYERS_TEMPLATE.expand(
            map_id=map_id,
            layer_id=layer_id,
        ),
        method="GET",
        api_token=api_token,
    )
    return json.load(response)["data"]


def update_layer_style(
    map_id: str,
    layer_id: str,
    style: dict,
    api_token: str | None = None,
):
    """Style a layer"""
    response = make_request(
        url=UPDATE_STYLE_TEMPLATE.expand(
            map_id=map_id,
            layer_id=layer_id,
        ),
        method="POST",
        json={"style": style},
        api_token=api_token,
    )
    return json.load(response)["data"]
