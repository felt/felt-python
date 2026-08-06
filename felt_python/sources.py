"""Sources"""

import json

from urllib.parse import urljoin

from .api import BASE_URL, build_query, build_url, make_request


SOURCES = urljoin(BASE_URL, "sources")
SOURCE = urljoin(BASE_URL, "sources/{source_id}")
SOURCE_UPDATE = urljoin(BASE_URL, "sources/{source_id}/update")
SOURCE_SYNC = urljoin(BASE_URL, "sources/{source_id}/sync")
SOURCE_CREDENTIALS = urljoin(BASE_URL, "sources/{source_id}/credentials")
SOURCE_CREDENTIAL = urljoin(BASE_URL, "sources/{source_id}/credentials/{credential_id}")
SOURCE_CREDENTIAL_UPDATE = urljoin(
    BASE_URL, "sources/{source_id}/credentials/{credential_id}/update"
)


def list_sources(workspace_id: str | None = None, api_token: str | None = None):
    """List all sources accessible to the authenticated user"""
    url = build_query(SOURCES, workspace_id=workspace_id)
    response = make_request(
        url=url,
        method="GET",
        api_token=api_token,
    )
    return json.load(response)


def create_source(
    name: str,
    connection: dict[str, str],
    permissions: dict[str, str] | None = None,
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
        url=build_url(SOURCE, source_id=source_id),
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
    json_payload: dict = {}
    if name is not None:
        json_payload["name"] = name
    if connection is not None:
        json_payload["connection"] = connection
    if permissions is not None:
        json_payload["permissions"] = permissions

    response = make_request(
        url=build_url(SOURCE_UPDATE, source_id=source_id),
        method="POST",
        json=json_payload,
        api_token=api_token,
    )
    return json.load(response)


def delete_source(source_id: str, api_token: str | None = None):
    """Delete a source"""
    make_request(
        url=build_url(SOURCE, source_id=source_id),
        method="DELETE",
        api_token=api_token,
    )


def sync_source(source_id: str, api_token: str | None = None):
    """Trigger synchronization of a source

    Returns:
        The source reference with synchronization status
    """
    response = make_request(
        url=build_url(SOURCE_SYNC, source_id=source_id),
        method="POST",
        api_token=api_token,
    )
    return json.load(response)


def create_source_credential(
    source_id: str,
    name: str,
    use_case: str,
    credential: dict,
    api_token: str | None = None,
):
    """Create a credential for a source

    Args:
        source_id: The ID of the source to create the credential for
        name: The name of the credential
        use_case: What the credential is used for. Options are
            "source_authentication", "stac_api_authentication",
            or "stac_asset_fetching".
        credential: The credential details. Must include a "type" key
            identifying the credential type along with its type-specific
            fields, e.g.:
            - {"type": "aws_assume_role", "role_arn": ..., "role_session_name": ...}
            - {"type": "azure_storage_connection_string", "connection_string": ...}
            - {"type": "custom_headers", "headers": [{"name": ..., "value": ...,
               "sensitive": ...}]}
              ("sensitive" is required on every header entry: a sensitive
              header's value is returned as "felt:redacted" when the
              credential is read back)
            - {"type": "gcp_service_account_json", "service_account_filename": ...,
               "service_account_json": ...}
            - {"type": "key_pair", "private_key_name": ..., "private_key": ...,
               "private_key_passphrase": ...}
            - {"type": "snowflake_pat", "token": ...}
        api_token: Optional API token

    Returns:
        The created source credential
    """
    response = make_request(
        url=SOURCE_CREDENTIALS.format(source_id=source_id),
        method="POST",
        json={"name": name, "use_case": use_case, "credential": credential},
        api_token=api_token,
    )
    return json.load(response)


def update_source_credential(
    source_id: str,
    credential_id: str,
    name: str | None = None,
    use_case: str | None = None,
    credential: dict | None = None,
    api_token: str | None = None,
):
    """Update a source credential

    Args:
        source_id: The ID of the source the credential belongs to
        credential_id: The ID of the credential to update
        name: Optional new name for the credential
        use_case: Optional new use case. Options are
            "source_authentication", "stac_api_authentication",
            or "stac_asset_fetching".
        credential: Optional updated credential details. Must include a
            "type" key identifying the credential type along with its
            type-specific fields (see create_source_credential).
        api_token: Optional API token

    Returns:
        The updated source credential
    """
    json_payload: dict = {}
    if name is not None:
        json_payload["name"] = name
    if use_case is not None:
        json_payload["use_case"] = use_case
    if credential is not None:
        json_payload["credential"] = credential

    response = make_request(
        url=SOURCE_CREDENTIAL_UPDATE.format(
            source_id=source_id, credential_id=credential_id
        ),
        method="POST",
        json=json_payload,
        api_token=api_token,
    )
    return json.load(response)


def delete_source_credential(
    source_id: str,
    credential_id: str,
    api_token: str | None = None,
):
    """Delete a source credential

    Args:
        source_id: The ID of the source the credential belongs to
        credential_id: The ID of the credential to delete
        api_token: Optional API token
    """
    make_request(
        url=SOURCE_CREDENTIAL.format(source_id=source_id, credential_id=credential_id),
        method="DELETE",
        api_token=api_token,
    )
