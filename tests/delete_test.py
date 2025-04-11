"""
Deletion test for the Felt Python library.
Creates and then deletes all types of resources to test deletion functionality.
"""

import os
import sys
import unittest
import time
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from felt_python import (
    # Maps
    create_map,
    delete_map,
    # Elements
    list_elements,
    upsert_elements,
    delete_element,
    list_element_groups,
    upsert_element_groups,
    # Layers
    get_layer,
    upload_file,
    delete_layer,
    # Layer Groups
    list_layer_groups,
    update_layer_groups,
    delete_layer_group,
    # Projects
    list_projects,
    create_project,
    delete_project,
    # Sources
    list_sources,
    create_source,
    delete_source,
)


class FeltDeleteTest(unittest.TestCase):
    """Test the Felt API resource deletion functionality."""

    def setUp(self):
        if not os.environ.get("FELT_API_TOKEN"):
            self.skipTest("FELT_API_TOKEN environment variable not set")

        # Generate timestamp for unique resource names
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    def test_resource_deletion(self):
        """Create and then delete all types of resources to test deletion functionality."""

        # Create a source and then delete it
        source_name = f"Source for deletion ({self.timestamp})"
        print(f"Creating source: {source_name}...")

        source = create_source(
            name=source_name,
            connection={
                "type": "wms_wmts",
                "url": "https://basemap.nationalmap.gov/arcgis/services/USGSTopo/MapServer/WMSServer",
            },
            permissions={"type": "workspace_editors"},
        )

        self.assertIsNotNone(source)
        source_id = source["id"]
        print(f"Created source with ID: {source_id}")

        # Delete the source
        print(f"Deleting source: {source_id}...")

        delete_source(source_id)

        # Verify deletion by listing sources
        all_sources = list_sources()

        source_exists = any(s["id"] == source_id for s in all_sources)
        self.assertFalse(source_exists)
        print("Source deleted successfully")

        # Create a project and then delete it
        project_name = f"Project for deletion ({self.timestamp})"
        print(f"Creating project: {project_name}...")

        project = create_project(name=project_name, visibility="private")

        self.assertIsNotNone(project)
        project_id = project["id"]
        print(f"Created project with ID: {project_id}")

        # Delete the project
        print(f"Deleting project: {project_id}...")

        delete_project(project_id)

        # Verify deletion by listing projects
        all_projects = list_projects()

        project_exists = any(p["id"] == project_id for p in all_projects)
        self.assertFalse(project_exists)
        print("Project deleted successfully")

        # Create a map with layers, layer groups, elements, element groups and delete them
        map_name = f"Map for deletion ({self.timestamp})"
        print(f"Creating map: {map_name}...")

        map_resp = create_map(
            title=map_name, lat=40, lon=-3, zoom=8, public_access="private"
        )

        self.assertIsNotNone(map_resp)
        map_id = map_resp["id"]
        print(f"Created map with ID: {map_id}")

        # Upload a layer
        print("Creating a layer...")
        file_name = os.path.join(
            os.path.dirname(__file__), "fixtures/null-island-points-sample.geojson"
        )

        layer_resp = upload_file(
            map_id=map_id,
            file_name=file_name,
            layer_name="Layer for deletion",
        )

        self.assertIsNotNone(layer_resp)
        layer_id = layer_resp["layer_id"]
        print(f"Created layer with ID: {layer_id}")

        # Wait for layer processing
        print("Waiting for layer processing...")
        max_wait_time = 60  # seconds
        start_time = time.time()

        while time.time() - start_time < max_wait_time:
            layer = get_layer(map_id, layer_id)
            if layer["progress"] >= 100:
                print(
                    f"Layer processing completed in {time.time() - start_time:.1f} seconds"
                )
                break
            print(f"Layer progress: {layer['progress']}%")
            time.sleep(5)

        # Create layer groups
        print("Creating layer groups...")
        layer_groups = [
            {"name": "Layer Group for deletion", "caption": "Test layer group"}
        ]

        layer_group_resp = update_layer_groups(map_id, layer_groups)

        self.assertIsNotNone(layer_group_resp)
        layer_group_id = layer_group_resp[0]["id"]
        print(f"Created layer group with ID: {layer_group_id}")

        # Create element groups
        print("Creating element groups...")
        element_groups = [
            {
                "name": "Element Group for deletion",
                "symbol": "square",
                "color": "#FF0000",
            }
        ]

        element_group_resp = upsert_element_groups(map_id, element_groups)

        self.assertIsNotNone(element_group_resp)
        element_group_id = element_group_resp[0]["id"]
        print(f"Created element group with ID: {element_group_id}")

        # Create elements
        print("Creating elements...")
        elements = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [-3.70379, 40.416775]},
                    "properties": {"name": "Element for deletion"},
                }
            ],
        }

        elements_resp = upsert_elements(map_id, elements)

        self.assertIsNotNone(elements_resp)
        element_id = elements_resp["features"][0]["properties"]["felt:id"]
        print(f"Created element with ID: {element_id}")

        # Now delete each resource in reverse order

        # Delete the element
        print(f"Deleting element: {element_id}...")

        delete_element(map_id, element_id)

        # Verify element deletion
        all_elements = list_elements(map_id)

        element_exists = any(
            el["properties"].get("felt:id") == element_id
            for el in all_elements["features"]
        )
        self.assertFalse(element_exists)
        print("Element deleted successfully")

        # Delete the layer group
        print(f"Deleting layer group: {layer_group_id}...")

        delete_layer_group(map_id, layer_group_id)

        # Verify layer group deletion
        all_layer_groups = list_layer_groups(map_id)

        layer_group_exists = any(g["id"] == layer_group_id for g in all_layer_groups)
        self.assertFalse(layer_group_exists)
        print("Layer group deleted successfully")

        # Delete the layer
        print(f"Deleting layer: {layer_id}...")

        delete_layer(map_id, layer_id)

        # Verify layer deletion by attempting to get it
        try:
            deleted_layer = get_layer(map_id, layer_id)
            self.fail("Layer should have been deleted but was still accessible")
        except Exception as e:
            print("Layer deleted successfully")

        # Delete the map
        print(f"Deleting map: {map_id}...")

        delete_map(map_id)

        print("Map deletion command executed successfully")


if __name__ == "__main__":
    unittest.main()
