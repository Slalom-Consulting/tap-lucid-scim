"""Tests standard tap features using the built-in SDK tests library."""

#import datetime

# from singer_sdk.testing import get_tap_test_class
from singer_sdk.testing import get_standard_tap_tests

from tests.mock.util import mock_api

from tap_lucid_scim.tap import TapLucidScim

SAMPLE_CONFIG = {
    "auth_token": "SampleApiKey",
}


# Run standard built-in tap tests from the SDK:
#TestTapLucidScim = get_tap_test_class(
#    tap_class=TapLucidScim,
#    config=SAMPLE_CONFIG,
#)

# Run standard built-in tap tests from the SDK:
def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    config = SAMPLE_CONFIG
    tests = get_standard_tap_tests(TapLucidScim, config=config)
    for test in tests:
        if test.__name__ in ("_test_stream_connections"):
            mock_api(test, config)
            continue

        test()

# TODO: Create additional tests as appropriate for your tap.
