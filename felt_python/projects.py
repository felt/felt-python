"""Projects"""

import json

from urllib.parse import urljoin

from .api import make_request, BASE_URL


PROJECTS_ENDPOINT = urljoin(BASE_URL, "projects/")
PROJECT_TEMPLATE = urljoin(PROJECTS_ENDPOINT, "{project_id}/")
PROJECT_UPDATE_TEMPLATE = urljoin(PROJECTS_ENDPOINT, "{project_id}/update")


def list_projects(workspace_id: str | None = None, api_token: str | None = None):
    """List all projects accessible to the authenticated user"""
    url = PROJECTS_ENDPOINT
    if workspace_id:
        url = f"{url}?workspace_id={workspace_id}"
    response = make_request(
        url=url,
        method="GET",
        api_token=api_token,
    )
    return json.load(response)


def create_project(name: str, visibility: str, api_token: str | None = None):
    """Create a new project

    Args:
        name: The name to be used for the Project
        visibility: Either "workspace" (viewable by all members of the workspace)
                  or "private" (private to users who are invited)
        api_token: Optional API token

    Returns:
        The created project
    """
    response = make_request(
        url=PROJECTS_ENDPOINT,
        method="POST",
        json={"name": name, "visibility": visibility},
        api_token=api_token,
    )
    return json.load(response)


def get_project_details(project_id: str, api_token: str | None = None):
    """Get details of a project"""
    response = make_request(
        url=PROJECT_TEMPLATE.format(project_id=project_id),
        method="GET",
        api_token=api_token,
    )
    return json.load(response)


def update_project(
    project_id: str,
    name: str | None = None,
    visibility: str | None = None,
    api_token: str | None = None,
):
    """Update a project's details

    Args:
        project_id: The ID of the project to update
        name: Optional new name for the project
        visibility: Optional new visibility setting ("workspace" or "private")
        api_token: Optional API token

    Returns:
        The updated project
    """
    json_args = {}
    if name is not None:
        json_args["name"] = name
    if visibility is not None:
        json_args["visibility"] = visibility

    response = make_request(
        url=PROJECT_UPDATE_TEMPLATE.format(project_id=project_id),
        method="POST",
        json=json_args,
        api_token=api_token,
    )
    return json.load(response)


def delete_project(project_id: str, api_token: str | None = None):
    """Delete a project

    Note: This will delete all Folders and Maps inside the project!
    """
    make_request(
        url=PROJECT_TEMPLATE.format(project_id=project_id),
        method="DELETE",
        api_token=api_token,
    )
