# Changelog for ndx-events

## 0.4.0 (2025-07-23)

Breaking changes:
- Removed previous implementations of `EventTypesTable`, `TTLTypesTable`, `TTLsTable`, `Task`
- Added new data types `TimestampVectorData`, `DurationVectorData`, `EventTypesTable`, `EventsTable`, `TTLTypesTable`, `TTLsTable`, `Task`.
- Added new data types `CategoricalVectorData` and `MeaningsTable`.
- Moved the `EventsTable` to be stored under the path "/events" in the NWB File. Use the new temporary type `NdxEventsNWBFile` to create a new NWB file with the updated structure.

## 0.2.1 (2025-01-13)
- Replaced deprecated call to `call_docval_func` in various `__init__` functions.

## 0.2.0 (2020-10-20)
- Created new data types for `Events`, `LabeledEvents`, and `TTLs` for acquired data, and `AnnotatedEvents` for processed event data.
