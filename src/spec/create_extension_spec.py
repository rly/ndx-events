# -*- coding: utf-8 -*-

import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBAttributeSpec
from pynwb.spec import NWBDatasetSpec


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        doc="""NWB extension for storing timestamped event and TTL pulse data""",
        name="""ndx-events""",
        version="""0.2.0""",
        author=list(map(str.strip, """Ryan Ly""".split(','))),
        contact=list(map(str.strip, """rly@lbl.gov""".split(',')))
    )

    ns_builder.include_type('NWBDataInterface', namespace='core')
    ns_builder.include_type('DynamicTable', namespace='core')
    ns_builder.include_type('VectorData', namespace='core')
    ns_builder.include_type('VectorIndex', namespace='core')

    timestamps = NWBDatasetSpec(
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
                doc=('The smallest possible difference between two event times. Usually 1 divided by the event time '
                     'sampling rate on the data acquisition system.'),
                required=False,
            )
        ]
    )

    events = NWBGroupSpec(
        neurodata_type_def='Events',
        neurodata_type_inc='NWBDataInterface',
        doc='A list of timestamps, stored in seconds, of an event.',
        attributes=[
            NWBAttributeSpec(
                name='description',
                dtype='text',
                doc='Description of the event.',
            ),
        ],
        datasets=[timestamps]
    )

    labels = NWBAttributeSpec(
        name='labels',
        dtype='text',
        dims=['num_labels'],
        shape=[None],
        doc=("Mapping from an unsigned integer (the zero-based index) to a string, used to understand the "
             "values in the 'data' dataset. Use an empty string to represent a label value that is not "
             "mapped to any text."),
    )

    data = NWBDatasetSpec(
        name='data',
        dtype='uint8',
        dims=['num_events'],
        shape=[None],
        doc=("Unsigned integer labels that map onto strings using the mapping in the 'labels' array attribute. This "
             "dataset should have the same number of elements as the 'timestamps' dataset."),
        attributes=[labels],
    )

    labeled_events = NWBGroupSpec(
        neurodata_type_def='LabeledEvents',
        neurodata_type_inc='Events',
        doc=("A list of timestamps, stored in seconds, of an event that can have different labels. For example, "
             "this type could represent the times that reward was given, as well as which of three different "
             "types of reward was given. In this case, the 'data' dataset would contain values {0, 1, 2}, "
             "its 'labels' attribute would contain three text elements, where the first (index 0) specifies the "
             "name of the reward associated with data = 0, the second (index 1) specifies the name of the "
             "reward associated with data = 1, etc. The labels do not have to start at 0 and do not need to "
             "be continuous, e.g. the 'data' dataset could contain values {0, 10, 100}, and the 'labels' "
             "attribute could contain 101 values, where labels[0] is 'No reward', labels[10] is '10% reward', "
             "labels[100] is 'Full reward', and all other entries in 'labels' are the empty string."),
        datasets=[data],
    )

    ttls = NWBGroupSpec(
        neurodata_type_def='TTLs',
        neurodata_type_inc='LabeledEvents',
        doc=("Data type to hold timestamps of TTL pulses. The 'data' dataset contains the integer pulse values "
             "(or channel IDs), and the 'labels' dataset contains user-defined labels associated with each pulse "
             "value (or channel ID). The value at index i of the 'labels' dataset corresponds to a pulse value (or "
             "channel ID) of i in the 'data' dataset. For example, the first value (index 0) of the 'labels' dataset "
             "corresponds to a pulse value of 0. See the LabeledEvents type for more details."),
    )

    event_times_index = NWBDatasetSpec(
        name='event_times_index',
        neurodata_type_inc='VectorIndex',
        doc=('Index into the event_times dataset.'),
    )

    event_times = NWBDatasetSpec(
        name='event_times',
        neurodata_type_inc='VectorData',
        dtype='float32',
        doc='Event times for each event type.',
        attributes=[
            NWBAttributeSpec(
                name='resolution',
                dtype='float32',
                doc=('The smallest possible difference between two event times. Usually 1 divided by the event time '
                     'sampling rate on the data acquisition system.'),
                required=False,
            ),
        ],
    )

    label_col = NWBDatasetSpec(
        name='label',
        neurodata_type_inc='VectorData',
        dtype='text',
        doc='Label for each event type.',
    )

    description_col = NWBDatasetSpec(
        name='event_description',
        neurodata_type_inc='VectorData',
        dtype='text',
        doc='Description for each event type.',
    )

    annotated_events_table = NWBGroupSpec(
        neurodata_type_def='AnnotatedEventsTable',
        neurodata_type_inc='DynamicTable',
        doc=("Table to hold event timestamps and event metadata relevant to data preprocessing and analysis. Each "
             "row corresponds to a different event type. Use the 'event_times' dataset to store timestamps for each "
             "event type. Add user-defined columns to add metadata for each event type or event time."),
        datasets=[event_times_index, event_times, label_col, description_col],
    )

    new_data_types = [events, labeled_events, ttls, annotated_events_table]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
