import numpy as np

from pynwb import register_class
from pynwb.core import NWBDataInterface, DynamicTable
from hdmf.utils import docval, getargs, popargs, call_docval_func, get_docval


@register_class('Events', 'ndx-events')
class Events(NWBDataInterface):
    """
    A list of timestamps, stored in seconds, of an event.
    """

    __nwbfields__ = ('description',
                     'timestamps',
                     'resolution',
                     {'name': 'unit', 'settable': False})

    @docval({'name': 'name', 'type': str, 'doc': 'The name of this Events object'},  # required
            {'name': 'description', 'type': str, 'doc': 'The name of this Events object'},  # required
            {'name': 'timestamps', 'type': ('array_data', 'data'),  # required
             'doc': ('Event timestamps, in seconds, relative to the common experiment master-clock '
                     'stored in NWBFile.timestamps_reference_time.'),
             'shape': (None,)},
            {'name': 'resolution', 'type': float,
             'doc': ('The smallest possible difference between two event times. Usually 1 divided '
                     'by the event time sampling rate on the data acquisition system.'),
             'default': None})
    def __init__(self, **kwargs):
        description, timestamps, resolution = popargs('description', 'timestamps', 'resolution', kwargs)
        call_docval_func(super().__init__, kwargs)
        self.description = description
        self.timestamps = timestamps
        self.resolution = resolution
        self.fields['unit'] = 'seconds'


@register_class('LabeledEvents', 'ndx-events')
class LabeledEvents(Events):
    """
    A list of timestamps, stored in seconds, of an event that can have different
    labels. For example, this type could represent the times that reward was given,
    as well as which of three different types of reward was given. In this case, the
    'label_keys' dataset would contain values {0, 1, 2}, and the 'labels' dataset
    would contain three text elements, where the first (index 0) specifies the name
    of the reward associated with a label_keys = 0, the second (index 1) specifies
    the name of the reward associated with a label_keys = 1, etc. The labels do not
    have to start at 0 and do not need to be sequential, e.g. the 'label_keys' dataset
    could contain values {0, 10, 100}, and the 'labels' dataset could contain 101
    values, where labels[0] is 'No reward', labels[10] is '10% reward', labels[100]
    is 'Full reward', and all other entries in 'labels' are the empty string.
    """

    __nwbfields__ = ('label_keys',
                     'labels')

    @docval(*get_docval(Events.__init__, 'name', 'description', 'timestamps'),  # required
            {'name': 'label_keys', 'type': ('array_data', 'data'),  # required
             'doc': ("Integer labels that map onto strings using the mapping in the 'labels' dataset. "
                     "Values must be 0 or greater and need not be sequential. This dataset should "
                     "have the same number of elements as the 'timestamps' dataset."),
             'shape': (None,)},
            {'name': 'labels', 'type': ('array_data', 'data'),
             'doc': ("Mapping from an integer (the zero-based index) to a string, used to understand "
                     "the integer values in the 'label_keys' dataset. Use an empty string to represent "
                     "a label value that is not mapped to any text. Use '' to represent any values "
                     "that are None or empty. If the argument is not specified, the label "
                     "will be set to the string representation of the label keys and '' for other values."),
             'shape': (None,), 'default': None},
            *get_docval(Events.__init__, 'resolution'))
    def __init__(self, **kwargs):
        timestamps = getargs('timestamps', kwargs)
        label_keys, labels = popargs('label_keys', 'labels', kwargs)
        call_docval_func(super().__init__, kwargs)
        if len(timestamps) != len(label_keys):
            raise ValueError('Timestamps and label_keys must have the same length: %d != %d'
                             % (len(timestamps), len(label_keys)))
        self.label_keys = label_keys
        if labels is None:
            unique_keys = np.unique(label_keys)
            self.labels = [''] * (max(unique_keys) + 1)
            for k in unique_keys:
                self.labels[k] = str(k)
        else:
            if None in labels:
                raise ValueError("None values are not allowed in the labels array. Please use '' for undefined label "
                                 "keys.")
            self.labels = labels


@register_class('TTLs', 'ndx-events')
class TTLs(LabeledEvents):
    """
    Data type to hold timestamps of TTL pulses. The 'label_keys' dataset contains
    the integer pulse values, and the 'labels' dataset contains user-defined labels
    associated with each pulse value. The value at index n of the 'labels' dataset
    corresponds to a pulse value of n. For example, the first value (index 0) of the
    'labels' dataset corresponds to a pulse value of 0. See the LabeledEvents type
    for more details.
    """
    pass


@register_class('AnnotatedEvents', 'ndx-events')
class AnnotatedEvents(DynamicTable):
    """
    Table to hold event timestamps and event metadata relevant to data preprocessing
    and analysis. Each row corresponds to a different event type. Use the 'event_time'
    dataset to store timestamps for each event type. Add user-defined columns to add
    metadata for each event type or event time.
    """

    __fields__ = (
        'resolution',
    )

    __columns__ = (
        {'name': 'event_times', 'description': 'Event times for each event type.', 'index': True},
        {'name': 'label', 'description': 'Label for each event type.'},
        {'name': 'event_description', 'description': 'Description for each event type.'}
        # note that the name 'description' cannot be used because it is already an attribute on VectorData
    )

    @docval({'name': 'description', 'type': str, 'doc': 'Description of what is in this table'},
            {'name': 'name', 'type': str, 'doc': 'Name of this AnnotatedEvents table', 'default': 'AnnotatedEvents'},
            {'name': 'resolution', 'type': float,
             'doc': ('The smallest possible difference between two event times. Usually 1 divided '
                     'by the event time sampling rate on the data acquisition system.'),
             'default': None},
            *get_docval(DynamicTable.__init__, 'id', 'columns', 'colnames'))
    def __init__(self, **kwargs):
        resolution = popargs('resolution', kwargs)
        call_docval_func(super().__init__, kwargs)
        self.resolution = resolution

    @docval({'name': 'label', 'type': str, 'doc': 'Label for each event type.'},
            {'name': 'event_description', 'type': str, 'doc': 'Description for each event type.'},
            {'name': 'event_times', 'type': 'array_data', 'doc': 'Event times for each event type.', 'shape': (None,)},
            {'name': 'id', 'type': int, 'doc': 'ID for each unit', 'default': None},
            allow_extra=True)
    def add_event_type(self, **kwargs):
        """Add an event type as a row to this table."""
        super().add_row(**kwargs)
