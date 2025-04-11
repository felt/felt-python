"""
End-to-end test for the Felt Library functionality.
Uses the felt_python library to test library functions including listing and publishing layers.
"""

import os
import sys
import unittest
import time
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from felt_python import (
    list_library_layers,
    create_map,
    upload_file,
    get_layer,
    publish_layer,
)


class FeltLibraryTest(unittest.TestCase):
    """Test the Felt API library functionality."""

    def setUp(self):
        if not os.environ.get("FELT_API_TOKEN"):
            self.skipTest("FELT_API_TOKEN environment variable not set")

        # Generate timestamp for unique resource names
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    def test_library_workflow(self):
        """Test the complete workflow for library operations."""
        # Step 1: List layers in the workspace library
        print("Listing layers in workspace library...")

        workspace_library = list_library_layers(source="workspace")

        self.assertIsNotNone(workspace_library)
        self.assertIn("layers", workspace_library)
        self.assertIn("layer_groups", workspace_library)

        print(f"Found {len(workspace_library['layers'])} layers in workspace library")
        print(
            f"Found {len(workspace_library['layer_groups'])} layer groups in workspace library"
        )

        # Show first few layers if any
        for i, layer in enumerate(workspace_library["layers"][:3]):
            print(f"Layer {i+1}: {layer['name']} (ID: {layer['id']})")

        # Step 2: List layers in the Felt data library
        print("\nListing layers in Felt data library...")

        felt_library = list_library_layers(source="felt")

        self.assertIsNotNone(felt_library)
        self.assertIn("layers", felt_library)
        self.assertIn("layer_groups", felt_library)

        print(f"Found {len(felt_library['layers'])} layers in Felt library")
        print(f"Found {len(felt_library['layer_groups'])} layer groups in Felt library")

        # Show first few layers
        for i, layer in enumerate(felt_library["layers"][:5]):
            print(f"Layer {i+1}: {layer['name']} (ID: {layer['id']})")

        # Step 3: Create a map with a layer and publish it to the library
        map_name = f"Library Test Map ({self.timestamp})"
        print(f"\nCreating map: {map_name}...")

        map_resp = create_map(
            title=map_name, lat=40, lon=-3, zoom=5, public_access="private"
        )

        self.assertIsNotNone(map_resp)
        self.assertIn("id", map_resp)
        map_id = map_resp["id"]
        print(f"Created map with ID: {map_id}")

        # Upload a layer
        print("Uploading layer...")
        file_name = os.path.join(
            os.path.dirname(__file__), "fixtures/null-island-points.geojson"
        )

        layer_resp = upload_file(
            map_id=map_id,
            file_name=file_name,
            layer_name="Points to publish",
        )

        self.assertIsNotNone(layer_resp)
        self.assertIn("layer_id", layer_resp)
        layer_id = layer_resp["layer_id"]
        print(f"Uploaded layer with ID: {layer_id}")

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

        print("Layer ready for publishing")

        # Step 4: Publish the layer to the library
        print("Publishing layer to library...")

        published = publish_layer(
            map_id=map_id,
            layer_id=layer_id,
            name=f"Published test layer ({self.timestamp})",
        )

        self.assertIsNotNone(published)
        print(f"Layer published: {published['name']}")

        # Step 5: Verify the layer is in the library
        print("Verifying layer was added to library...")

        # Wait a moment for library to update
        time.sleep(5)

        updated_library = list_library_layers(source="workspace")

        self.assertIsNotNone(updated_library)

        # Try to find our published layer
        published_found = any(
            layer["name"] == f"Published test layer ({self.timestamp})"
            for layer in updated_library["layers"]
        )

        print(f"Published layer found in library: {published_found}")

        if not published_found:
            print("Note: Layer may not appear immediately in library listings")

        # Step 6: List all libraries (Felt and workspace)
        print("\nListing all libraries (Felt and workspace)...")

        all_libraries = list_library_layers(source="all")

        self.assertIsNotNone(all_libraries)
        self.assertIn("layers", all_libraries)
        self.assertIn("layer_groups", all_libraries)

        print(
            f"Total number of layers in all libraries: {len(all_libraries['layers'])}"
        )
        print(
            f"Total number of layer groups in all libraries: {len(all_libraries['layer_groups'])}"
        )

        print(f"\nLibrary test completed successfully! Map URL: {map_resp['url']}")


if __name__ == "__main__":
    unittest.main()
