# ndx-events Extension for NWB

This is an NWB extension for storing timestamped event data and TTL pulses.

The latest version is 0.3.0. This is a major change from previous versions.

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

This extension was developed by Ryan Ly, Oliver Rübel, and the NWB Technical Advisory Board.
Information about the rationale, background, and alternative approaches to this extension can be found here:
https://docs.google.com/document/d/1qcsjyFVX9oI_746RdMoDdmQPu940s0YtDjb1en1Xtdw

## Installation
Python:
```bash
pip install -U ndx-events
```

Matlab:
```matlab
generateExtension('<directory path>/ndx-events/spec/ndx-events.namespace.yaml');
```

## Developer installation
In a Python 3.8-3.12 environment:
```bash
pip install -r requirements-dev.txt
pip install -e .
```

Run tests:
```bash
pytest
```

Install pre-commit hooks:
```bash
pre-commit install
```

Style and other checks:
```bash
black .
ruff .
codespell .
```

## Example usage
Python:


This extension was created using [ndx-template](https://github.com/nwb-extensions/ndx-template).
