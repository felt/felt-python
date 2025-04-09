"""User"""

import json

from urllib.parse import urljoin

from .api import make_request, BASE_URL


USER = urljoin(BASE_URL, "user")


def get_current_user(api_token: str | None = None):
    """Get details of the currently authenticated user

    Args:
        api_token: Optional API token

    Returns:
        The user details including id, name, and email
    """
    response = make_request(
        url=USER,
        method="GET",
        api_token=api_token,
    )
    return json.load(response)
