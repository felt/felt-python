# Hoist all functions to the top level
from .maps import (
    create_map,
    delete_map,
    get_map,
    update_map,
    move_map,
    create_embed_token,
    add_source_layer,
    # Deprecated
    get_map_details,
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
    get_layer,
    update_layer_style,
    get_export_link,
    download_layer,
    update_layers,
    delete_layer,
    publish_layer,
    create_custom_export,
    get_custom_export_status,
    duplicate_layers,
    # Deprecated
    get_layer_details,
)
from .elements import (
    list_elements,
    list_element_groups,
    upsert_elements,
    delete_element,
    get_element_group,
    upsert_element_groups,
    # Deprecated:
    post_elements,
    post_element_group,
    list_elements_in_group,
)
from .layer_groups import (
    list_layer_groups,
    get_layer_group,
    update_layer_groups,
    delete_layer_group,
    publish_layer_group,
)
from .projects import (
    list_projects,
    create_project,
    get_project,
    update_project,
    delete_project,
)
from .sources import (
    list_sources,
    create_source,
    get_source,
    update_source,
    delete_source,
    sync_source,
)
from .library import list_library_layers
from .comments import export_comments, resolve_comment, delete_comment
from .user import get_current_user

__doc__ = """
The official Python client for the Felt API
===========================================

**felt-python** is a Python client for the Felt API. It provides convenient wrappers for
common operations like creating, deleting and updating maps and data layers.

This client is especially useful at simplifying certain operations like uploading and
refreshing files and (Geo)DataFrames or updating layer styles and element properties.
"""

__all__ = [
    # Maps
    "create_map",
    "delete_map",
    "update_map",
    "move_map",
    "create_embed_token",
    "add_source_layer",
    # Layers
    "list_layers",
    "upload_file",
    "upload_geodataframe",
    "upload_dataframe",
    "upload_url",
    "refresh_file_layer",
    "refresh_url_layer",
    "get_layer",
    "update_layer_style",
    "get_export_link",
    "download_layer",
    "update_layers",
    "delete_layer",
    "publish_layer",
    "create_custom_export",
    "get_custom_export_status",
    "duplicate_layers",
    # Layer groups
    "list_layer_groups",
    "get_layer_group",
    "update_layer_groups",
    "delete_layer_group",
    "publish_layer_group",
    # Elements
    "list_elements",
    "list_element_groups",
    "list_elements_in_group",
    "upsert_elements",
    "delete_element",
    "upsert_element_groups",
    # Projects
    "list_projects",
    "create_project",
    "get_project",
    "update_project",
    "delete_project",
    # Sources
    "list_sources",
    "create_source",
    "get_source",
    "update_source",
    "delete_source",
    "sync_source",
    # Library
    "list_library_layers",
    # Comments
    "export_comments",
    "resolve_comment",
    "delete_comment",
    # User
    "get_current_user",
    # Exceptions
    "AuthError",
    # Deprecated
    "post_elements",
    "post_element_group",
    "get_map_details",
    "get_layer_details",
]
