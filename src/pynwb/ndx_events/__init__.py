import os
from pynwb import load_namespaces

try:
    from importlib.resources import files
except ImportError:
    # TODO: Remove when python 3.9 becomes the new minimum
    from importlib_resources import files

# Get path to the namespace.yaml file with the expected location when installed not in editable mode
__location_of_this_file = files(__name__)
__spec_path = __location_of_this_file / "spec" / "ndx-events.namespace.yaml"

# If that path does not exist, we are likely running in editable mode. Use the local path instead
if not os.path.exists(__spec_path):
    __spec_path = __location_of_this_file.parent.parent.parent / "spec" / "ndx-events.namespace.yaml"

# Load the namespace
load_namespaces(str(__spec_path))

# Define the new classes
from .events import (
    TimestampVectorData,
    DurationVectorData,
    CategoricalVectorData,
    MeaningsTable,
    EventsTable,
    NdxEventsNWBFile,
)


from .ndx_events_nwb_file_io import NdxEventsNWBFileMap


# Remove these functions from the package
del load_namespaces
