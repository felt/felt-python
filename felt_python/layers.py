"""Layers"""
import json
import os
import tempfile

import geopandas as gpd
import pandas as pd
import requests

from .api import (
    make_request,
    LAYERS_TEMPLATE,
    URL_IMPORT_TEMPLATE,
    REFRESH_FILE_TEMPLATE,
    REFRESH_URL_TEMPLATE,
    UPLOAD_TEMPLATE,
    LAYER_STYLE_TEMPLATE,
)


def list_layers(map_id: str, api_token: str | None = None):
    """List layers on a map"""
    response = make_request(
        url=LAYERS_TEMPLATE.expand(map_id=map_id),
        method=requests.get,
        api_token=api_token,
    )
    return response.json()["data"]


def _request_and_upload(
    url: str,
    file_name: str,
    layer_name: str | None = None,
    api_token: str | None = None,
):
    """Upload or refresh a file"""
    json_payload = {"file_names": [file_name]}
    if layer_name:
        json_payload["name"] = layer_name
    layer_response = make_request(
        url=url, method=requests.post, api_token=api_token, json=json_payload
    )
    presigned_upload = layer_response.json()

    url = presigned_upload["data"]["attributes"]["url"]
    presigned_attributes = presigned_upload["data"]["attributes"][
        "presigned_attributes"
    ]
    with open(file_name, "rb") as file_obj:
        output = requests.post(
            url,
            # Order is important, file should come at the end
            files={**presigned_attributes, "file": file_obj},
        )
    return output


def upload_file(
    map_id: str,
    file_name: str,
    layer_name: str | None = None,
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
    dataframe: pd.DataFrame | gpd.GeoDataFrame,
    layer_name: str | None = None,
    api_token: str | None = None,
):
    """Upload a (Geo)Pandas (Geo)DataFrame to a Felt map"""
    with tempfile.TemporaryDirectory() as tempdir:
        if isinstance(dataframe, gpd.GeoDataFrame):
            file_name = os.path.join(tempdir, "geodataframe.gpkg")
            dataframe.to_file(file_name)
        else:
            file_name = os.path.join(tempdir, "dataframe.csv")
            dataframe.to_csv(file_name)
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
        url=REFRESH_FILE_TEMPLATE.expand(map_id=map_id, layer_id=layer_id),
        file_name=file_name,
        api_token=api_token,
    )


def upload_url(
    map_id: str,
    layer_url: str,
    layer_name: str | None = None,
    api_token: str | None = None,
):
    """Upload a URL to a Felt map"""
    json_payload = {"layer_url": layer_url}
    if layer_name:
        json_payload["name"] = layer_name
    layer_response = make_request(
        url=URL_IMPORT_TEMPLATE.expand(map_id=map_id),
        method=requests.post,
        api_token=api_token,
        json=json_payload,
    )
    return layer_response.json()["data"]


def refresh_url_layer(map_id: str, layer_id: str, api_token: str | None = None):
    """Refresh a layer originated from a URL upload"""
    layer_response = make_request(
        url=REFRESH_URL_TEMPLATE.expand(
            map_id=map_id,
            layer_id=layer_id,
        ),
        method=requests.post,
        api_token=api_token,
    )
    return layer_response.json()["data"]


def get_layer_style(
    map_id: str,
    layer_id: str,
    api_token: str | None = None,
):
    """Get style of a layer"""
    response = make_request(
        url=LAYER_STYLE_TEMPLATE.expand(
            map_id=map_id,
            layer_id=layer_id,
        ),
        method=requests.get,
        api_token=api_token,
    )
    return response.json()["data"]


def update_layer_style(
    map_id: str,
    layer_id: str,
    style: dict,
    api_token: str | None = None,
):
    """Style a layer"""
    response = make_request(
        url=LAYER_STYLE_TEMPLATE.expand(
            map_id=map_id,
            layer_id=layer_id,
        ),
        method=requests.patch,
        json={"style": json.dumps(style)},
        api_token=api_token,
    )
    return response.json()["data"]
