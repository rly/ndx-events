# ndx-events Extension for NWB

## Installation

TODO:
```
pip install ndx-events
```

## Usage

```python
from pynwb import NWBFile, NWBHDF5IO
from ndx_events import LabeledEvents, AnnotatedEvents

from datetime import datetime
import numpy as np

nwb = NWBFile(
    session_description='session_description',
    identifier='identifier',
    session_start_time=datetime.now().astimezone()
)

events = LabeledEvents(
    name='LabeledEvents',
    description='events from my experiment',
    timestamps=[0., 1., 2.],
    resolution=1e-5,
    label_keys=np.uint([3, 4, 3]),
    labels=['', '', '', 'event1', 'event2']
)
nwb.add_acquisition(events)

annotated_events = AnnotatedEvents(
    name='AnnotatedEvents',
    description='annotated events from my experiment',
    resolution=1e-5
)
annotated_events.add_column(
    name='extra',
    description='extra metadata for each event type'
)
annotated_events.add_event_type(
    label='Reward',
    event_description='Times when the animal received juice reward.',
    event_times=[1., 2., 3.],
    extra='extra',
    id=3
)
events_module = nwb.create_processing_module(
    name='events',
    description='processed event data'
)
events_module.add(annotated_events)

# Write nwb file
filename = 'test.nwb'
with NWBHDF5IO(filename, 'w') as io:
    io.write(nwb)

# Read nwb file and check its content
with NWBHDF5IO(filename, 'r', load_namespaces=True) as io:
    nwb = io.read()
    print(nwb)
```

This extension was created using [ndx-template](https://github.com/nwb-extensions/ndx-template).
