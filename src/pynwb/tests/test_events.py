from hdmf.common import DynamicTable
import numpy as np
from pynwb import NWBHDF5IO
from pynwb.testing import TestCase, remove_test_file
from pynwb.testing.mock.file import mock_NWBFile

from ndx_events import (
    EventsTable,
    EventTypesTable,
    TtlsTable,
    TtlTypesTable,
    Task,
    DurationVectorData,
    TimestampVectorData,
)


class TestTimestampVectorData(TestCase):
    def test_init(self):
        data = TimestampVectorData(name="test", description="description")
        assert data.name == "test"
        assert data.description == "description"
        assert data.unit == "seconds"
        assert data.resolution is None

    def test_add_to_dynamic_table(self):
        col = TimestampVectorData(name="test", description="description")
        table = DynamicTable(name="table", description="test", columns=[col])
        table.add_row(test=0.1)
        assert table.test is col
        assert table.test[0] == 0.1

    def test_set_resolution_init(self):
        data = TimestampVectorData(name="test", description="description", resolution=1 / 32000.0)
        assert data.resolution == 1 / 32000.0

    def test_set_resolution_attr(self):
        data = TimestampVectorData(name="test", description="description")
        data.resolution = 1 / 32000.0
        assert data.resolution == 1 / 32000.0


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
                read_event_types_table["event_type_description"].data[:]
                == [
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
        )
        event_types_table.add_row(
            event_name="stimulus on",
            event_type_description="Times when the stimulus was on screen.",
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
        events_table.add_column(name="cue_type", description="The cue type.")
        events_table.add_column(name="stimulus_type", description="The stimulus type.")
        events_table.add_row(
            timestamp=0.1,
            cue_type="white circle",
            stimulus_type="",
            event_type=0,
            duration=0.1,
            # hed_tags=["(White, Circle)"],
        )
        events_table.add_row(
            timestamp=0.3,
            cue_type="",
            stimulus_type="animal",
            event_type=1,
            duration=0.15,
        )
        events_table.add_row(
            timestamp=1.1,
            cue_type="green square",
            stimulus_type="",
            event_type=0,
            duration=0.1,
            # hed_tags=["(Green, Square)"],
        )
        events_table.add_row(
            timestamp=1.3,
            cue_type="",
            stimulus_type="landscape",
            event_type=1,
            duration=0.15,
        )
        assert events_table["timestamp"].data == [0.1, 0.3, 1.1, 1.3]
        assert events_table["cue_type"].data == ["white circle", "", "green square", ""]
        assert events_table["stimulus_type"].data == ["", "animal", "", "landscape"]
        assert events_table["duration"].data == [0.1, 0.15, 0.1, 0.15]
        assert events_table["event_type"].data == [0, 1, 0, 1]
        # assert events_table["hed_tags"][0] == ["(White, Circle)"]
        # assert events_table["hed_tags"][2] == ["(Green, Square)"]


class TestEventsTableSimpleRoundtrip(TestCase):
    """Simple roundtrip test for EventsTable."""

    def setUp(self):
        self.path = "test.nwb"

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):
        """
        Create an EventsTable, write it to file, read the file, and test that the read table matches the original.
        """
        # NOTE that when adding an EventTypesTable to a Task, the EventTypesTable
        # must be named "event_types" according to the spec
        event_types_table = EventTypesTable(name="event_types", description="Metadata about event types")
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
        events_table.add_column(name="cue_type", description="The cue type.")
        events_table.add_column(name="stimulus_type", description="The stimulus type.")
        events_table.add_row(
            timestamp=0.1,
            cue_type="white circle",
            stimulus_type="",
            event_type=0,
            duration=0.1,
            # hed_tags=["(White, Circle)"],
        )
        events_table.add_row(
            timestamp=0.3,
            cue_type="",
            stimulus_type="animal",
            event_type=1,
            duration=0.15,
        )
        events_table.add_row(
            timestamp=1.1,
            cue_type="green square",
            stimulus_type="",
            event_type=0,
            duration=0.1,
            # hed_tags=["(Green, Square)"],
        )
        events_table.add_row(
            timestamp=1.3,
            cue_type="",
            stimulus_type="landscape",
            event_type=1,
            duration=0.15,
        )

        task = Task()
        task.event_types = event_types_table
        nwbfile = mock_NWBFile()
        nwbfile.add_lab_meta_data(task)
        nwbfile.add_acquisition(events_table)

        with NWBHDF5IO(self.path, mode="w") as io:
            io.write(nwbfile)

        with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            read_event_types_table = read_nwbfile.get_lab_meta_data("task").event_types
            read_events_table = read_nwbfile.acquisition["EventsTable"]
            assert isinstance(read_events_table, EventsTable)
            assert read_events_table.name == "EventsTable"
            assert read_events_table.description == "Metadata about events"
            assert all(read_events_table["timestamp"].data[:] == [0.1, 0.3, 1.1, 1.3])
            assert all(read_events_table["cue_type"].data[:] == ["white circle", "", "green square", ""])
            assert all(read_events_table["stimulus_type"].data[:] == ["", "animal", "", "landscape"])
            assert all(read_events_table["duration"].data[:] == [0.1, 0.15, 0.1, 0.15])
            assert all(read_events_table["event_type"].data[:] == [0, 1, 0, 1])
            assert read_events_table["event_type"].table is read_event_types_table


