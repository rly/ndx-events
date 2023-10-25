from hdmf.common import DynamicTable
from pynwb import NWBHDF5IO
from pynwb.testing import TestCase, remove_test_file
from pynwb.testing.mock.file import mock_NWBFile

from ndx_events import EventsTable, EventTypesTable, Task, DurationVectorData, TimestampVectorData


class TestTimestampVectorData(TestCase):

    def test_init(self):
        data = TimestampVectorData(name="test", description="description")
        assert data.name == "test"
        assert data.description == "description"
        assert data.unit == "seconds"

    def test_add_to_dynamic_table(self):
        col = TimestampVectorData(name="test", description="description")
        table = DynamicTable(name="table", description="test", columns=[col])
        table.add_row(test=0.1)
        assert table.test is col
        assert table.test[0] == 0.1


class TestTimestampVectorDataSimpleRoundtrip(TestCase):
    """Simple roundtrip test for TimestampVectorData."""

    def setUp(self):
        self.path = "test.nwb"

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):
        """
        Create a TimestampVectorData, write it to file, read the file, and test that the read object matches the
        original.
        """
        col = TimestampVectorData(name="test", description="description")
        table = DynamicTable(name="table", description="description", columns=[col])
        table.add_row(test=0.1)

        nwbfile = mock_NWBFile()
        nwbfile.add_acquisition(table)

        with NWBHDF5IO(self.path, mode="w") as io:
            io.write(nwbfile)

        with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            read_col = read_nwbfile.acquisition["table"]["test"]
            assert isinstance(read_col, TimestampVectorData)
            assert read_col.name == "test"
            assert read_col.description == "description"
            assert read_col.unit == "seconds"
            assert read_col[0] == 0.1


class TestDurationVectorData(TestCase):

    def test_init(self):
        data = DurationVectorData(name="test", description="description")
        assert data.name == "test"
        assert data.description == "description"
        assert data.unit == "seconds"

    def test_add_to_dynamic_table(self):
        col = DurationVectorData(name="test", description="description")
        table = DynamicTable(name="table", description="test", columns=[col])
        table.add_row(test=0.1)
        assert table.test is col
        assert table.test[0] == 0.1


class TestDurationVectorDataSimpleRoundtrip(TestCase):
    """Simple roundtrip test for DurationVectorData."""

    def setUp(self):
        self.path = "test.nwb"

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):
        """
        Create a DurationVectorData, write it to file, read the file, and test that the read object matches the
        original.
        """
        col = DurationVectorData(name="test", description="description")
        table = DynamicTable(name="table", description="description", columns=[col])
        table.add_row(test=0.1)

        nwbfile = mock_NWBFile()
        nwbfile.add_acquisition(table)

        with NWBHDF5IO(self.path, mode="w") as io:
            io.write(nwbfile)

        with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            read_col = read_nwbfile.acquisition["table"]["test"]
            assert isinstance(read_col, DurationVectorData)
            assert read_col.name == "test"
            assert read_col.description == "description"
            assert read_col.unit == "seconds"
            assert read_col[0] == 0.1


class TestTask(TestCase):

    def test_init(self):
        task = Task()
        assert task.name == "task"

    def test_add_to_nwbfile(self):
        nwbfile = mock_NWBFile()
        task = Task()
        nwbfile.add_lab_meta_data(task)
        assert nwbfile.get_lab_meta_data("task") is task
        assert nwbfile.lab_meta_data["task"] is task


class TestTaskSimpleRoundtrip(TestCase):
    """Simple roundtrip test for Task."""

    def setUp(self):
        self.path = "test.nwb"

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):
        """
        Create a Task, write it to file, read the file, and test that the read object matches the original.
        """
        task = Task()
        nwbfile = mock_NWBFile()
        nwbfile.add_lab_meta_data(task)

        with NWBHDF5IO(self.path, mode="w") as io:
            io.write(nwbfile)

        with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            assert isinstance(read_nwbfile.get_lab_meta_data("task"), Task)
            assert read_nwbfile.get_lab_meta_data("task").name == "task"
            assert read_nwbfile.lab_meta_data["task"].name == "task"


