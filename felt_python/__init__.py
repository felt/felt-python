# For now, hoist all functions to the top level
from .maps import (
    create_map,
    delete_map,
    get_map_details,
    update_map,
)
from .exceptions import AuthError
from .layers import (
    list_layers,
    upload_file,
    upload_geodataframe,
    upload_dataframe,
    upload_url,
    refresh_file_layer,
    refresh_url_layer,
    get_layer_details,
    update_layer_style,
    get_export_link,
    download_layer,
)
from .elements import (
    list_elements,
    list_element_groups,
    list_elements_in_group,
    post_elements,
    delete_element,
    post_element_group,
)

__doc__ = """
The official Python client for the Felt API
===========================================

**felt-python** is a Python client for the Felt API. It provides convenient wrappers for
common operations like creating, deleting and updating maps and data layers.

This client is especially useful at simplifying certain operations like uploading and
refreshing files and (Geo)DataFrames or updating layer styles and element properties.
"""

__all__ = [
    "create_map",
    "delete_map",
    "get_map_details",
    "update_map",
    "list_layers",
    "upload_file",
    "upload_geodataframe",
    "upload_dataframe",
    "upload_url",
    "refresh_file_layer",
    "refresh_url_layer",
    "get_layer_details",
    "update_layer_style",
    "get_export_link",
    "download_layer",
    "AuthError",
    "list_elements",
    "list_element_groups",
    "list_elements_in_group",
    "post_elements",
    "delete_element",
    "post_element_group",
]
