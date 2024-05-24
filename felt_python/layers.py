"""Layers"""

import io
import json
import os
import tempfile
import typing
import urllib.request
import uuid

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
    presigned_upload = json.load(layer_response)
    url = presigned_upload["url"]
    presigned_attributes = presigned_upload["presigned_attributes"]
    with open(file_name, "rb") as file_obj:
        request = _multipart_request(url, presigned_attributes, file_obj)
        urllib.request.urlopen(request)
    return presigned_upload


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
