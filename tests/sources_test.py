"""
End-to-end test for the Felt Sources functionality.
Uses the felt_python library to test source creation, updating, and map integration.
"""

import os
import sys
import unittest
import time
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from felt_python import (
    list_sources,
    create_source,
    get_source,
    update_source,
    sync_source,
    create_map,
    add_source_layer,
)


class FeltSourcesTest(unittest.TestCase):
    """Test the Felt API sources functionality."""

    def setUp(self):
        if not os.environ.get("FELT_API_TOKEN"):
            self.skipTest("FELT_API_TOKEN environment variable not set")

        # Generate timestamp for unique resource names
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    def test_sources_workflow(self):
        """Test the complete workflow for source operations."""
        # Step 1: List available sources
        print("Listing available sources...")
        sources = list_sources()

        self.assertIsNotNone(sources)
        print(f"Found {len(sources)} sources")

        # Step 2: Create a source (WMS/WMTS source as it's public)
        source_name = f"Public WMS Source ({self.timestamp})"
        print(f"Creating source: {source_name}...")

        wms_source = create_source(
            name=source_name,
            connection={
                "type": "wms_wmts",
                "url": "https://basemap.nationalmap.gov/arcgis/services/USGSTopo/MapServer/WMSServer",
            },
            permissions={
                "type": "workspace_editors"  # Share with all workspace editors
            },
        )

        self.assertIsNotNone(wms_source)
        self.assertIn("id", wms_source)
        source_id = wms_source["id"]
        print(f"Created source with ID: {source_id}")

        # Step 3: Get source details
        print(f"Getting details for source: {source_id}...")

        source_details = get_source(source_id)

        self.assertIsNotNone(source_details)
        self.assertEqual(source_details["id"], source_id)
        self.assertEqual(source_details["name"], source_name)
        print(f"Retrieved source details: {source_details['name']}")

        # Step 4: Update a source
        updated_name = f"Updated WMS Source ({self.timestamp})"
        print(f"Updating source to: {updated_name}...")

        updated_source = update_source(
            source_id=source_id,
            name=updated_name,
            # Update connection details if needed
            connection={
                "type": "wms_wmts",
                "url": "https://basemap.nationalmap.gov/arcgis/services/USGSTopo/MapServer/WMSServer",
            },
        )

        self.assertIsNotNone(updated_source)

        # Verify update by getting source details again
        updated_details = get_source(source_id)

        self.assertEqual(updated_details["name"], updated_name)
        print("Source updated successfully")

        # Step 5: Synchronize a source
        print(f"Synchronizing source: {source_id}...")

        synced_source = sync_source(source_id)

        self.assertIsNotNone(synced_source)
        print(
            f"Source sync initiated with status: {synced_source.get('sync_status', 'unknown')}"
        )

        # Step 6: Create a map and add a layer from the source
        print("Creating a map for source layers...")

        map_resp = create_map(
            title=f"Map with source layers ({self.timestamp})",
            lat=39.8283,
            lon=-98.5795,  # Center of USA
            zoom=4,
            public_access="private",
        )

        self.assertIsNotNone(map_resp)
        self.assertIn("id", map_resp)
        map_id = map_resp["id"]
        print(f"Created map with ID: {map_id}")

        # Wait for source synchronization to complete (or timeout)
        print("Waiting for source synchronization...")
        max_wait_time = 60  # seconds
        start_time = time.time()
        sync_completed = False

        while time.time() - start_time < max_wait_time:
            current_source = get_source(source_id)
            sync_status = current_source.get("sync_status")

            if sync_status == "completed":
                sync_completed = True
                print(
                    f"Source sync completed in {time.time() - start_time:.1f} seconds"
                )
                break

            print(f"Waiting for source sync... Status: {sync_status}")
            time.sleep(5)

        # Check for available datasets
        print("Checking for available datasets...")

        current_source = get_source(source_id)

        datasets = current_source.get("datasets", [])

        print(f"Available datasets: {len(datasets)}")
        for i, dataset in enumerate(datasets[:5]):  # Show first 5 datasets
            print(
                f"- {dataset.get('name', 'Unnamed')} (ID: {dataset.get('id', 'Unknown')})"
            )

        # Step 7: Add a layer from the source (if datasets available)
        if datasets:
            print("Adding source layer to map...")
            dataset_id = datasets[0]["id"]

            layer_result = add_source_layer(
                map_id=map_id,
                source_layer_params={"from": "dataset", "dataset_id": dataset_id},
            )

            self.assertIsNotNone(layer_result)
            print("Source layer added successfully")
        else:
            print("No datasets available to add as layers")

        print(
            f"\nSources test completed successfully! Source ID: {source_id}, Map URL: {map_resp['url']}"
        )


if __name__ == "__main__":
    unittest.main()
