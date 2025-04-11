"""
End-to-end test for the Felt Layers functionality.
Uses the felt_python library to test layer creation, updating, styling and other operations.
"""

import os
import sys
import unittest
import time
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from felt_python import (
    create_map,
    list_layers,
    upload_file,
    upload_url,
    refresh_file_layer,
    refresh_url_layer,
    get_layer,
    update_layer_style,
    get_export_link,
    update_layers,
    create_custom_export,
    get_custom_export_status,
)


class FeltLayersTest(unittest.TestCase):
    """Test the Felt API layers functionality."""

    def setUp(self):
        if not os.environ.get("FELT_API_TOKEN"):
            self.skipTest("FELT_API_TOKEN environment variable not set")

        # Generate timestamp for unique resource names
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    def test_layers_workflow(self):
        """Test the complete workflow for layer operations."""
        # Step 1: Create a map to work with
        map_name = f"Layers Test Map ({self.timestamp})"
        print(f"Creating map: {map_name}...")

        response = create_map(
            title=map_name,
            lat=40,
            lon=-3,
            zoom=10,
            public_access="private",
        )

        self.assertIsNotNone(response)
        self.assertIn("id", response)
        map_id = response["id"]
        print(f"Created map with ID: {map_id}")
        print(f"Map URL: {response['url']}")

        # Step 2: Upload a file layer
        print("Uploading file layer...")
        metadata = {
            "attribution_text": "Sample Data",
            "source_name": "Felt Python Test",
            "description": "Sample points near Null Island",
        }

        file_name = os.path.join(
            os.path.dirname(__file__), "fixtures/null-island-points-sample.geojson"
        )
        layer_resp = upload_file(
            map_id=map_id,
            file_name=file_name,
            layer_name="Points Layer",
            metadata=metadata,
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
        self.assertEqual(layer["status"], "completed")

        # Step 3: Refresh file layer
        print("Refreshing file layer...")
        file_name = os.path.join(
            os.path.dirname(__file__), "fixtures/null-island-points.geojson"
        )

        refresh_response = refresh_file_layer(map_id, layer_id, file_name=file_name)

        self.assertIsNotNone(refresh_response)
        print("File layer refresh initiated")

        # Step 4: Upload a URL layer
        print("Uploading URL layer...")
        live_earthquakes_url = (
            "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
        )

        url_upload = upload_url(map_id, live_earthquakes_url, "Live Earthquakes")

        self.assertIsNotNone(url_upload)
        self.assertIn("layer_id", url_upload)
        url_layer_id = url_upload["layer_id"]
        print(f"Uploaded URL layer with ID: {url_layer_id}")

        # Wait for URL layer processing
        print("Waiting for URL layer processing...")
        start_time = time.time()

        while time.time() - start_time < max_wait_time:
            layer = get_layer(map_id, url_layer_id)
            if layer["progress"] >= 100:
                print(
                    f"URL layer processing completed in {time.time() - start_time:.1f} seconds"
                )
                break
            print(f"URL layer progress: {layer['progress']}%")
            time.sleep(5)

        # Step 5: Refresh URL layer
        print("Refreshing URL layer...")

        url_refresh_resp = refresh_url_layer(map_id, url_layer_id)

        self.assertIsNotNone(url_refresh_resp)
        print("URL layer refresh initiated")

        # Step 6: Update layer style
        print("Updating layer style...")

        current_style = get_layer(map_id, layer_id)["style"]

        self.assertIsNotNone(current_style)

        new_style = current_style.copy()
        new_style["color"] = "red"
        new_style["size"] = 20

        style_update_resp = update_layer_style(map_id, layer_id, new_style)

        self.assertIsNotNone(style_update_resp)

        # Verify style update
        updated_layer = get_layer(map_id, layer_id)

        self.assertEqual(updated_layer["style"]["color"], "red")
        self.assertEqual(updated_layer["style"]["size"], 20)
        print("Layer style updated successfully")

        # Step 7: Update multiple layers
        print("Updating multiple layers...")

        all_layers = list_layers(map_id)

        self.assertGreaterEqual(len(all_layers), 2)

        # Prepare updates for both layers
        layer_updates = [
            {
                "id": layer_id,
                "name": "Updated Points Layer",
                "caption": "New caption for points layer",
            },
            {
                "id": url_layer_id,
                "name": "Updated Earthquakes Layer",
                "caption": "New caption for earthquakes layer",
            },
        ]

        update_resp = update_layers(map_id, layer_updates)

        self.assertIsNotNone(update_resp)

        # Verify updates
        updated_layers = list_layers(map_id)

        for layer in updated_layers:
            if layer["id"] == layer_id:
                self.assertEqual(layer["name"], "Updated Points Layer")
                self.assertEqual(layer["caption"], "New caption for points layer")
            elif layer["id"] == url_layer_id:
                self.assertEqual(layer["name"], "Updated Earthquakes Layer")
                self.assertEqual(layer["caption"], "New caption for earthquakes layer")

        print("Multiple layers updated successfully")

        # Step 8: Get export link
        print("Getting layer export link...")

        export_link = get_export_link(map_id, layer_id)

        self.assertIsNotNone(export_link)
        self.assertTrue(export_link.startswith("http"))
        print("Export link obtained")

        # Step 9: Create custom export with filters
        print("Creating custom export...")

        export_request = create_custom_export(
            map_id=map_id,
            layer_id=layer_id,
            output_format="csv",
            email_on_completion=False,
        )

        self.assertIsNotNone(export_request)
        self.assertIn("export_request_id", export_request)
        export_id = export_request["export_request_id"]
        print(f"Created custom export with ID: {export_id}")

        # Poll for export status (try a few times)
        max_polls = 3
        for i in range(max_polls):
            print(f"Checking export status (attempt {i+1}/{max_polls})...")

            export_status = get_custom_export_status(
                map_id=map_id, layer_id=layer_id, export_id=export_id
            )

            print(f"Export status: {export_status['status']}")

            if export_status["status"] == "completed":
                print(
                    f"Export completed! Download URL: {export_status['download_url']}"
                )
                break
            elif export_status["status"] == "failed":
                print("Export failed")
                break

            if i < max_polls - 1:  # Don't sleep on the last attempt
                time.sleep(5)

        print(f"\nLayers test completed successfully! Map URL: {response['url']}")


if __name__ == "__main__":
    unittest.main()
