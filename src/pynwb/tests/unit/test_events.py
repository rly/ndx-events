import numpy as np

from pynwb.testing import TestCase
from pynwb.core import VectorData, VectorIndex

from ndx_events import Events, LabeledEvents, TTLs, AnnotatedEvents


class TestEvents(TestCase):

    def test_init(self):
        events = Events(
            name='Events',
            description='events from my experiment',
            timestamps=[0., 1., 2.],
            resolution=1e-5
        )
        self.assertEqual(events.name, 'Events')
        self.assertEqual(events.description, 'events from my experiment')
        self.assertEqual(events.timestamps, [0., 1., 2.])
        self.assertEqual(events.resolution, 1e-5)
        self.assertEqual(events.unit, 'seconds')


class TestLabeledEvents(TestCase):

    def test_init(self):
        events = LabeledEvents(
            name='LabeledEvents',
            description='events from my experiment',
            timestamps=[0., 1., 2.],
            resolution=1e-5,
            label_keys=np.uint([3, 4, 3]),
            labels=['', '', '', 'event1', 'event2']
        )
        self.assertEqual(events.name, 'LabeledEvents')
        self.assertEqual(events.description, 'events from my experiment')
        self.assertEqual(events.timestamps, [0., 1., 2.])
        self.assertEqual(events.resolution, 1e-5)
        self.assertEqual(events.unit, 'seconds')
        np.testing.assert_array_equal(events.label_keys, np.uint([3, 4, 3])),
        self.assertEqual(events.labels, ['', '', '', 'event1', 'event2'])

    def test_mismatch_length(self):
        msg = 'Timestamps and label_keys must have the same length: 3 != 4'
        with self.assertRaisesWith(ValueError, msg):
            LabeledEvents(
                name='LabeledEvents',
                description='events from my experiment',
                timestamps=[0., 1., 2.],
                resolution=1e-5,
                label_keys=np.uint([3, 4, 3, 5]),
                labels=['', '', '', 'event1', 'event2', 'event3']
            )

    def test_defaultlabels(self):
        events = LabeledEvents(
            name='LabeledEvents',
            description='events from my experiment',
            timestamps=[0., 1., 2.],
            resolution=1e-5,
            label_keys=np.uint([3, 4, 3]),
        )
        self.assertEqual(events.labels, ['', '', '', '3', '4'])

    def test_none_in_labels(self):
        msg = "None values are not allowed in the labels array. Please use '' for undefined label keys."
        with self.assertRaisesWith(ValueError, msg):
            LabeledEvents(
                name='LabeledEvents',
                description='events from my experiment',
                timestamps=[0., 1., 2.],
                resolution=1e-5,
                label_keys=np.uint([3, 4, 3]),
                labels=[None, None, None, 'event1', 'event2']
            )


class TestTTLs(TestCase):

    def test_init(self):
        events = TTLs(
            name='TTLs',
            description='ttl pulses from my experiment',
            timestamps=[0., 1., 2.],
            resolution=1e-5,
            label_keys=np.uint([3, 4, 3]),
            labels=['', '', '', 'event1', 'event2']
        )
        self.assertEqual(events.name, 'TTLs')
        self.assertEqual(events.description, 'ttl pulses from my experiment')
        self.assertEqual(events.timestamps, [0., 1., 2.])
        self.assertEqual(events.resolution, 1e-5)
        self.assertEqual(events.unit, 'seconds')
        np.testing.assert_array_equal(events.label_keys, np.uint([3, 4, 3])),
        self.assertEqual(events.labels, ['', '', '', 'event1', 'event2'])


class TestAnnotatedEvents(TestCase):

    def test_init(self):
        events = AnnotatedEvents(
            name='AnnotatedEvents',
            description='annotated events from my experiment',
            resolution=1e-5
        )
        self.assertEqual(events.name, 'AnnotatedEvents')
        self.assertEqual(events.description, 'annotated events from my experiment')
        self.assertEqual(events.resolution, 1e-5)

    def test_add_event_type(self):
        events = AnnotatedEvents(
            name='AnnotatedEvents',
            description='annotated events from my experiment'
        )
        events.add_event_type(
            label='Reward',
            event_description='Times when the animal received juice reward.',
            event_times=[1., 2., 3.],
            id=3
        )
        events.add_event_type(
            label='Abort',
            event_description='Times when the animal aborted the trial.',
            event_times=[0.5, 4.5],
            id=4
        )
        self.assertEqual(events.id.data, [3, 4])
        self.assertEqual(events['event_times'][0], [1., 2., 3.])
        self.assertEqual(events['event_times'][1], [0.5, 4.5])
        self.assertEqual(events['label'][0], 'Reward')
        self.assertEqual(events['label'][1], 'Abort')
        self.assertListEqual(events['event_description'].data, ['Times when the animal received juice reward.',
                                                                'Times when the animal aborted the trial.'])
        self.assertEqual(events.colnames, ('event_times', 'label', 'event_description'))
        self.assertEqual(len(events.columns), 4)
        self.assertEqual(events.columns[0].name, 'event_times_index')
        self.assertIsInstance(events.columns[0], VectorIndex)
        self.assertIs(events.columns[0].target, events.columns[1])
        self.assertEqual(events.columns[1].name, 'event_times')
        self.assertIsInstance(events.columns[1], VectorData)
        self.assertEqual(events.columns[2].name, 'label')
        self.assertIsInstance(events.columns[2], VectorData)
        self.assertEqual(events.columns[3].name, 'event_description')
        self.assertIsInstance(events.columns[3], VectorData)
        self.assertEqual(events.resolution, None)
