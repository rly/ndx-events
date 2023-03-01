# -*- coding: utf-8 -*-

import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBAttributeSpec, NWBDatasetSpec, NWBLinkSpec


def main():
    ns_builder = NWBNamespaceBuilder(
        doc="""NWB extension for storing timestamped event and TTL pulse data""",
        name="""ndx-events""",
        version="""0.3.0""",
        author=list(map(str.strip, """Ryan Ly""".split(','))),
        contact=list(map(str.strip, """rly@lbl.gov""".split(',')))
    )

    ns_builder.include_type('NWBDataInterface', namespace='core')
    ns_builder.include_type('DynamicTable', namespace='core')
    ns_builder.include_type('VectorData', namespace='core')
    ns_builder.include_type('VectorIndex', namespace='core')

    events = NWBGroupSpec(
        neurodata_type_def='Events',
        neurodata_type_inc='NWBDataInterface',
        doc=("A list of timestamps, stored in seconds, of an event type. For example, this neurodata type could be "
             "used to store all the times that a nosepoke was detected. The name may be set to 'nosepoke_onset'"),
        attributes=[
            NWBAttributeSpec(
                name='description',
                dtype='text',
                doc='Description of the event type.',
            ),
        ],
        datasets=[
            NWBDatasetSpec(
                name='timestamps',
                dtype='float32',
                dims=['num_events'],
                shape=[None],
                doc=('Event timestamps, in seconds, relative to the common experiment master-clock stored in '
                    'NWBFile.timestamps_reference_time.'),
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
                    )
                ],
            ),
        ],
    )

    event_types_table = NWBGroupSpec(
        neurodata_type_def="EventTypesTable",
        neurodata_type_inc='DynamicTable',
        doc=("Labels and other metadata associated with each event type."),
        datasets=[
            NWBDatasetSpec(
                name='label',
                neurodata_type_inc='VectorData',
                dtype='text',
                doc='Label for each event type.',
            ),
        ],
    )

    labeled_events = NWBGroupSpec(
        neurodata_type_def='LabeledEvents',
        neurodata_type_inc='Events',
        doc=("Event timestamps that can have different labels and other metadata. "
             "For example, "
             "this type could represent the times that reward was given, as well as which of three different "
             "types of reward was given. In this case, the 'data' dataset would contain unique values {0, 1, 2}, and "
             "the 'labels' table would contain three rows, one for each unique data value, and two columns: 'label', "
             "which stores a unique name for each event type, and a custom column 'reward_type', which stores "
             "information about the type of reward given. The values in row with index i would represent the reward "
             "associated with a data value of i. For example, 'timestamps' may contain values [0, 0.05, 0.15, 0.2], "
             "'data' may contain values [0, 1, 0, 2], and the 'labels' table may contain three rows, where the row "
             "at index 0 has label='"
             "Users may specify custom columns "
             "in the 'labels' table to store arbitrary metadata associated with each event type. "
             "The values in the 'data' dataset do not have to be continuous and start at 0, "
             "but this is recommended so that there are not empty rows in the 'labels' table."),
        links=[
            NWBLinkSpec(
                name="event_types",
                target_type='EventTypesTable',
                doc=("Labels and other metadata associated with each event type, as accessed by row index."),
            )
        ],
        datasets=[
            NWBDatasetSpec(
                name='data',
                dtype='uint8',
                dims=['num_events'],
                shape=[None],
                doc=("Unsigned integer labels that map onto row indices in the 'event_types' table. This "
                    "dataset should have the same number of elements as the 'timestamps' dataset."),
            ),
        ],
    )

    ttl_types_table = NWBGroupSpec(
        neurodata_type_def="TTLTypesTable",
        neurodata_type_inc='EventTypesTable',
        doc=("Labels and other metadata associated with each event type."),
        datasets=[
            NWBDatasetSpec(
                name='label',
                neurodata_type_inc='VectorData',
                dtype='text',
                doc='Label for each event type.',
            ),
            NWBDatasetSpec(
                name='pulse_value',
                neurodata_type_inc='VectorData',
                dtype='int8',
                doc='TTL pulse value for each event type.',
            ),
        ],
    )

    ttls = NWBGroupSpec(
        neurodata_type_def='TTLs',
        neurodata_type_inc='LabeledEvents',
        doc=("Data type to hold timestamps of TTL pulses."),
        links=[
            NWBLinkSpec(
                name="event_types",
                target_type='TTLTypesTable',
                doc=("Labels and other metadata associated with each event type, as accessed by row index."),
            )
        ],
    )

    new_data_types = [events, event_types_table, labeled_events, ttl_types_table, ttls]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
