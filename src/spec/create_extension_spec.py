# -*- coding: utf-8 -*-
import os.path
from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBAttributeSpec, NWBDatasetSpec, NWBRefSpec


def main():
    ns_builder = NWBNamespaceBuilder(
        doc="""NWB extension for storing timestamped event and TTL pulse data""",
        name="""ndx-events""",
        version="""0.4.0""",
        author=["Ryan Ly"],
        contact=["rly@lbl.gov"],
    )

    ns_builder.include_namespace("core")

    timestamp_vector_data = NWBDatasetSpec(
        neurodata_type_def="TimestampVectorData",
        neurodata_type_inc="VectorData",
        doc="A 1-dimensional VectorData that stores timestamps in seconds.",
        dtype="float",
        dims=["num_times"],
        shape=[None],
        attributes=[
            NWBAttributeSpec(
                name="unit",
                dtype="text",
                doc="The unit of measurement for the timestamps, fixed to 'seconds'.",
                value="seconds",
            ),
            # NOTE: alternatively, this could be an attribute of EventsTable instead
            NWBAttributeSpec(
                name="resolution",
                dtype="float",
                doc=(
                    "The smallest possible difference between two timestamps. Usually 1 divided by the "
                    "sampling rate for timestamps of the data acquisition system."
                ),
                required=False,
            ),
        ],
    )

    duration_vector_data = NWBDatasetSpec(
        neurodata_type_def="DurationVectorData",
        neurodata_type_inc="VectorData",
        doc="A 1-dimensional VectorData that stores durations in seconds.",
        dtype="float",
        dims=["num_events"],
        shape=[None],
        attributes=[
            NWBAttributeSpec(
                name="unit",
                dtype="text",
                doc="The unit of measurement for the durations, fixed to 'seconds'.",
                value="seconds",
            ),
            # NOTE: this is probably always the same as the timestamp resolution
            NWBAttributeSpec(
                name="resolution",
                dtype="float",
                doc=(
                    "The smallest possible difference between two timestamps. Usually 1 divided by the "
                    "sampling rate for timestamps of the data acquisition system."
                ),
                required=False,
            ),
        ],
    )

    meanings_table = NWBGroupSpec(
        neurodata_type_def="MeaningsTable",
        neurodata_type_inc="DynamicTable",
        doc=(
            "A table to store information about the meanings of categorical data. Intended to be used as a "
            "lookup table for the meanings of values in a CategoricalVectorData object. All possible values of "
            "the parent CategoricalVectorData object should be present in the 'value' column of this table, even "
            "if the value is not observed in the data. Additional columns may be added to store additional metadata "
            "about each value."
        ),
        datasets=[
            NWBDatasetSpec(
                name="value",
                neurodata_type_inc="VectorData",
                doc="The value of the parent CategoricalVectorData object.",
            ),
            NWBDatasetSpec(
                name="meaning",
                neurodata_type_inc="VectorData",
                dtype="text",
                doc="The meaning of the value in the parent CategoricalVectorData object.",
            ),
        ],
    )

    categorical_vector_data = NWBDatasetSpec(
        neurodata_type_def="CategoricalVectorData",
        neurodata_type_inc="VectorData",
        doc="A 1-dimensional VectorData that stores categorical data of any type. This is an experimental type.",
        dims=["num_events"],
        shape=[None],
        attributes=[
            NWBAttributeSpec(
                # object reference to the meanings table because datasets cannot contain groups
                name="meanings",
                dtype=NWBRefSpec(
                    target_type="MeaningsTable",
                    reftype="object",
                ),
                doc=(
                    "The MeaningsTable object that provides the meanings of the values in this "
                    "CategoricalVectorData object."
                ),
            ),
            NWBAttributeSpec(
                name="filter_values",
                doc=(
                    "Optional dataset containing possible values in the parent data that represent missing or "
                    "invalid values that should be filtered out during analysis. Currently, only string values are "
                    "allowed. "
                    'For example, the filter values may contain the values "undefined" or "None" '
                    "to signal that those values in the data are missing or invalid."
                ),
                dtype="text",  # NOTE: a dtype is required for attributes!
                dims=["num_events"],
                shape=[None],
                required=False,
            ),
        ],
    )

    events_table = NWBGroupSpec(
        neurodata_type_def="EventsTable",
        neurodata_type_inc="DynamicTable",
        doc=(
            "A column-based table to store information about events (event instances), one event per row. "
            "Additional columns may be added to store metadata about each event, such as the duration "
            "of the event."
        ),
        datasets=[
            NWBDatasetSpec(
                name="timestamp",
                neurodata_type_inc="TimestampVectorData",
                doc="Column containing the time that each event occurred, in seconds, from the session start time.",
            ),
            NWBDatasetSpec(
                name="duration",
                neurodata_type_inc="DurationVectorData",
                doc=(
                    "Optional column containing the duration of each event, in seconds. "
                    "A value of NaN can be used for events without a duration or with a duration that is not yet "
                    "specified."
                ),
                quantity="?",
            ),
        ],
        groups=[
            # NOTE: the EventsTable will automatically become a MultiContainerInterface, so adjust the auto-generated
            # class in the extension
            NWBGroupSpec(
                neurodata_type_inc="MeaningsTable",
                doc=(
                    "Lookup tables for the meanings of the values in any CategoricalVectorData columns. "
                    "The name of the table should be the name of the corresponding CategoricalVectorData column "
                    'followed by "_meanings".'
                ),
                quantity="*",
            ),
        ],
        attributes=[
            NWBAttributeSpec(
                name="description",
                dtype="text",
                doc=(
                    "A description of the events stored in the table, including information about "
                    "how the event times were computed, especially if the times are the result of processing or "
                    "filtering raw data. For example, if the experimenter is encoding different types of events using "
                    "a strobed or N-bit encoding, then the description should describe which channels were used and "
                    "how the event time is computed, e.g., as the rise time of the first bit."
                ),
            ),
        ],
    )

    ndx_events_nwb_file = NWBGroupSpec(
        neurodata_type_def="NdxEventsNWBFile",
        neurodata_type_inc="NWBFile",
        doc=(
            "An extension to the NWBFile to store event data. After integration of ndx-events with the core schema, "
            "the NWBFile schema should be updated to this type."
        ),
        groups=[
            NWBGroupSpec(
                name="events",
                doc="Events that occurred during the session.",
                groups=[
                    NWBGroupSpec(
                        neurodata_type_inc="EventsTable",
                        doc="Events that occurred during the session.",
                        quantity="*",
                    ),
                ],
            ),
        ],
    )

    new_data_types = [
        timestamp_vector_data,
        duration_vector_data,
        meanings_table,
        categorical_vector_data,
        events_table,
        ndx_events_nwb_file,
    ]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "spec"))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
