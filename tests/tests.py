"""
Simple test runner for felt-python tests.
"""

import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import test files
from maps_test import FeltAPITest
from elements_test import FeltElementsTest
from layers_test import FeltLayersTest
from layer_groups_test import FeltLayerGroupsTest
from library_test import FeltLibraryTest
from projects_test import FeltProjectsTest
from sources_test import FeltSourcesTest
from delete_test import FeltDeleteTest


if __name__ == "__main__":
    # Check for API token
    if not os.environ.get("FELT_API_TOKEN"):
        print("ERROR: FELT_API_TOKEN environment variable not set")
        print("export FELT_API_TOKEN='your_api_token'")
        sys.exit(1)

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    test_cases = [
        FeltAPITest,
        FeltElementsTest,
        FeltLayersTest,
        FeltLayerGroupsTest,
        FeltLibraryTest,
        FeltProjectsTest,
        FeltSourcesTest,
        FeltDeleteTest,
    ]

    for test_case in test_cases:
        suite.addTests(loader.loadTestsFromTestCase(test_case))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return appropriate exit code
    sys.exit(not result.wasSuccessful())
