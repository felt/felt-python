"""
End-to-end test for the Felt Elements functionality.
Uses the felt_python library to test elements creation, listing, updating, and grouping operations.
"""

import os
import sys
import unittest
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from felt_python import (
    create_map,
    list_elements,
    list_element_groups,
    get_element_group,
    upsert_elements,
    upsert_element_groups,
)


class FeltElementsTest(unittest.TestCase):
    """Test the Felt API elements functionality."""

    def setUp(self):
        if not os.environ.get("FELT_API_TOKEN"):
            self.skipTest("FELT_API_TOKEN environment variable not set")

        # Generate timestamp for unique resource names
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    def test_elements_workflow(self):
        """Test the complete workflow for element operations."""
        # Step 1: Create a map to work with
        map_name = f"Elements Test Map ({self.timestamp})"
        print(f"Creating map: {map_name}...")

        response = create_map(
            title=map_name,
            lat=40,
            lon=-3,
            zoom=8,
            public_access="private",
        )

        self.assertIsNotNone(response)
        self.assertIn("id", response)
        map_id = response["id"]
        print(f"Created map with ID: {map_id}")
        print(f"Map URL: {response['url']}")

        # Step 2: Create elements (points in Madrid and Barcelona)
        print("Creating elements...")
        geojson_feature_collection = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [-3.70379, 40.416775]},
                    "properties": {"name": "Madrid"},
                },
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [2.173403, 41.385063]},
                    "properties": {"name": "Barcelona"},
                },
            ],
        }

        elements_response = upsert_elements(map_id, geojson_feature_collection)

        self.assertIsNotNone(elements_response)
        self.assertEqual(elements_response["type"], "FeatureCollection")
        self.assertEqual(len(elements_response["features"]), 2)
        print(f"Created {len(elements_response['features'])} elements")

        # Step 3: List all elements
        print("Listing all elements...")

        elements = list_elements(map_id)

        self.assertIsNotNone(elements)
        self.assertEqual(elements["type"], "FeatureCollection")
        self.assertEqual(len(elements["features"]), 2)
        print(f"Found {len(elements['features'])} elements")

        # Step 4: Update an element (Barcelona with blue color)
        print("Updating Barcelona element...")
        barcelona_element = next(
            el for el in elements["features"] if el["properties"]["name"] == "Barcelona"
        )
        barcelona_element_id = barcelona_element["properties"]["felt:id"]

        barcelona_element["properties"]["felt:color"] = "#0000FF"
        barcelona_feature_collection = {
            "type": "FeatureCollection",
            "features": [barcelona_element],
        }

        update_response = upsert_elements(map_id, barcelona_feature_collection)

        self.assertIsNotNone(update_response)

        # Verify the update by listing elements again
        updated_elements = list_elements(map_id)

        for element in updated_elements["features"]:
            if element["properties"]["name"] == "Barcelona":
                self.assertEqual(element["properties"]["felt:color"], "#0000FF")
                print("Barcelona element successfully updated with blue color")
                break

        # Step 5: Create element groups
        print("Creating element groups...")
        element_groups = [
            {"name": "Spanish cities", "symbol": "monument", "color": "#A02CFA"},
            {"name": "Parks", "symbol": "tree", "color": "#00AA55"},
        ]

        created_groups = upsert_element_groups(map_id, element_groups)

        self.assertIsNotNone(created_groups)
        self.assertEqual(len(created_groups), 2)
        print(f"Created {len(created_groups)} element groups")

        # Step 6: List element groups
        print("Listing element groups...")

        all_groups = list_element_groups(map_id)

        self.assertIsNotNone(all_groups)
        self.assertEqual(len(all_groups), 2)
        print(f"Found {len(all_groups)} element groups")

        # Step 7: Add elements to a group
        print("Adding elements to Spanish cities group...")
        cities_group_id = all_groups[0]["id"]

        # Update all elements to add them to the Spanish cities group
        for feature in elements["features"]:
            feature["properties"]["felt:parentId"] = cities_group_id

        group_update_response = upsert_elements(map_id, elements)

        self.assertIsNotNone(group_update_response)

        # Step 8: List elements in a specific group
        print(f"Listing elements in group: {cities_group_id}...")

        group_elements = get_element_group(map_id, cities_group_id)

        self.assertIsNotNone(group_elements)
        self.assertEqual(len(group_elements["features"]), 2)
        print(f"Found {len(group_elements['features'])} elements in the group")

        # Step 9: Create elements directly with group assignment
        print("Creating park elements with direct group assignment...")
        parks_group_id = all_groups[1]["id"]

        parks_geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [-3.6762, 40.4153]},
                    "properties": {
                        "name": "Retiro Park",
                        "felt:parentId": parks_group_id,
                    },
                },
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [2.1526, 41.3851]},
                    "properties": {
                        "name": "Parc de la Ciutadella",
                        "felt:parentId": parks_group_id,
                    },
                },
            ],
        }

        parks_response = upsert_elements(map_id, parks_geojson)

        self.assertIsNotNone(parks_response)
        self.assertEqual(len(parks_response["features"]), 2)

        # Verify elements were added to the parks group
        parks_group_elements = get_element_group(map_id, parks_group_id)

        self.assertEqual(len(parks_group_elements["features"]), 2)
        print(
            f"Created and assigned {len(parks_group_elements['features'])} elements to Parks group"
        )

        print(f"\nElements test completed successfully! Map URL: {response['url']}")


if __name__ == "__main__":
    unittest.main()
