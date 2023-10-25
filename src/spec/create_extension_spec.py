# -*- coding: utf-8 -*-
import os.path
from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBAttributeSpec, NWBDatasetSpec


def main():
    ns_builder = NWBNamespaceBuilder(
        doc="""NWB extension for storing timestamped event and TTL pulse data""",
        name="""ndx-events""",
        version="""0.3.0""",
        author=["Ryan Ly"],
        contact=["rly@lbl.gov"],
    )

    ns_builder.include_namespace('core')

    timestamp_vector_data = NWBDatasetSpec(
        neurodata_type_def="TimestampVectorData",
        neurodata_type_inc="VectorData",
        doc="A VectorData that stores timestamps in seconds.",
        dtype="float64",
        dims=['num_times'],
        shape=[None],
        attributes=[
            NWBAttributeSpec(
                name="unit",
                dtype="text",
                doc="The unit of measurement for the timestamps, fixed to 'seconds'.",
                value="seconds",
            ),
            NWBAttributeSpec(
                name="resolution",
                dtype="float64",
                doc=("The smallest possible difference between two timestamps. Usually 1 divided by the "
                     "sampling rate for timestamps of the data acquisition system."),
                required=False,
            ),
        ],
    )

    duration_vector_data = NWBDatasetSpec(
        neurodata_type_def="DurationVectorData",
        neurodata_type_inc="VectorData",
        doc="A VectorData that stores durations in seconds.",
        dtype="float64",
        dims=['num_events'],
        shape=[None],
        attributes=[
            NWBAttributeSpec(
                name="unit",
                dtype="text",
                doc="The unit of measurement for the durations, fixed to 'seconds'.",
                value="seconds",
            ),
            NWBAttributeSpec(
                name="resolution",
                dtype="float64",
                doc=("The smallest possible difference between two timestamps. Usually 1 divided by the "
                     "sampling rate for timestamps of the data acquisition system."),
                required=False,
            ),
        ],
    )

    event_types_table = NWBGroupSpec(
        neurodata_type_def="EventTypesTable",
        neurodata_type_inc='DynamicTable',
        doc=("A column-based table to store information about each event type, such as name, one event type per row."),
        default_name="EventTypesTable",
        datasets=[
            NWBDatasetSpec(
                name='event_name',
                neurodata_type_inc='VectorData',
                dtype='text',
                doc='Name of each event type.',
            ),
            NWBDatasetSpec(
                name='event_type_description',
                neurodata_type_inc='VectorData',
                dtype='text',
                doc='Description of each event type.',
            ),
        ],
    )

    events_table = NWBGroupSpec(
        neurodata_type_def='EventsTable',
        neurodata_type_inc='DynamicTable',
        doc=("A column-based table to store information about events (event instances), one event per row. "
             "Each event must have an event_type, which is a row in the EventTypesTable. Additional columns "
             "may be added to store metadata about each event, such as the duration of the event, or a "
             "text value of the event."),
        default_name="EventsTable",
        datasets=[
            NWBDatasetSpec(
                name='timestamp',
                neurodata_type_inc='TimestampVectorData',
                doc="The time that each event occurred, in seconds, from the session start time.",
            ),
            NWBDatasetSpec(
                name='event_type',
                neurodata_type_inc='DynamicTableRegion',
                dims=['num_events'],
                shape=[None],
                doc=("The type of event that occurred. This is represented as a reference "
                     "to a row of the EventTypesTable."),
            ),
            NWBDatasetSpec(
                name='value',
                neurodata_type_inc='VectorData',
                dtype='text',
                dims=['num_events'],
                shape=[None],
                doc=("Optional column containing the text value of each event."),
                quantity="?",
            ),
            NWBDatasetSpec(
                name='duration',
                neurodata_type_inc='DurationVectorData',
                doc="Optional column containing the duration of each event, in seconds.",
                quantity="?",
            ),
        ],
    )

    ttl_types_table = NWBGroupSpec(
        neurodata_type_def="TtlTypesTable",
        neurodata_type_inc='EventTypesTable',
        doc=("A column-based table to store information about each TTL type, such as name and pulse value, "
             "one TTL type per row."),
        default_name="TtlTypesTable",
        datasets=[
            NWBDatasetSpec(
                name='pulse_value',
                neurodata_type_inc='VectorData',
                dtype='uint8',
                doc='TTL pulse value for each event type.',
            ),
        ],
    )

    ttls_table = NWBGroupSpec(
        neurodata_type_def='TtlsTable',
        neurodata_type_inc='EventsTable',
        doc=("Data type to hold timestamps of TTL pulses."),
        default_name="TtlsTable",
        datasets=[
            NWBDatasetSpec(
                name='event_type',
                neurodata_type_inc='DynamicTableRegion',
                dims=['num_events'],
                shape=[None],
                doc=("The type of TTL that occurred. This is represented as a reference "
                     "to a row of the TtlTypesTable."),
            ),
        ],
    )

    task = NWBGroupSpec(
        neurodata_type_def='Task',
        neurodata_type_inc='LabMetaData',
        doc=("A group to store task-related general metadata. TODO When merged with core, "
             "this will no longer inherit from LabMetaData but from NWBContainer and be placed "
             "optionally in /general."),
        name="task",
        groups=[
            NWBGroupSpec(
                name="event_types",
                neurodata_type_inc="EventTypesTable",
                doc="Table to store information about each task event type.",
                quantity="?",
            ),
        ],
    )

    new_data_types = [timestamp_vector_data, duration_vector_data, event_types_table, events_table, ttl_types_table, ttls_table, task, ]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
