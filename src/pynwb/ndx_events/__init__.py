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

# TODO: Define your classes here to make them accessible at the package level.
# Either have PyNWB generate a class from the spec using `get_class` as shown
# below or write a custom class and register it using the class decorator
# `@register_class("TetrodeSeries", "ndx-hed")`
Task = get_class("Task", "ndx-events")
TimestampVectorData = get_class("TimestampVectorData", "ndx-events")
DurationVectorData = get_class("DurationVectorData", "ndx-events")
EventTypesTable = get_class("EventTypesTable", "ndx-events")
EventsTable = get_class("EventsTable", "ndx-events")
TtlTypesTable = get_class("TtlTypesTable", "ndx-events")
TtlsTable = get_class("TtlsTable", "ndx-events")

# Remove these functions from the package
del load_namespaces, get_class