class TestEventTypesTable(TestCase):

    def test_init(self):
        event_types_table = EventTypesTable(description="Metadata about event types")
        assert event_types_table.name == "EventTypesTable"
        assert event_types_table.description == "Metadata about event types"

    def test_init_name(self):
        event_types_table = EventTypesTable(name="event_types", description="Metadata about event types")
        assert event_types_table.name == "event_types"
        assert event_types_table.description == "Metadata about event types"

    def test_add_row(self):
        event_types_table = EventTypesTable(description="Metadata about event types")
        event_types_table.add_row(
            event_name="cue on",
            event_type_description="Times when the cue was on screen.",
        )
        event_types_table.add_row(
            event_name="stimulus on",
            event_type_description="Times when the stimulus was on screen.",
        )
        assert event_types_table["event_name"].data == ["cue on", "stimulus on"]
        assert event_types_table["event_type_description"].data == [
            "Times when the cue was on screen.",
            "Times when the stimulus was on screen.",
        ]


class TestEventTypesTableSimpleRoundtrip(TestCase):
    """Simple roundtrip test for EventTypesTable."""

    def setUp(self):
        self.path = "test.nwb"

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):
        """
        Create an EventTypesTable, write it to file, read the file, and test that the read table matches the original.
        """
        # NOTE that when adding an EventTypesTable to a Task, the EventTypesTable
        # must be named "event_types" according to the spec
        event_types_table = EventTypesTable(name="event_types", description="Metadata about event types")
        event_types_table.add_row(
            event_name="cue on",
            event_type_description="Times when the cue was on screen.",
        )
        event_types_table.add_row(
            event_name="stimulus on",
            event_type_description="Times when the stimulus was on screen.",
        )
        task = Task()
        task.event_types = event_types_table
        nwbfile = mock_NWBFile()
        nwbfile.add_lab_meta_data(task)

        with NWBHDF5IO(self.path, mode="w") as io:
            io.write(nwbfile)

        with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            read_event_types_table = read_nwbfile.get_lab_meta_data("task").event_types
            assert isinstance(read_event_types_table, EventTypesTable)
            assert read_event_types_table.name == "event_types"
            assert read_event_types_table.description == "Metadata about event types"
            assert all(read_event_types_table["event_name"].data[:] == ["cue on", "stimulus on"])
            assert all(
                read_event_types_table["event_type_description"].data[:] == [
                    "Times when the cue was on screen.",
                    "Times when the stimulus was on screen.",
                ]
            )


class TestEventsTable(TestCase):

    def test_init(self):
        events_table = EventsTable(description="Metadata about events")
        assert events_table.name == "EventsTable"
        assert events_table.description == "Metadata about events"

    def test_init_dtr(self):
        event_types_table = EventTypesTable(description="Metadata about event types")
        event_types_table.add_row(
            event_name="cue on",
            event_type_description="Times when the cue was on screen.",
            # hed_tags=["Sensory-event", "(Intended-effect, Cue)"],
        )
        event_types_table.add_row(
            event_name="stimulus on",
            event_type_description="Times when the stimulus was on screen.",
            # hed_tags=["Sensory-event", "Experimental-stimulus", "Visual-presentation", "Image", "Face"],
        )

        events_table = EventsTable(description="Metadata about events", target_tables={"event_type": event_types_table})
        assert events_table["event_type"].table is event_types_table

    def test_add_row(self):
        event_types_table = EventTypesTable(description="Metadata about event types")
        event_types_table.add_row(
            event_name="cue on",
            event_type_description="Times when the cue was on screen.",
            # hed_tags=["Sensory-event", "(Intended-effect, Cue)"],
        )
        event_types_table.add_row(
            event_name="stimulus on",
            event_type_description="Times when the stimulus was on screen.",
            # hed_tags=["Sensory-event", "Experimental-stimulus", "Visual-presentation", "Image", "Face"],
        )

        events_table = EventsTable(description="Metadata about events", target_tables={"event_type": event_types_table})
        events_table.add_row(
            timestamp=0.1,
            value="white circle",
            event_type=0,
            duration=0.2,
            # hed_tags=["(White, Circle)"],
        )
        events_table.add_row(
            timestamp=1.1,
            value="green square",
            event_type=0,
            duration=0.15,
            # hed_tags=["(Green, Square)"],
        )
        assert events_table["timestamp"].data == [0.1, 1.1]
        assert events_table["value"].data == ["white circle", "green square"]
        assert events_table["duration"].data == [0.2, 0.15]
        # assert events_table["hed_tags"][0] == ["(White, Circle)"]
        # assert events_table["hed_tags"][1] == ["(Green, Square)"]


