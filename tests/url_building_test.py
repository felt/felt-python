"""
Unit tests for URL construction.

Unlike the rest of the suite these need no API token and make no requests.
"""

import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from felt_python.api import build_query, build_url
from felt_python.comments import COMMENT
from felt_python.layers import LAYER
from felt_python.maps import MAP


class BuildUrlTest(unittest.TestCase):
    def test_ordinary_ids_are_untouched(self):
        """Felt's short slugs and UUIDs contain nothing that needs encoding."""
        for map_id in (
            "PF0ve5FaSWujSB5402D8wD",
            "deadbeef-0000-0000-0000-000000000000",
        ):
            with self.subTest(map_id=map_id):
                self.assertTrue(
                    build_url(MAP, map_id=map_id).endswith(f"/maps/{map_id}")
                )

    def test_space_is_encoded_instead_of_raising(self):
        """Previously http.client raised InvalidURL before sending anything."""
        self.assertTrue(
            build_url(MAP, map_id="not a real id").endswith("/maps/not%20a%20real%20id")
        )

    def test_query_and_fragment_cannot_escape_the_path(self):
        """An id with "?" or "#" used to silently truncate the path."""
        self.assertTrue(build_url(MAP, map_id="abc?x=1").endswith("/maps/abc%3Fx%3D1"))
        self.assertTrue(build_url(MAP, map_id="abc#frag").endswith("/maps/abc%23frag"))

    def test_slash_cannot_add_path_segments(self):
        """safe="" is the point: a "/" in an id must not become a separator."""
        url = build_url(MAP, map_id="../../sources")
        self.assertTrue(url.endswith("/maps/..%2F..%2Fsources"), url)

    def test_each_segment_is_encoded_independently(self):
        url = build_url(LAYER, map_id="a b", layer_id="c/d")
        self.assertTrue(url.endswith("/maps/a%20b/layers/c%2Fd"), url)

    def test_unicode_ids(self):
        self.assertTrue(build_url(MAP, map_id="mapa-ñ").endswith("/maps/mapa-%C3%B1"))

    def test_non_string_values_are_coerced(self):
        self.assertTrue(build_url(MAP, map_id=123).endswith("/maps/123"))

    def test_multi_segment_template(self):
        url = build_url(COMMENT, map_id="m1", comment_id="c1")
        self.assertTrue(url.endswith("/maps/m1/comments/c1"), url)


class BuildQueryTest(unittest.TestCase):
    def test_none_values_are_omitted(self):
        self.assertEqual(
            build_query("https://x/api", workspace_id=None), "https://x/api"
        )

    def test_single_param(self):
        self.assertEqual(
            build_query("https://x/api", workspace_id="w1"),
            "https://x/api?workspace_id=w1",
        )

    def test_values_are_encoded(self):
        """A "+" in an email would otherwise decode server-side as a space."""
        self.assertEqual(
            build_query("https://x/api", user_email="a+b@example.com"),
            "https://x/api?user_email=a%2Bb%40example.com",
        )

    def test_ampersand_cannot_inject_a_parameter(self):
        self.assertEqual(
            build_query("https://x/api", source="felt&admin=true"),
            "https://x/api?source=felt%26admin%3Dtrue",
        )

    def test_appends_to_an_existing_query_string(self):
        self.assertEqual(
            build_query("https://x/api?a=1", b="2"), "https://x/api?a=1&b=2"
        )

    def test_mixed_present_and_absent(self):
        self.assertEqual(
            build_query("https://x/api", a="1", b=None), "https://x/api?a=1"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
