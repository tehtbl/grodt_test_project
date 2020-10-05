"""Mocks used for testing."""

import httmock


@httmock.urlmatch(netloc=r"api\.myapp\.org$", path=r"^api/v1/versions/", method="get")
def api_versions(url, request):
    """Simulate versions check."""
    return {
        "status_code": 200,
        "content": [
            {"name": "grodt_test_project", "version": "0.1.0"},
        ]
    }
