"""
Unit tests for get_export_link's wait on a slow export. No API token needed.
"""

import io
import json
import os
import sys
import unittest
from unittest import mock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from felt_python import ExportFailedError, ExportTimeoutError, get_export_link

POLL_ENDPOINT = "https://felt.com/api/v2/maps/m/layers/l/custom_exports/e"


def respond(*bodies):
    return mock.patch(
        "felt_python.layers.make_request",
        side_effect=[io.BytesIO(json.dumps(body).encode()) for body in bodies],
    )


class Clock:
    def __init__(self):
        self.now = 0.0
        self.sleeps = []

    def monotonic(self):
        return self.now

    def sleep(self, seconds):
        self.sleeps.append(seconds)
        self.now += seconds


class FeltExportLinkTest(unittest.TestCase):
    def setUp(self):
        self.clock = Clock()
        for name in ("monotonic", "sleep"):
            patcher = mock.patch(
                f"felt_python.layers.time.{name}", getattr(self.clock, name)
            )
            patcher.start()
            self.addCleanup(patcher.stop)

    def test_returns_the_link_when_the_export_is_ready(self):
        with respond({"export_link": "https://files/layer.gpkg"}) as request:
            self.assertEqual(get_export_link("m", "l"), "https://files/layer.gpkg")
        self.assertEqual(request.call_count, 1)

    def test_polls_a_slow_export_until_it_completes(self):
        with respond(
            {"status": "processing", "poll_endpoint": POLL_ENDPOINT},
            {"status": "pending", "download_url": None},
            {"status": "in_progress", "download_url": None},
            {"status": "completed", "download_url": "https://files/layer.gpkg"},
        ) as request:
            self.assertEqual(get_export_link("m", "l"), "https://files/layer.gpkg")
        self.assertEqual(request.call_args.kwargs["url"], POLL_ENDPOINT)
        self.assertEqual(self.clock.sleeps, [2.0, 3.0])

    def test_raises_when_the_export_fails(self):
        with respond(
            {"status": "processing", "poll_endpoint": POLL_ENDPOINT},
            {"status": "failed", "download_url": None},
        ):
            with self.assertRaises(ExportFailedError) as raised:
                get_export_link("m", "l")
        self.assertEqual(raised.exception.poll_endpoint, POLL_ENDPOINT)

    def test_raises_with_the_poll_endpoint_after_the_timeout(self):
        in_progress = {"status": "in_progress", "download_url": None}
        with respond(
            {"status": "processing", "poll_endpoint": POLL_ENDPOINT},
            *[in_progress] * 5,
        ):
            with self.assertRaises(ExportTimeoutError) as raised:
                get_export_link("m", "l", timeout=5)
        self.assertEqual(raised.exception.poll_endpoint, POLL_ENDPOINT)
        self.assertEqual(self.clock.now, 5)


if __name__ == "__main__":
    unittest.main()
