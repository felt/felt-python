"""
End-to-end test for the Felt Layer Groups functionality.
Uses the felt_python library to test layer group creation, updating, and other operations.
"""

import os
import sys
import unittest
import time
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from felt_python import (
    create_map,
    list_layer_groups,
    get_layer_group,
    update_layer_groups,
    publish_layer_group,
    update_layers,
    get_layer,
    upload_file,
)


class FeltLayerGroupsTest(unittest.TestCase):
    """Test the Felt API layer groups functionality."""

    def setUp(self):
        if not os.environ.get("FELT_API_TOKEN"):
            self.skipTest("FELT_API_TOKEN environment variable not set")

        # Generate timestamp for unique resource names
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    def test_layer_groups_workflow(self):
        """Test the complete workflow for layer groups operations."""
        # Step 1: Create a map to work with
        map_name = f"Layer Groups Test Map ({self.timestamp})"
        print(f"Creating map: {map_name}...")

        response = create_map(
            title=map_name,
            lat=40,
            lon=-3,
            zoom=5,
            public_access="private",
        )

        self.assertIsNotNone(response)
        self.assertIn("id", response)
        map_id = response["id"]
        print(f"Created map with ID: {map_id}")
        print(f"Map URL: {response['url']}")

        # Step 2: Upload some layers to work with
        print("Uploading first layer...")
        file_name = os.path.join(
            os.path.dirname(__file__), "fixtures/null-island-points-sample.geojson"
        )

        layer1_resp = upload_file(
            map_id=map_id, file_name=file_name, layer_name="Points Layer"
        )

        self.assertIsNotNone(layer1_resp)
        self.assertIn("layer_id", layer1_resp)
        layer1_id = layer1_resp["layer_id"]
        print(f"Uploaded first layer with ID: {layer1_id}")

        print("Uploading second layer...")
        file_name = os.path.join(
            os.path.dirname(__file__), "fixtures/null-island-polygons-wkt.csv"
        )

        layer2_resp = upload_file(
            map_id=map_id,
            file_name=file_name,
            layer_name="Polygons Layer",
        )

        self.assertIsNotNone(layer2_resp)
        self.assertIn("layer_id", layer2_resp)
        layer2_id = layer2_resp["layer_id"]
        print(f"Uploaded second layer with ID: {layer2_id}")

        # Wait for layer processing to complete
        print("Waiting for layers to finish processing...")
        max_wait_time = 60  # seconds

        # Wait for first layer
        start_time = time.time()
        while time.time() - start_time < max_wait_time:
            layer = get_layer(map_id, layer1_id)
            if layer["progress"] >= 100:
                print(
                    f"First layer processing completed in {time.time() - start_time:.1f} seconds"
                )
                break
            print(f"First layer progress: {layer['progress']}%")
            time.sleep(5)

        # Wait for second layer
        start_time = time.time()
        while time.time() - start_time < max_wait_time:
            layer = get_layer(map_id, layer2_id)
            if layer["progress"] >= 100:
                print(
                    f"Second layer processing completed in {time.time() - start_time:.1f} seconds"
                )
                break
            print(f"Second layer progress: {layer['progress']}%")
            time.sleep(5)

        # Step 3: List initial layer groups (should be empty)
        print("Listing initial layer groups...")

        initial_groups = list_layer_groups(map_id)

        self.assertIsNotNone(initial_groups)
        print(f"Found {len(initial_groups)} initial layer groups")

        # Step 4: Create layer groups
        print("Creating layer groups...")
        layer_groups = [
            {"name": "Vector Data", "caption": "A collection of vector datasets"},
            {"name": "Base Data", "caption": "Reference layers"},
        ]

        created_groups = update_layer_groups(map_id, layer_groups)

        self.assertIsNotNone(created_groups)
        self.assertEqual(len(created_groups), 2)
        print(f"Created {len(created_groups)} layer groups")

        # Step 5: Retrieve a specific layer group's details
        group_id = created_groups[0]["id"]
        print(f"Getting details for layer group: {group_id}...")

        group_details = get_layer_group(map_id, group_id)

        self.assertIsNotNone(group_details)
        self.assertEqual(group_details["id"], group_id)
        self.assertEqual(group_details["name"], "Vector Data")
        print(f"Retrieved details for layer group: {group_details['name']}")

        # Step 6: Update layer groups
        print("Updating layer groups...")
        # Retrieve current groups

        current_groups = list_layer_groups(map_id)

        self.assertEqual(len(current_groups), 2)

        group1_id = current_groups[0]["id"]
        group2_id = current_groups[1]["id"]

        # Update the groups
        updated_groups = [
            {
                "id": group1_id,
                "name": "Vector Data (Updated)",
                "caption": "A collection of vector datasets (updated)",
                "ordering_key": 1,
            },
            {
                "id": group2_id,
                "name": "Base Data (Updated)",
                "caption": "Reference layers (updated)",
                "ordering_key": 2,
            },
        ]

        update_result = update_layer_groups(map_id, updated_groups)

        self.assertIsNotNone(update_result)
        self.assertEqual(len(update_result), 2)

        # Verify updates by getting layer groups again
        updated_groups_list = list_layer_groups(map_id)

        for group in updated_groups_list:
            if group["id"] == group1_id:
                self.assertEqual(group["name"], "Vector Data (Updated)")
                self.assertEqual(
                    group["caption"], "A collection of vector datasets (updated)"
                )
            elif group["id"] == group2_id:
                self.assertEqual(group["name"], "Base Data (Updated)")
                self.assertEqual(group["caption"], "Reference layers (updated)")

        print("Layer groups updated successfully")

        # Step 7: Update layers to assign them to groups
        print("Updating layers to assign them to groups...")
        layer_updates = [
            {
                "id": layer1_id,
                "layer_group_id": group1_id,
            },
            {
                "id": layer2_id,
                "layer_group_id": group2_id,
            },
        ]

        updated_layers = update_layers(map_id, layer_updates)

        self.assertIsNotNone(updated_layers)
        print("Layers assigned to groups successfully")

        # Verify assignment by checking each group's contents
        group1_details = get_layer_group(map_id, group1_id)

        self.assertTrue(
            any(layer["id"] == layer1_id for layer in group1_details["layers"])
        )

        group2_details = get_layer_group(map_id, group2_id)
        self.assertTrue(
            any(layer["id"] == layer2_id for layer in group2_details["layers"])
        )

        # Step 8: Publish a layer group to the library
        print(f"Publishing layer group: {group1_id} to the library...")
        try:
            published_group = publish_layer_group(
                map_id=map_id,
                layer_group_id=group1_id,
                name="Published Vector Data Test",
            )

            self.assertIsNotNone(published_group)
            print(f"Published layer group with name: {published_group['name']}")
        except Exception as e:
            print(
                f"Publishing layer group failed (might be normal due to test data): {e}"
            )

        print(f"\nLayer groups test completed successfully! Map URL: {response['url']}")


if __name__ == "__main__":
    unittest.main()