## TODO: TestEventsTableSimpleRoundtrip



# class TestEventsTable(TestCase):

#     def test_init(self):
#         event_types_table = EventTypesTable()
#         events = EventsTable(
#             name='EventsTable',
#             description='events from my experiment',
#             timestamps=[0., 1., 2.],
#             resolution=1e-5
#         )
#         self.assertEqual(events.name, 'Events')
#         self.assertEqual(events.description, 'events from my experiment')
#         self.assertEqual(events.timestamps, [0., 1., 2.])
#         self.assertEqual(events.resolution, 1e-5)
#         self.assertEqual(events.unit, 'seconds')


# class TestLabeledEvents(TestCase):

#     def test_init(self):
#         events = LabeledEvents(
#             name='LabeledEvents',
#             description='events from my experiment',
#             timestamps=[0., 1., 2.],
#             resolution=1e-5,
#             data=np.uint([3, 4, 3]),
#             labels=['', '', '', 'event1', 'event2']
#         )
#         self.assertEqual(events.name, 'LabeledEvents')
#         self.assertEqual(events.description, 'events from my experiment')
#         self.assertEqual(events.timestamps, [0., 1., 2.])
#         self.assertEqual(events.resolution, 1e-5)
#         self.assertEqual(events.unit, 'seconds')
#         np.testing.assert_array_equal(events.data, np.uint([3, 4, 3])),
#         self.assertEqual(events.labels, ['', '', '', 'event1', 'event2'])

#     def test_mismatch_length(self):
#         msg = 'Timestamps and data must have the same length: 3 != 4'
#         with self.assertRaisesWith(ValueError, msg):
#             LabeledEvents(
#                 name='LabeledEvents',
#                 description='events from my experiment',
#                 timestamps=[0., 1., 2.],
#                 resolution=1e-5,
#                 data=np.uint([3, 4, 3, 5]),
#                 labels=['', '', '', 'event1', 'event2', 'event3']
#             )

#     def test_default_labels(self):
#         events = LabeledEvents(
#             name='LabeledEvents',
#             description='events from my experiment',
#             timestamps=[0., 1., 2.],
#             resolution=1e-5,
#             data=np.uint([3, 4, 3]),
#         )
#         self.assertEqual(events.labels, ['', '', '', '3', '4'])

#     def test_none_in_labels(self):
#         msg = "None values are not allowed in the labels array. Please use '' for undefined labels."
#         with self.assertRaisesWith(ValueError, msg):
#             LabeledEvents(
#                 name='LabeledEvents',
#                 description='events from my experiment',
#                 timestamps=[0., 1., 2.],
#                 resolution=1e-5,
#                 data=np.uint([3, 4, 3]),
#                 labels=[None, None, None, 'event1', 'event2']
#             )

#     def test_data_negative(self):
#         msg = "Negative values are not allowed in 'data'."
#         with self.assertRaisesWith(ValueError, msg):
#             LabeledEvents(
#                 name='LabeledEvents',
#                 description='events from my experiment',
#                 timestamps=[0., 1., 2.],
#                 resolution=1e-5,
#                 data=[1, -2, 3],
#                 labels=['', '', '', 'event1', 'event2']
#             )

#     def test_data_int_conversion(self):
#         le = LabeledEvents(
#             name='LabeledEvents',
#             description='events from my experiment',
#             timestamps=[0., 1., 2.],
#             resolution=1e-5,
#             data=[1, 2, 3],
#             labels=['', '', '', 'event1', 'event2']
#         )
#         np.testing.assert_array_equal(le.data, np.array([1, 2, 3]))
#         self.assertEqual(le.data.dtype, np.uint)

