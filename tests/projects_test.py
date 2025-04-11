"""
End-to-end test for the Felt Projects functionality.
Uses the felt_python library to test project creation, updating, and related map operations.
"""

import os
import sys
import unittest
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from felt_python import (
    list_projects,
    create_project,
    get_project,
    update_project,
    create_map,
    move_map,
)


class FeltProjectsTest(unittest.TestCase):
    """Test the Felt API projects functionality."""

    def setUp(self):
        if not os.environ.get("FELT_API_TOKEN"):
            self.skipTest("FELT_API_TOKEN environment variable not set")

        # Generate timestamp for unique resource names
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    def test_projects_workflow(self):
        """Test the complete workflow for project operations."""
        # Step 1: List available projects
        print("Listing available projects...")

        projects = list_projects()

        self.assertIsNotNone(projects)
        print(f"Found {len(projects)} projects")

        # Step 2: Create a new project
        project_name = f"Test Project ({self.timestamp})"
        print(f"Creating project: {project_name}...")

        project = create_project(
            name=project_name, visibility="private"  # Options: "workspace" or "private"
        )

        self.assertIsNotNone(project)
        self.assertIn("id", project)
        project_id = project["id"]
        print(f"Created project with ID: {project_id}")

        # Step 3: Get project details
        print(f"Getting details for project: {project_id}...")

        project_details = get_project(project_id)

        self.assertIsNotNone(project_details)
        self.assertEqual(project_details["id"], project_id)
        self.assertEqual(project_details["name"], project_name)
        self.assertEqual(project_details["visibility"], "private")
        print(f"Retrieved project details: {project_details['name']}")

        # Step 4: Update a project
        updated_name = f"Test Project Test Updated ({self.timestamp})"
        print(f"Updating project to: {updated_name}...")

        updated_project = update_project(
            project_id=project_id,
            name=updated_name,
            visibility="workspace",  # Change visibility to workspace-wide
        )

        self.assertIsNotNone(updated_project)

        # Verify update by getting project details again
        updated_details = get_project(project_id)

        self.assertEqual(updated_details["name"], updated_name)
        self.assertEqual(updated_details["visibility"], "workspace")
        print("Project updated successfully")

        # Step 5: Create a map and move it to the project
        map_name = f"Map for testing projects ({self.timestamp})"
        print(f"Creating map: {map_name}...")

        map_resp = create_map(
            title=map_name,
            lat=37.7749,
            lon=-122.4194,  # San Francisco
            zoom=12,
            public_access="private",
        )

        self.assertIsNotNone(map_resp)
        self.assertIn("id", map_resp)
        map_id = map_resp["id"]
        print(f"Created map with ID: {map_id}")

        # Move the map to our new project
        print(f"Moving map to project: {project_id}...")

        moved_map = move_map(map_id=map_id, project_id=project_id)

        self.assertIsNotNone(moved_map)
        self.assertEqual(moved_map["id"], map_id)
        self.assertEqual(moved_map["project_id"], project_id)
        print("Map moved successfully")

        # Step 6: Verify the map was moved
        print("Verifying map was moved to project...")

        project_with_map = get_project(project_id)

        # Check if our map is in the project
        map_in_project = False
        project_maps = project_with_map.get("maps", [])
        for project_map in project_maps:
            if project_map["id"] == map_id:
                map_in_project = True
                break

        self.assertTrue(map_in_project, "Map should be in the project")
        print(f"Number of maps in project: {len(project_maps)}")
        print(f"Our map is in the project: {map_in_project}")

        print(f"\nProjects test completed successfully! Project ID: {project_id}")


if __name__ == "__main__":
    unittest.main()
