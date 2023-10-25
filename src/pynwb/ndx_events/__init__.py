import os
from pynwb import load_namespaces, get_class

# Set path of the namespace.yaml file to the expected install location
ndx_events_specpath = os.path.join(
    os.path.dirname(__file__),
    'spec',
    'ndx-events.namespace.yaml'
)

# If the extension has not been installed yet but we are running directly from
# the git repo
if not os.path.exists(ndx_events_specpath):
    ndx_events_specpath = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        '..', '..', '..',
        'spec',
        'ndx-events.namespace.yaml'
    ))

# Load the namespace
load_namespaces(ndx_events_specpath)

from . import io as __io  # noqa: E402,F401

Task = get_class('Task', 'ndx-events')
TimestampVectorData = get_class('TimestampVectorData', 'ndx-events')
DurationVectorData = get_class('DurationVectorData', 'ndx-events')
EventTypesTable = get_class('EventTypesTable', 'ndx-events')
EventsTable = get_class('EventsTable', 'ndx-events')
TtlTypesTable = get_class('TtlTypesTable', 'ndx-events')
TtlsTable = get_class('TtlsTable', 'ndx-events')