class TestTtlTypesTable(TestCase):
    def test_init(self):
        ttl_types_table = TtlTypesTable(description="Metadata about TTL types")
        assert ttl_types_table.name == "TtlTypesTable"
        assert ttl_types_table.description == "Metadata about TTL types"

    def test_init_name(self):
        ttl_types_table = TtlTypesTable(name="ttl_types", description="Metadata about TTL types")
        assert ttl_types_table.name == "ttl_types"
        assert ttl_types_table.description == "Metadata about TTL types"

    def test_add_row(self):
        ttl_types_table = TtlTypesTable(description="Metadata about TTL types")
        ttl_types_table.add_row(
            event_name="cue on",
            event_type_description="Times when the cue was on screen.",
            pulse_value=np.uint(1),
        )
        ttl_types_table.add_row(
            event_name="stimulus on",
            event_type_description="Times when the stimulus was on screen.",
            pulse_value=np.uint(2),
        )
        assert ttl_types_table["event_name"].data == ["cue on", "stimulus on"]
        assert ttl_types_table["event_type_description"].data == [
            "Times when the cue was on screen.",
            "Times when the stimulus was on screen.",
        ]
        assert all(ttl_types_table["pulse_value"].data == np.uint([1, 2]))


class TestTtlTypesTableSimpleRoundtrip(TestCase):
    """Simple roundtrip test for TtlTypesTable."""

    def setUp(self):
        self.path = "test.nwb"

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):
        """
        Create an TtlTypesTable, write it to file, read the file, and test that the read table matches the original.
        """
        # NOTE that when adding an TtlTypesTable to a Task, the TtlTypesTable
        # must be named "ttl_types" according to the spec
        ttl_types_table = TtlTypesTable(name="ttl_types", description="Metadata about TTL types")
        ttl_types_table.add_row(
            event_name="cue on",
            event_type_description="Times when the cue was on screen.",
            pulse_value=np.uint(1),
        )
        ttl_types_table.add_row(
            event_name="stimulus on",
            event_type_description="Times when the stimulus was on screen.",
            pulse_value=np.uint(2),
        )
        task = Task()
        task.ttl_types = ttl_types_table
        nwbfile = mock_NWBFile()
        nwbfile.add_lab_meta_data(task)

        with NWBHDF5IO(self.path, mode="w") as io:
            io.write(nwbfile)

        with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            read_ttl_types_table = read_nwbfile.get_lab_meta_data("task").ttl_types
            assert isinstance(read_ttl_types_table, EventTypesTable)
            assert read_ttl_types_table.name == "ttl_types"
            assert read_ttl_types_table.description == "Metadata about TTL types"
            assert all(read_ttl_types_table["event_name"].data[:] == ["cue on", "stimulus on"])
            assert all(
                read_ttl_types_table["event_type_description"].data[:]
                == [
                    "Times when the cue was on screen.",
                    "Times when the stimulus was on screen.",
                ]
            )
            assert all(read_ttl_types_table["pulse_value"].data[:] == np.uint([1, 2]))


