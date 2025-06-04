import os
import json
import time
import socket
import tempfile
import subprocess
import pytest
from tests.test_utils import is_port_open, send_query


@pytest.fixture(scope="module")
def server_setup():
    """Spins up a test server and yields its config for end-to-end tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "data.txt")
        config_file = os.path.join(tmpdir, "config.json")
        
        # Create a test file
        with open(test_file, "w") as f:
            f.write("banana\napple\norange\n")

        # Create config
        port = 12500
        config = {
            "file_path": test_file,
            "REREAD_ON_QUERY": False,
            "SSL_ENABLED": False,
            "port": port,
            "linuxpath": "C:/Windows/System32/findstr.exe"  # Added to fix server start errors
        }
        with open(config_file, "w") as f:
            json.dump(config, f)

        # Start server process
        env = os.environ.copy()
        env["USE_TEST_CONFIG"] = "true"
        env["TEST_CONFIG_PATH"] = config_file

        process = subprocess.Popen(
            ["python", "-m", "server.server"],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Wait for server to start (up to 30 seconds)
        timeout = time.time() + 30
        while not is_port_open(port):
            if time.time() > timeout:
                out, err = process.communicate(timeout=5)
                print("=== SERVER STDOUT ===")
                print(out.decode(errors="ignore"))
                print("=== SERVER STDERR ===")
                print(err.decode(errors="ignore"))
                raise RuntimeError("Server did not start in 30 seconds.")
            time.sleep(0.25)

        yield {"port": port, "process": process}

        # Clean up
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()


def test_server_client_interaction(server_setup):
    """Test end-to-end client/server interaction with valid queries."""
    port = server_setup["port"]
    response = send_query("banana", port)
    assert "STRING EXISTS" in response

    response = send_query("pineapple", port)
    assert "STRING NOT FOUND" in response
