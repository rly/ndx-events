"""Evaluate examples of how to use the ndx-events extension."""

import subprocess
from pathlib import Path


def test_example_usage_write_ttls_events():
    """Call examples/write_ttls_events.py and check that it runs without errors."""
    subprocess.run(["python", "examples/write_ttls_events.py"], check=True)

    # Remove the generated test_events.nwb if it exists
    if Path("test_events.nwb").exists():
        Path("test_events.nwb").unlink()
