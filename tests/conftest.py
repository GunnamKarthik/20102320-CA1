# conftest.py - Shared test fixtures used by all test files
# Sets up a fresh temporary database for each test so tests don't affect each other

import pytest
import sys
import os
import tempfile

# Add the project root to the path so we can import app and db
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app
import db as db_module


@pytest.fixture
def client():
    """Create a test client with a fresh temporary database for each test."""
    # Create a temporary file for the test database
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    # Point the db module to the temporary database
    db_module.DATABASE = db_path
    app.config['TESTING'] = True

    with app.test_client() as test_client:
        # Create all tables in the temporary database
        db_module.init_db()
        yield test_client

    # Clean up: close and delete the temporary database file
    os.close(db_fd)
    os.unlink(db_path)