class TestTtlsTable(TestCase):
    def test_init(self):
        ttls_table = TtlsTable(description="Metadata about TTLs")
        assert ttls_table.name == "TtlsTable"
        assert ttls_table.description == "Metadata about TTLs"

    def test_init_dtr(self):
        ttl_types_table = TtlTypesTable(description="Metadata about TTL types")
        ttl_types_table.add_row(
            event_name="cue on",
            event_type_description="Times when the cue was on screen.",
            pulse_value=np.uint(1),
        )
        ttl_types_table.add_row(
            event_name="stimulus on",
            event_type_description="Times when the stimulus was on screen.",
            pulse_value=np.uint(2),
        )

        ttls_table = TtlsTable(description="Metadata about TTLs", target_tables={"ttl_type": ttl_types_table})
        assert ttls_table["ttl_type"].table is ttl_types_table

    def test_add_row(self):
        ttl_types_table = TtlTypesTable(description="Metadata about TTL types")
        ttl_types_table.add_row(
            event_name="cue on",
            event_type_description="Times when the cue was on screen.",
            pulse_value=np.uint(1),
        )
        ttl_types_table.add_row(
            event_name="stimulus on",
            event_type_description="Times when the stimulus was on screen.",
            pulse_value=np.uint(2),
        )

        ttls_table = TtlsTable(description="Metadata about TTLs", target_tables={"ttl_type": ttl_types_table})
        ttls_table.add_row(
            timestamp=0.1,
            ttl_type=0,
        )
        ttls_table.add_row(
            timestamp=1.1,
            ttl_type=0,
        )
        assert ttls_table["timestamp"].data == [0.1, 1.1]
        assert ttls_table["ttl_type"].data == [0, 0]


class TestTtlsTableSimpleRoundtrip(TestCase):
    """Simple roundtrip test for TtlsTable."""

    def setUp(self):
        self.path = "test.nwb"

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):
        """
        Create a TtlsTable, write it to file, read the file, and test that the read table matches the original.
        """
        # NOTE that when adding an TtlTypesTable to a Task, the TtlTypesTable
        # must be named "ttl_types" according to the spec
        ttl_types_table = TtlTypesTable(name="ttl_types", description="Metadata about TTL types")
        ttl_types_table.add_row(
            event_name="cue on",
            event_type_description="Times when the cue was on screen.",
            pulse_value=np.uint(1),
        )
        ttl_types_table.add_row(
            event_name="stimulus on",
            event_type_description="Times when the stimulus was on screen.",
            pulse_value=np.uint(2),
        )

        ttls_table = TtlsTable(description="Metadata about TTLs", target_tables={"ttl_type": ttl_types_table})
        ttls_table.add_row(
            timestamp=0.1,
            ttl_type=0,
        )
        ttls_table.add_row(
            timestamp=1.1,
            ttl_type=0,
        )

        task = Task()
        task.ttl_types = ttl_types_table
        nwbfile = mock_NWBFile()
        nwbfile.add_lab_meta_data(task)
        nwbfile.add_acquisition(ttls_table)

        with NWBHDF5IO(self.path, mode="w") as io:
            io.write(nwbfile)

        with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            read_ttl_types_table = read_nwbfile.get_lab_meta_data("task").ttl_types
            read_ttls_table = read_nwbfile.acquisition["TtlsTable"]
            assert isinstance(read_ttls_table, TtlsTable)
            assert read_ttls_table.name == "TtlsTable"
            assert read_ttls_table.description == "Metadata about TTLs"
            assert all(read_ttls_table["timestamp"].data[:] == [0.1, 1.1])
            assert all(read_ttls_table["ttl_type"].data[:] == [0, 0])
            assert read_ttls_table["ttl_type"].table is read_ttl_types_table
