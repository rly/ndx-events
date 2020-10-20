import datetime
import numpy as np
from pynwb import NWBFile, NWBHDF5IO
from pynwb.testing import AcquisitionH5IOMixin, TestCase, remove_test_file

from ndx_events import Events, LabeledEvents, TTLs, AnnotatedEventsTable


class TestEventsIOSimple(TestCase):
    """Simple roundtrip test for CSD."""

    def setUp(self):
        self.nwbfile = NWBFile(
            session_description='session_description',
            identifier='identifier',
            session_start_time=datetime.datetime.now(datetime.timezone.utc)
        )
        self.path = 'test.nwb'

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):
        """
        Add a CSD to an "ecephys" processing module in the NWBFile, write it to file, read the file, and test that the
        CSD from the file matches the original CSD.
        """

        events = Events(
            name='Events',
            description='events from my experiment',
            timestamps=[0., 1., 2.],
            resolution=1e-5
        )
        self.nwbfile.add_acquisition(events)

        labeled_events = LabeledEvents(
            name='LabeledEvents',
            description='events from my experiment',
            timestamps=[0., 1., 2.],
            resolution=1e-5,
            data=np.uint([3, 4, 3]),
            labels=['', '', '', 'event1', 'event2']
        )
        self.nwbfile.add_acquisition(labeled_events)

        ttls = TTLs(
            name='TTLs',
            description='events from my experiment',
            timestamps=[0., 1., 2.],
            resolution=1e-5,
            data=np.uint([3, 4, 3]),
            labels=['', '', '', 'event1', 'event2']
        )
        self.nwbfile.add_acquisition(ttls)

        annotated_events = AnnotatedEventsTable(
            name='AnnotatedEventsTable',
            description='annotated events from my experiment',
            resolution=1e-5
        )
        annotated_events.add_column(
            name='extra',
            description='extra metadata for each event type'
        )
        annotated_events.add_event_type(
            label='Reward',
            event_description='Times when the animal received juice reward.',
            event_times=[1., 2., 3.],
            extra='extra',
            id=3
        )
        annotated_events.add_event_type(
            label='Nosepoke',
            event_description='Times when the animal poked its noise through the input port.',
            event_times=[1., 2., 3.],
            extra='extra',
            id=5
        )

        events_module = self.nwbfile.create_processing_module(
            name='events',
            description='processed events data'
        )
        events_module.add(annotated_events)

        with NWBHDF5IO(self.path, mode='w') as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode='r', load_namespaces=True) as io:
            read_nwbfile = io.read()
            self.assertContainerEqual(events, read_nwbfile.acquisition['Events'])
            self.assertContainerEqual(labeled_events, read_nwbfile.acquisition['LabeledEvents'])
            self.assertContainerEqual(ttls, read_nwbfile.acquisition['TTLs'])
            self.assertContainerEqual(annotated_events, read_nwbfile.processing['events']['AnnotatedEventsTable'])


class TestEventsIO(AcquisitionH5IOMixin, TestCase):

    def setUpContainer(self):
        """ Return the test Events to read/write """
        events = Events(
            name='Events',
            description='events from my experiment',
            timestamps=[0., 1., 2.],
            resolution=1e-5
        )
        return events


class TestLabeledEventsIO(AcquisitionH5IOMixin, TestCase):

    def setUpContainer(self):
        """ Return the test Events to read/write """
        labeled_events = LabeledEvents(
            name='LabeledEvents',
            description='events from my experiment',
            timestamps=[0., 1., 2.],
            resolution=1e-5,
            data=np.uint([3, 4, 3]),
            labels=['', '', '', 'event1', 'event2']
        )
        return labeled_events


class TestTTLs(AcquisitionH5IOMixin, TestCase):

    def setUpContainer(self):
        """ Return the test Events to read/write """
        ttls = TTLs(
            name='TTLs',
            description='events from my experiment',
            timestamps=[0., 1., 2.],
            resolution=1e-5,
            data=np.uint([3, 4, 3]),
            labels=['', '', '', 'event1', 'event2']
        )
        return ttls


class TestAnnotatedEventsTableIO(AcquisitionH5IOMixin, TestCase):
    """ Test adding AnnotatedEventsTable into acquisition and accessing AnnotatedEvents after read """

    def setUpContainer(self):
        """ Return the test AnnotatedEventsTable to read/write """
        annotated_events = AnnotatedEventsTable(
            name='AnnotatedEventsTable',
            description='annotated events from my experiment',
            resolution=1e-5
        )
        annotated_events.add_column(
            name='extra',
            description='extra metadata for each event type'
        )
        annotated_events.add_event_type(
            label='Reward',
            event_description='Times when the animal received juice reward.',
            event_times=[1., 2., 3.],
            extra='extra',
            id=3
        )
        annotated_events.add_event_type(
            label='Nosepoke',
            event_description='Times when the animal poked its noise through the input port.',
            event_times=[1., 2., 3.],
            extra='extra',
            id=5
        )
        return annotated_events
