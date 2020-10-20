# ndx-events Extension for NWB

This is an NWB extension for storing timestamped event data and TTL pulses.

Events can be:
1. **Simple events**. These are stored in the `Events` type. The `Events` type consists of only a name, a description,
and a 1D array of timestamps. This should be used instead of a `TimeSeries` when the time series has no data.
2. **Labeled events**. These are stored in the `LabeledEvents` type. The `LabeledEvents` type expands on the `Events`
type by adding 1) a 1D array of integer values (data) with the same length as the timestamps and 2) a 1D array of
labels (labels) associated with each unique integer value in the data array. The data values are indices into the
array of labels. The `LabeledEvents` type can be used to encode additional information about individual events,
such as the reward values for each reward event.
3. **TTL pulses**. These are stored in the `TTLs` type. The `TTLs` type is a subtype of the `LabeledEvents` type
specifically for TTL pulse data. A single instance should be used for all TTL pulse data. The pulse value (or channel)
should be stored in the 1D data array, and the labels associated with each pulse value (or channel)
should be stored in the 1D array of labels.
4. **Annotated events**. These are stored in the `AnnotatedEventsTable` type. The `AnnotatedEventsTable` type is a
subtype of `DynamicTable`, where each row corresponds to a different event type. The table has a ragged
(variable-length) 1D column of event times, such that each event type (row) is associated with an array of event times.
Unlike for the other event types, users can add their own custom columns to annotate each event type or event time.
This can be useful for storing event metadata related to data preprocessing and analysis, such as marking bad events.

This extension was developed by Ryan Ly, Ben Dichter, Oliver Rübel, and Andrew Tritt. Information about the rationale,
background, and alternative approaches to this extension can be found here:
https://docs.google.com/document/d/1qcsjyFVX9oI_746RdMoDdmQPu940s0YtDjb1en1Xtdw

## Installation

```
pip install ndx-events
```

## Example usage

```python
from datetime import datetime

from pynwb import NWBFile, NWBHDF5IO
from ndx_events import LabeledEvents, AnnotatedEventsTable


nwb = NWBFile(
    session_description='session description',
    identifier='cool_experiment_001',
    session_start_time=datetime.now().astimezone()
)

# create a new LabeledEvents type to hold events recorded from the data acquisition system
events = LabeledEvents(
    name='LabeledEvents',
    description='events from my experiment',
    timestamps=[0., 0.5, 0.6, 2., 2.05, 3., 3.5, 3.6, 4.],
    resolution=1e-5,  # resolution of the timestamps, i.e., smallest possible difference between timestamps
    data=[0, 1, 2, 3, 5, 0, 1, 2, 4],
    labels=['trial_start', 'cue_onset', 'cue_offset', 'response_left', 'response_right', 'reward']
)

# add the LabeledEvents type to the acquisition group of the NWB file
nwb.add_acquisition(events)

# create a new AnnotatedEventsTable type to hold annotated events
annotated_events = AnnotatedEventsTable(
    name='AnnotatedEventsTable',
    description='annotated events from my experiment',
    resolution=1e-5  # resolution of the timestamps, i.e., smallest possible difference between timestamps
)
# add a custom indexed (ragged) column to represent whether each event time was a bad event
annotated_events.add_column(
    name='bad_event',
    description='whether each event time should be excluded',
    index=True
)
# add an event type (row) to the AnnotatedEventsTable instance
annotated_events.add_event_type(
    label='Reward',
    event_description='Times when the subject received juice reward.',
    event_times=[1., 2., 3.],
    bad_event=[False, False, True],
    id=3
)

# create a processing module in the NWB file to hold processed events data
events_module = nwb.create_processing_module(
    name='events',
    description='processed event data'
)

# add the AnnotatedEventsTable instance to the processing module
events_module.add(annotated_events)

# write nwb file
filename = 'test.nwb'
with NWBHDF5IO(filename, 'w') as io:
    io.write(nwb)

# read nwb file and check its contents
with NWBHDF5IO(filename, 'r', load_namespaces=True) as io:
    nwb = io.read()
    print(nwb)
```

This extension was created using [ndx-template](https://github.com/nwb-extensions/ndx-template).
