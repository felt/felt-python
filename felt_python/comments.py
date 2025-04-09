"""Comments"""

import json

from urllib.parse import urljoin

from .api import make_request, BASE_URL


COMMENT = urljoin(BASE_URL, "maps/{map_id}/comments/{comment_id}")
COMMENT_RESOLVE = urljoin(BASE_URL, "maps/{map_id}/comments/{comment_id}/resolve")
COMMENT_EXPORT = urljoin(BASE_URL, "maps/{map_id}/comments/export")


def export_comments(map_id: str, format: str = "json", api_token: str | None = None):
    """Export comments from a map

    Args:
        map_id: The ID of the map to export comments from
        format: The format to export the comments in, either 'csv' or 'json' (default)
        api_token: Optional API token

    Returns:
        The exported comments in the specified format
    """
    url = f"{COMMENT_EXPORT.format(map_id=map_id)}?format={format}"
    response = make_request(
        url=url,
        method="GET",
        api_token=api_token,
    )
    return json.load(response)


def resolve_comment(map_id: str, comment_id: str, api_token: str | None = None):
    """Resolve a comment

    Args:
        map_id: The ID of the map that contains the comment
        comment_id: The ID of the comment to resolve
        api_token: Optional API token

    Returns:
        Confirmation of the resolved comment
    """
    response = make_request(
        url=COMMENT_RESOLVE.format(map_id=map_id, comment_id=comment_id),
        method="POST",
        api_token=api_token,
    )
    return json.load(response)


def delete_comment(map_id: str, comment_id: str, api_token: str | None = None):
    """Delete a comment

    Args:
        map_id: The ID of the map that contains the comment
        comment_id: The ID of the comment to delete
        api_token: Optional API token
    """
    make_request(
        url=COMMENT.format(map_id=map_id, comment_id=comment_id),
        method="DELETE",
        api_token=api_token,
    )
