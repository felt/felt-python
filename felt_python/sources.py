"""Sources"""

import json

from urllib.parse import urljoin
from typing import Dict, Any, List, Union

from .api import make_request, BASE_URL


SOURCES_ENDPOINT = urljoin(BASE_URL, "sources/")
SOURCE_TEMPLATE = urljoin(SOURCES_ENDPOINT, "{source_id}/")
SOURCE_UPDATE_TEMPLATE = urljoin(SOURCES_ENDPOINT, "{source_id}/update")
SOURCE_SYNC_TEMPLATE = urljoin(SOURCES_ENDPOINT, "{source_id}/sync")


def list_sources(workspace_id: str | None = None, api_token: str | None = None):
    """List all sources accessible to the authenticated user"""
    url = SOURCES_ENDPOINT
    if workspace_id:
        url = f"{url}?workspace_id={workspace_id}"
    response = make_request(
        url=url,
        method="GET",
        api_token=api_token,
    )
    return json.load(response)


def create_source(
    name: str, 
    connection: Dict[str, Any], 
    permissions: Dict[str, Any] = None,
    api_token: str | None = None
):
    """Create a new source
    
    Args:
        name: The name of the source
        connection: Connection details - varies by source type
        permissions: Optional permissions configuration 
        api_token: Optional API token
    
    Returns:
        The created source reference
    """
    json_payload = {"name": name, "connection": connection}
    if permissions:
        json_payload["permissions"] = permissions
        
    response = make_request(
        url=SOURCES_ENDPOINT,
        method="POST",
        json=json_payload,
        api_token=api_token,
    )
    return json.load(response)


def get_source_details(source_id: str, api_token: str | None = None):
    """Get details of a source"""
    response = make_request(
        url=SOURCE_TEMPLATE.format(source_id=source_id),
        method="GET",
        api_token=api_token,
    )
    return json.load(response)


def update_source(
    source_id: str, 
    name: str | None = None,
    connection: Dict[str, Any] | None = None,
    permissions: Dict[str, Any] | None = None,
    api_token: str | None = None
):
    """Update a source's details
    
    Args:
        source_id: The ID of the source to update
        name: Optional new name for the source
        connection: Optional updated connection details
        permissions: Optional updated permissions configuration
        api_token: Optional API token
    
    Returns:
        The updated source reference
    """
    json_payload = {}
    if name is not None:
        json_payload["name"] = name
    if connection is not None:
        json_payload["connection"] = connection
    if permissions is not None:
        json_payload["permissions"] = permissions
        
    response = make_request(
        url=SOURCE_UPDATE_TEMPLATE.format(source_id=source_id),
        method="POST",
        json=json_payload,
        api_token=api_token,
    )
    return json.load(response)


def delete_source(source_id: str, api_token: str | None = None):
    """Delete a source"""
    make_request(
        url=SOURCE_TEMPLATE.format(source_id=source_id),
        method="DELETE",
        api_token=api_token,
    )


def sync_source(source_id: str, api_token: str | None = None):
    """Trigger synchronization of a source
    
    Returns:
        The source reference with synchronization status
    """
    response = make_request(
        url=SOURCE_SYNC_TEMPLATE.format(source_id=source_id),
        method="POST",
        api_token=api_token,
    )
    return json.load(response)
