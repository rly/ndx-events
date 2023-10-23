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

    # events = NWBGroupSpec(
    #     neurodata_type_def='Events',
    #     neurodata_type_inc='NWBDataInterface',
    #     doc=("A simple list of timestamps, stored in seconds, of an event type. For example, this neurodata type "
    #          "could be used to store all the times that a nosepoke was detected. The name may be set to "
    #          "'nosepoke_onset'."),
    #     attributes=[
    #         NWBAttributeSpec(
    #             name='description',
    #             dtype='text',
    #             doc='Description of the event type.',
    #         ),
    #     ],
    #     datasets=[
    #         NWBDatasetSpec(
    #             name='timestamps',
    #             dtype='float32',
    #             dims=['num_events'],
    #             shape=[None],
    #             doc=('Event timestamps, in seconds, relative to the common experiment master-clock stored in '
    #                 'NWBFile.timestamps_reference_time.'),
    #             attributes=[
    #                 NWBAttributeSpec(
    #                     name='unit',
    #                     dtype='text',
    #                     value='seconds',
    #                     doc="Unit of measurement for timestamps, which is fixed to 'seconds'.",
    #                 ),
    #                 NWBAttributeSpec(
    #                     name='resolution',
    #                     dtype='float32',
    #                     doc=('The smallest possible difference between two event times. Usually 1 divided by the '
    #                         'event time sampling rate on the data acquisition system.'),
    #                     required=False,
    #                 ),
    #             ],
    #         ),
    #     ],
    # )

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
            NWBDatasetSpec(
                name='hed_tags',
                neurodata_type_inc='VectorData',
                dtype='text',
                dims=['num_tags'],
                shape=[None],
                doc=("Optional column containing the Hierarchical Event Descriptor (HED) tags for each event type."),
                quantity="?",
            ),
            NWBDatasetSpec(
                name='hed_tags_index',
                neurodata_type_inc='VectorIndex',
                dims=['num_events'],
                shape=[None],
                doc=("Index column for `hed_tags` column."),
                quantity="?",
            ),
        ],
        attributes=[  # override required description attribute from DynamicTable
            NWBAttributeSpec(
                name='description',
                dtype='text',
                doc='Description of the event types table.',
                default_value="Metadata about event types.",
                required=True,
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
                neurodata_type_inc='VectorData',
                dtype='float32',
                dims=['num_events'],
                shape=[None],
                doc=("The time that the event occurred, in seconds, from the session start time."),
                attributes=[
                    NWBAttributeSpec(
                        name='unit',
                        dtype='text',
                        value='seconds',
                        doc="Unit of measurement for timestamps, which is fixed to 'seconds'.",
                    ),
                    NWBAttributeSpec(
                        name='resolution',
                        dtype='float32',
                        doc=('The smallest possible difference between two event times. Usually 1 divided by the '
                            'event time sampling rate on the data acquisition system.'),
                        required=False,
                    ),
                ],
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
                neurodata_type_inc='VectorData',
                dtype='float32',
                dims=['num_events'],
                shape=[None],
                doc=("Optional column containing the duration of each event, in seconds."),
                quantity="?",
            ),
            NWBDatasetSpec(
                name='hed_tags',
                neurodata_type_inc='VectorData',
                dtype='text',
                dims=['num_tags'],
                shape=[None],
                doc=("Optional column containing the Hierarchical Event Descriptor (HED) tags for each event. "
                     "HED tags should be used at the event type level, not at the event instance level, when "
                     "possible, unless it is important to annotate events individually."),
                quantity="?",
            ),
            NWBDatasetSpec(
                name='hed_tags_index',
                neurodata_type_inc='VectorIndex',
                dims=['num_events'],
                shape=[None],
                doc=("Index column for `hed_tags` column."),
                quantity="?",
            ),
        ],
        attributes=[  # override required description attribute from DynamicTable
            NWBAttributeSpec(
                name='description',
                dtype='text',
                doc='Description of the events table.',
                default_value="Metadata about events.",
                required=True,
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
                doc=("The type of TTL that occured. This is represented as a reference "
                     "to a row of the TtlTypesTable."),
            ),
        ],
    )

    new_data_types = [event_types_table, events_table, ttl_types_table, ttls_table]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
