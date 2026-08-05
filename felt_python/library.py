"""Layer library"""

import json

from urllib.parse import urljoin

from .api import BASE_URL, build_query, make_request


LIBRARY = urljoin(BASE_URL, "library")


def list_library_layers(source: str = "workspace", api_token: str | None = None):
    """List layers available in the layer library

    Args:
        source: The source of library layers to list.
            Options are:
            - "workspace": list layers from your workspace library (default)
            - "felt": list layers from the Felt data library
            - "all": list layers from both sources
        api_token: Optional API token

    Returns:
        The layer library containing layers and layer groups
    """
    url = build_query(LIBRARY, source=source)
    response = make_request(
        url=url,
        method="GET",
        api_token=api_token,
    )
    return json.load(response)
