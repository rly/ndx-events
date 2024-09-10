# ndx-events Extension for NWB

This is an NWB extension for storing timestamped event data and TTL pulses.

The latest version is 0.3.0. This is a major change from previous versions.

**`EventTypesTable`**: Event types (e.g., lick, reward left, reward right, airpuff, reach) and metadata about them should be stored in an `EventTypesTable` object.
- `EventTypesTable` inherits from `DynamicTable` and stores metadata related to each event type, one per row. 
- An "event_name" text column is required.
- A "event_type_description" text column is required.
- The table allows for an arbitrary number of custom columns to be added for additional metadata for each event type. 
- This table is intended to live in a `Task` object at the path "general/task" in the `NWBFile`.

**`EventsTable`**: Event times and metadata about them should be stored in an `EventsTable` object.
- `EventsTable` inherits from `DynamicTable` and stores metadata related to each event time / instance, one per row.
- A "timestamp" column of type `TimestampVectorData` is required.
- A “duration” column of type `DurationVectorData` is optional. 
- An “event_type” column that is a foreign key reference to a row index of the `EventTypesTable` is required.
- A "value" text column is optional. This enables storage of another layer of events within an event type. This could store different reward sizes or different tone frequencies or other parameterizations of an event. For example, if you have three levels of reward (e.g., 1 drop, 2 drops, 3 drops), instead of encoding each level of reward as its own event type (e.g., "reward_value_1", "reward_value_2", "reward_value_3", you could encode "reward" as the event type, and the value for each event time could be "1", "2", or "3". 
- Because this inherits from `DynamicTable`, users can add additional custom columns to store other metadata.
- This table is intended to live either under the "acquisition" group or in a "behavior" `ProcessingModule`, i.e., under the "processing/behavior" group.

**`TtlTypesTable`**: TTL pulse types and metadata about them should be stored in a `TtlTypesTable` object. 
- `TtlTypesTable` inherits from `EventTypesTable` and stores metadata related to each TTL pulse type, one per row. 
- A "pulse_value" unsigned integer column is required. 
- This table is intended to live in a `Task` object at the path "general/task" in the `NWBFile`.

**`TtlsTable`**: TTL pulses and metadata about them should be stored in a `TtlsTable` object.
- `TtlsTable` inherits from `EventsTable`.
- The "event_type" column inherited from `EventsTable` should refer to the `TtlTypesTable`.
- This table is intended to live either under the "acquisition" group or in a "behavior" `ProcessingModule`, i.e., under the "processing/behavior" group.

This extension defines a few additional neurodata types related to storing events:

**`Task`**: `Task` type is a subtype of the `LabMetaData` type and holds the `EventTypesTable` and `TtlTypesTable`. This allows the `Task` type to be added as a group in the root "general" group. 

**`TimestampVectorData`**: The `TimestampVectorData` type stores a 1D array of timestamps in seconds.
- Values are in seconds from session start time.
- It has a "unit" attribute. The value of the attribute is fixed to "seconds".
- It has a "resolution" attribute that represents the smallest possible difference between two timestamps. Usually 1 divided by the sampling rate for timestamps of the data acquisition system.

**`DurationVectorData`**: The `DurationVectorData` type that stores a 1D array of durations in seconds.
- It is otherwise identical to the `TimestampVectorData` type.

This extension was developed by Ryan Ly, Oliver Rübel, and the NWB Technical Advisory Board.
Information about the rationale, background, and alternative approaches to this extension can be found here:
https://docs.google.com/document/d/1qcsjyFVX9oI_746RdMoDdmQPu940s0YtDjb1en1Xtdw

## Installation

The latest **ndx-events 0.3.0** has not yet been released on PyPI. To install it on Python, use:
```bash
pip install git+https://github.com/rly/ndx-events.git
```

To install the 0.2.0 version, use:
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


This extension was created using [ndx-template](https://github.com/nwb-extensions/ndx-template).
