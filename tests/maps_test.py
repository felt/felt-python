"""
End-to-end test for the Felt Map functionality.
Uses the felt_python library to test the map creation, updates, and other map-related operations.
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
    get_map,
    update_map,
    export_comments,
    resolve_comment,
    delete_comment,
    create_embed_token,
)


class FeltAPITest(unittest.TestCase):
    """Test the Felt API map functionality"""

    def setUp(self):
        if not os.environ.get("FELT_API_TOKEN"):
            self.skipTest("FELT_API_TOKEN environment variable not set")

        # Generate timestamp for unique resource names
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    def test_map_workflow(self):
        """Test the complete workflow for map operations."""
        # Step 1: Create a map with timestamp in name for uniqueness
        map_name = f"Map Test ({self.timestamp})"
        print(f"Creating map: {map_name}...")

        response = create_map(
            title=map_name,
            lat=40.416775,
            lon=-3.70379,  # Madrid coordinates
            zoom=9,
            basemap="light",
            description=f"A test map created using the felt-python test at {self.timestamp}",
            public_access="private",
        )

        self.assertIsNotNone(response)
        self.assertIn("id", response)
        self.assertEqual(response["title"], map_name)

        map_id = response["id"]
        print(f"Map URL: {response['url']}")

        # Step 2: Get map details
        print("Getting map details...")
        map_details = get_map(map_id)

        self.assertIsNotNone(map_details)
        self.assertEqual(map_details["id"], map_id)
        self.assertEqual(map_details["title"], map_name)
        self.assertEqual(map_details["public_access"], "private")

        # Step 3: Update the map
        updated_name = f"Test Map Updated ({self.timestamp})"
        print(f"Updating map to: {updated_name}...")

        updated_map = update_map(
            map_id=map_id,
            title=updated_name,
            description=f"This map was updated through the API test at {self.timestamp}",
            public_access="view_only",
        )

        self.assertIsNotNone(updated_map)

        # Verify update by getting map details again
        updated_details = get_map(map_id)

        self.assertEqual(updated_details["title"], updated_name)
        self.assertEqual(updated_details["public_access"], "view_only")

        # Step 4: Export comments
        # Note: There will be no comments on a newly created map
        print("Exporting comments...")

        comments = export_comments(map_id)

        self.assertIsNotNone(comments)
        self.assertIsInstance(comments, list)
        print(f"Found {len(comments)} comments")

        # Step 5 & 6: If there are comments, resolve and delete one
        # Note: This section will only run if there are comments
        if comments:
            comment_id = comments[0]["id"]

            # Resolve comment
            print(f"Resolving comment {comment_id}...")
            resolve_result = resolve_comment(map_id, comment_id)
            self.assertIsNotNone(resolve_result)
            self.assertEqual(resolve_result["comment_id"], comment_id)

            # Get updated comments to check if the comment was resolved
            updated_comments = export_comments(map_id)
            for comment in updated_comments:
                if comment["id"] == comment_id:
                    self.assertTrue(comment["isResolved"])
                    break

            # Delete comment
            print(f"Deleting comment {comment_id}...")
            delete_comment(map_id, comment_id)

            # Verify comment was deleted
            updated_comments = export_comments(map_id)
            comment_ids = [c["id"] for c in updated_comments]
            self.assertNotIn(comment_id, comment_ids)
        else:
            print("No comments to resolve or delete")

        # Step 7: Create an embed token
        print("Creating embed token...")

        token_data = create_embed_token(
            map_id=map_id, user_email=f"test.user@example.com"
        )

        self.assertIsNotNone(token_data)
        self.assertIn("token", token_data)
        self.assertIn("expires_at", token_data)
        print(f"Created embed token that expires at {token_data['expires_at']}")
        print("\nTest completed successfully!")


if __name__ == "__main__":
    unittest.main()
