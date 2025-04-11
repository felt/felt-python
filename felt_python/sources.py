"""Sources"""

import json

from urllib.parse import urljoin

from .api import make_request, BASE_URL


SOURCES = urljoin(BASE_URL, "sources")
SOURCE = urljoin(BASE_URL, "sources/{source_id}")
SOURCE_UPDATE = urljoin(BASE_URL, "sources/{source_id}/update")
SOURCE_SYNC = urljoin(BASE_URL, "sources/{source_id}/sync")


def list_sources(workspace_id: str | None = None, api_token: str | None = None):
    """List all sources accessible to the authenticated user"""
    url = SOURCES
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
    connection: dict[str, str],
    permissions: dict[str, str] = None,
    api_token: str | None = None,
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
        url=SOURCES,
        method="POST",
        json=json_payload,
        api_token=api_token,
    )
    return json.load(response)


def get_source(source_id: str, api_token: str | None = None):
    """Get details of a source"""
    response = make_request(
        url=SOURCE.format(source_id=source_id),
        method="GET",
        api_token=api_token,
    )
    return json.load(response)


def update_source(
    source_id: str,
    name: str | None = None,
    connection: dict[str, str] | None = None,
    permissions: dict[str, str] | None = None,
    api_token: str | None = None,
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
        url=SOURCE_UPDATE.format(source_id=source_id),
        method="POST",
        json=json_payload,
        api_token=api_token,
    )
    return json.load(response)


def delete_source(source_id: str, api_token: str | None = None):
    """Delete a source"""
    make_request(
        url=SOURCE.format(source_id=source_id),
        method="DELETE",
        api_token=api_token,
    )


def sync_source(source_id: str, api_token: str | None = None):
    """Trigger synchronization of a source

    Returns:
        The source reference with synchronization status
    """
    response = make_request(
        url=SOURCE_SYNC.format(source_id=source_id),
        method="POST",
        api_token=api_token,
    )
    return json.load(response)