#     def test_data_string(self):
#         msg = ("'data' must be an array of numeric values that have type unsigned int or "
#                "can be converted to unsigned int, not type <U1")
#         with self.assertRaisesWith(ValueError, msg):
#             LabeledEvents(
#                 name='LabeledEvents',
#                 description='events from my experiment',
#                 timestamps=[0., 1., 2.],
#                 resolution=1e-5,
#                 data=['1', '2', '3'],
#                 labels=['', '', '', 'event1', 'event2']
#             )

#     def test_data_pass_through(self):
#         data = [1.0, 2.0, 3.0]
#         le = LabeledEvents(
#             name='LabeledEvents',
#             description='events from my experiment',
#             timestamps=[0., 1., 2.],
#             resolution=1e-5,
#             data=data,
#             labels=['', '', '', 'event1', 'event2']
#         )
#         self.assertIs(le.data, data)


# class TestTTLs(TestCase):

#     def test_init(self):
#         events = TTLs(
#             name='TTLs',
#             description='ttl pulses from my experiment',
#             timestamps=[0., 1., 2.],
#             resolution=1e-5,
#             data=np.uint([3, 4, 3]),
#             labels=['', '', '', 'event1', 'event2']
#         )
#         self.assertEqual(events.name, 'TTLs')
#         self.assertEqual(events.description, 'ttl pulses from my experiment')
#         self.assertEqual(events.timestamps, [0., 1., 2.])
#         self.assertEqual(events.resolution, 1e-5)
#         self.assertEqual(events.unit, 'seconds')
#         np.testing.assert_array_equal(events.data, np.uint([3, 4, 3])),
#         self.assertEqual(events.labels, ['', '', '', 'event1', 'event2'])


# class TestAnnotatedEventsTable(TestCase):

#     def test_init(self):
#         events = AnnotatedEventsTable(
#             name='AnnotatedEventsTable',
#             description='annotated events from my experiment',
#             resolution=1e-5
#         )
#         self.assertEqual(events.name, 'AnnotatedEventsTable')
#         self.assertEqual(events.description, 'annotated events from my experiment')
#         self.assertEqual(events.resolution, 1e-5)

#     def test_add_event_type(self):
#         events = AnnotatedEventsTable(
#             name='AnnotatedEventsTable',
#             description='annotated events from my experiment'
#         )
#         events.add_event_type(
#             label='Reward',
#             event_description='Times when the animal received juice reward.',
#             event_times=[1., 2., 3.],
#             id=3
#         )
#         events.add_event_type(
#             label='Abort',
#             event_description='Times when the animal aborted the trial.',
#             event_times=[0.5, 4.5],
#             id=4
#         )
#         self.assertEqual(events.id.data, [3, 4])
#         self.assertEqual(events['event_times'][0], [1., 2., 3.])
#         self.assertEqual(events['event_times'][1], [0.5, 4.5])
#         self.assertEqual(events['label'][0], 'Reward')
#         self.assertEqual(events['label'][1], 'Abort')
#         self.assertListEqual(events['event_description'].data, ['Times when the animal received juice reward.',
#                                                                 'Times when the animal aborted the trial.'])
#         self.assertEqual(events.colnames, ('event_times', 'label', 'event_description'))
#         self.assertEqual(len(events.columns), 4)
#         self.assertEqual(events.columns[0].name, 'event_times_index')
#         self.assertIsInstance(events.columns[0], VectorIndex)
#         self.assertIs(events.columns[0].target, events.columns[1])
#         self.assertEqual(events.columns[1].name, 'event_times')
#         self.assertIsInstance(events.columns[1], VectorData)
#         self.assertEqual(events.columns[2].name, 'label')
#         self.assertIsInstance(events.columns[2], VectorData)
#         self.assertEqual(events.columns[3].name, 'event_description')
#         self.assertIsInstance(events.columns[3], VectorData)
#         self.assertEqual(events.resolution, None)
