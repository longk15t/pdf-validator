"""
Pytest fixtures — starts the Flask app on localhost before the test session
and tears it down afterwards.
"""
import os
import time
import threading
import shutil

import pytest
import requests as http_requests

# Ensure we can import app from the project root
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import app  # noqa: E402

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------
TEST_PORT = 5099  # Use a non-default port so it doesn't collide with dev server
TEST_HOST = "127.0.0.1"
BASE_URL = f"http://{TEST_HOST}:{TEST_PORT}"


# --------------------------------------------------------------------------
# Output directory for test-generated PDFs
# --------------------------------------------------------------------------
TEST_OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "output"
)


@pytest.fixture(scope="session", autouse=True)
def flask_server():
    """
    Session-scoped fixture that starts the Flask app in a background thread
    before all tests run and tears it down afterwards.
    """
    # Overwrite the OUTPUT_DIR in the app module so it writes to our known path
    import app as app_module
    app_module.OUTPUT_DIR = os.path.abspath(TEST_OUTPUT_DIR)
    os.makedirs(app_module.OUTPUT_DIR, exist_ok=True)

    # Start Flask in a daemon thread
    server_thread = threading.Thread(
        target=lambda: app.run(
            host=TEST_HOST,
            port=TEST_PORT,
            debug=False,
            use_reloader=False,
        ),
        daemon=True,
    )
    server_thread.start()

    # Wait until the server is actually reachable
    for _ in range(30):
        try:
            http_requests.get(f"{BASE_URL}/", timeout=1)
            break
        except http_requests.ConnectionError:
            time.sleep(0.3)
    else:
        pytest.fail("Flask server did not start within the timeout period.")

    yield BASE_URL

    # Daemon thread will be killed when the process exits — no explicit teardown needed.


@pytest.fixture()
def clean_output_dir():
    """
    Per-test fixture that ensures the output/ directory is clean before
    a test runs and leaves the generated files for inspection afterwards.
    """
    import app as app_module
    output_dir = os.path.abspath(app_module.OUTPUT_DIR)
    # Remove existing PDF if present
    pdf_path = os.path.join(output_dir, "insurance_confirmation.pdf")
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    yield pdf_path
