import os
from pynwb import load_namespaces, get_class

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
Task = get_class("Task", "ndx-events")
TimestampVectorData = get_class("TimestampVectorData", "ndx-events")
DurationVectorData = get_class("DurationVectorData", "ndx-events")
EventTypesTable = get_class("EventTypesTable", "ndx-events")
EventsTable = get_class("EventsTable", "ndx-events")
TtlTypesTable = get_class("TtlTypesTable", "ndx-events")
TtlsTable = get_class("TtlsTable", "ndx-events")

# Remove these functions from the package
del load_namespaces, get_class
