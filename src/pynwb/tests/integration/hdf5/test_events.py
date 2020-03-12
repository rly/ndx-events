import numpy as np

from pynwb.testing import AcquisitionH5IOMixin, TestCase

from ndx_events import Events, LabeledEvents, TTLs, AnnotatedEvents


class TestEventsIO(AcquisitionH5IOMixin, TestCase):

    def setUpContainer(self):
        """ Return the test Events to read/write """
        events = Events(
            name='my_events',
            description='events from my experiment',
            timestamps=[0., 1., 2.],
            resolution=1e-5
        )
        return events


class TestLabeledEventsIO(AcquisitionH5IOMixin, TestCase):

    def setUpContainer(self):
        """ Return the test Events to read/write """
        labeled_events = LabeledEvents(
            name='my_events',
            description='events from my experiment',
            timestamps=[0., 1., 2.],
            resolution=1e-5,
            label_keys=np.uint([3, 4, 3]),
            labels=['', '', '', 'event1', 'event2']
        )
        return labeled_events


class TestTTLs(AcquisitionH5IOMixin, TestCase):

    def setUpContainer(self):
        """ Return the test Events to read/write """
        ttls = TTLs(
            name='my_events',
            description='events from my experiment',
            timestamps=[0., 1., 2.],
            resolution=1e-5,
            label_keys=np.uint([3, 4, 3]),
            labels=['', '', '', 'event1', 'event2']
        )
        return ttls


class TestAnnotatedEventsIO(AcquisitionH5IOMixin, TestCase):
    """ Test adding AnnotatedEvents into acquisition and accessing AnnotatedEvents after read """

    def setUpContainer(self):
        """ Return the test AnnotatedEvents to read/write """
        events = AnnotatedEvents(
            name='my_annotated_events',
            description='annotated events from my experiment',
            resolution=1e-5
        )
        events.add_column(
            name='extra',
            description='extra metadata for each event type'
        )
        events.add_event_type(
            label='Reward',
            event_description='Times when the animal received juice reward.',
            event_times=[1., 2., 3.],
            extra='extra',
            id=3
        )
        events.add_event_type(
            label='Nosepoke',
            event_description='Times when the animal poked its noise through the input port.',
            event_times=[1., 2., 3.],
            extra='extra',
            id=5
        )
        return events
