"""
End-to-end test for the Felt layer components functionality.
Uses the felt_python library to test creating, listing, updating and
deleting components on a layer.
"""

import os
import sys
import unittest
import time
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from felt_python import (
    create_map,
    delete_map,
    upload_file,
    get_layer,
    list_layer_components,
    create_layer_component,
    get_layer_component,
    update_layer_component,
    delete_layer_component,
)


class FeltComponentsTest(unittest.TestCase):
    """Test the Felt API layer components functionality."""

    def setUp(self):
        if not os.environ.get("FELT_API_TOKEN"):
            self.skipTest("FELT_API_TOKEN environment variable not set")

        # Generate timestamp for unique resource names
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    def test_components_workflow(self):
        """Test the complete workflow for layer component operations."""
        # Step 1: Create a map and upload a layer to attach components to
        map_name = f"Components Test Map ({self.timestamp})"
        print(f"Creating map: {map_name}...")

        response = create_map(
            title=map_name,
            lat=0,
            lon=0,
            zoom=10,
            public_access="private",
        )

        self.assertIsNotNone(response)
        self.assertIn("id", response)
        map_id = response["id"]
        print(f"Created map with ID: {map_id}")

        print("Uploading file layer...")
        file_name = os.path.join(
            os.path.dirname(__file__), "fixtures/null-island-points-sample.geojson"
        )
        layer_resp = upload_file(
            map_id=map_id,
            file_name=file_name,
            layer_name="Points Layer",
        )

        self.assertIsNotNone(layer_resp)
        self.assertIn("layer_id", layer_resp)
        layer_id = layer_resp["layer_id"]
        print(f"Uploaded file layer with ID: {layer_id}")

        # Wait for layer processing to complete
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

        self.assertEqual(layer["progress"], 100, "Layer processing should complete")

        # Step 2: Create a statistic component (feature count)
        print("Creating statistic component...")
        component = create_layer_component(
            map_id=map_id,
            layer_id=layer_id,
            component_type="statistic",
            data={"aggregate": "count"},
            title="Feature count",
        )

        self.assertIsNotNone(component)
        self.assertIn("id", component)
        component_id = component["id"]
        print(f"Created component with ID: {component_id}")

        # Step 3: List components
        print("Listing components...")
        components = list_layer_components(map_id, layer_id)

        self.assertIsNotNone(components)
        self.assertTrue(any(c["id"] == component_id for c in components))
        print(f"Found {len(components)} components")

        # Step 4: Get component details
        print("Getting component details...")
        details = get_layer_component(map_id, layer_id, component_id)

        self.assertIsNotNone(details)
        self.assertEqual(details["id"], component_id)
        self.assertEqual(details["type"], "statistic")

        # Step 5: Update the component
        updated_title = "Updated feature count"
        print(f"Updating component title to: {updated_title}...")
        updated = update_layer_component(
            map_id=map_id,
            layer_id=layer_id,
            component_id=component_id,
            title=updated_title,
        )

        self.assertIsNotNone(updated)

        updated_details = get_layer_component(map_id, layer_id, component_id)
        self.assertEqual(updated_details["title"], updated_title)
        print("Component updated successfully")

        # Step 6: Delete the component
        print("Deleting component...")
        delete_layer_component(map_id, layer_id, component_id)

        remaining = list_layer_components(map_id, layer_id)
        self.assertFalse(any(c["id"] == component_id for c in remaining))
        print("Component deleted successfully")

        # Clean up
        print("Cleaning up: deleting map...")
        delete_map(map_id)

        print("\nComponents test completed successfully!")


if __name__ == "__main__":
    unittest.main()
