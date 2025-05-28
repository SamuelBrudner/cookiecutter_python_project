"""Pytest configuration and fixtures."""

import pytest
from pathlib import Path


@pytest.fixture(scope="session")
def test_data_dir() -> Path:
    """Return the path to the test data directory."""
    return Path(__file__).parent / "data"


@pytest.fixture(autouse=True)
def setup_logging():
    """Configure logging for tests."""
    import logging
    logging.basicConfig(level=logging.INFO)
    # Disable logging for test runs
    logging.disable(logging.CRITICAL)
    yield
    # Re-enable logging after tests complete
    logging.disable(logging.NOTSET)
