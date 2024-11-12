from datetime import datetime
from hdmf.common import DynamicTable
from pynwb import NWBHDF5IO
from pynwb.testing import TestCase, remove_test_file
from pynwb.testing.mock.file import mock_NWBFile

from ndx_events import (
    EventsTable,
    CategoricalVectorData,
    MeaningsTable,
    DurationVectorData,
    TimestampVectorData,
    NdxEventsNWBFile,
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


class TestMeaningsTable(TestCase):
    def test_init(self):
        meanings_table = MeaningsTable(
            name="x_meanings", description="Meanings for values in a CategoricalVectorData object."
        )
        assert meanings_table.name == "x_meanings"
        assert meanings_table.description == "Meanings for values in a CategoricalVectorData object."

    def test_add_row(self):
        meanings_table = MeaningsTable(
            name="x_meanings", description="Meanings for values in a CategoricalVectorData object."
        )
        meanings_table.add_row(value="cue on", meaning="Times when the cue was on screen.")
        assert meanings_table["value"].data == ["cue on"]
        assert meanings_table["meaning"].data == ["Times when the cue was on screen."]


class TestMeaningsTableSimpleRoundtrip(TestCase):
    """Simple roundtrip test for MeaningsTable."""

    def setUp(self):
        self.path = "test.nwb"

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):
        """
        Create a MeaningsTable, write it to file, read the file, and test that the read object matches the
        original.
        """
        meanings_table = MeaningsTable(name="x_meanings", description="Test meanings table.")
        meanings_table.add_row(value="cue on", meaning="Times when the cue was on screen.")
        meanings_table.add_row(value="cue off", meaning="Times when the cue was off screen.")

        # place the meanings table in the acquisition group for testing purposes
        nwbfile = mock_NWBFile()
        nwbfile.add_acquisition(meanings_table)

        with NWBHDF5IO(self.path, mode="w") as io:
            io.write(nwbfile)

        with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            read_meanings_table = read_nwbfile.acquisition["x_meanings"]
            assert isinstance(read_meanings_table, MeaningsTable)
            assert read_meanings_table.name == "x_meanings"
            assert read_meanings_table.description == "Test meanings table."
            assert all(read_meanings_table["value"].data[:] == ["cue on", "cue off"])
            assert all(
                read_meanings_table["meaning"].data[:]
                == ["Times when the cue was on screen.", "Times when the cue was off screen."]
            )


class TestCategoricalVectorData(TestCase):
    def test_init(self):
        meanings_table = MeaningsTable(
            name="categorical_vector_data_meanings",
            description="Meanings for values in a CategoricalVectorData object.",
        )
        categorical_vector_data = CategoricalVectorData(
            name="categorical_vector_data", description="description", data=["a", "b"], meanings=meanings_table
        )
        assert categorical_vector_data.name == "categorical_vector_data"
        assert categorical_vector_data.description == "description"
        assert categorical_vector_data.data == ["a", "b"]
        assert categorical_vector_data.meanings is meanings_table

    def test_init_filter_values(self):
        meanings_table = MeaningsTable(
            name="categorical_vector_data_meanings",
            description="Meanings for values in a CategoricalVectorData object.",
        )
        categorical_vector_data = CategoricalVectorData(
            name="categorical_vector_data",
            description="description",
            data=["a", "b", "undefined"],
            meanings=meanings_table,
            filter_values=["undefined"],
        )
        assert categorical_vector_data.filter_values == ["undefined"]


# NOTE: A roundtrip test for CategoricalVectorData is bundled with the test for EventsTable
# because the CategoricalVectorData object is used in the EventsTable class.
# The MeaningsTable object should be placed in the EventsTable object.


class TestEventsTable(TestCase):
    def test_init(self):
        events_table = EventsTable(name="stimulus_events", description="Metadata about events")
        assert events_table.name == "stimulus_events"
        assert events_table.description == "Metadata about events"

    def test_add_row(self):
        cue_meanings_table = MeaningsTable(
            name="cue_type_meanings", description="Meanings for values in a CategoricalVectorData object."
        )
        stimulus_meanings_table = MeaningsTable(
            name="stimulus_type_meanings", description="Meanings for values in a CategoricalVectorData object."
        )
        columns = [
            CategoricalVectorData(
                name="cue_type", description="The cue type.", meanings=cue_meanings_table, filter_values=["n/a"]
            ),
            CategoricalVectorData(
                name="stimulus_type",
                description="The stimulus type.",
                meanings=stimulus_meanings_table,
                filter_values=["n/a"],
            ),
        ]
        events_table = EventsTable(
            name="stimulus_events", description="Metadata about stimulus events", columns=columns
        )
        events_table.add_row(
            timestamp=0.1,
            duration=0.1,
            cue_type="white circle",
            stimulus_type="n/a",
        )
        events_table.add_row(
            timestamp=0.3,
            duration=0.15,
            cue_type="n/a",
            stimulus_type="animal",
        )
        events_table.add_row(
            timestamp=1.1,
            duration=0.1,
            cue_type="green square",
            stimulus_type="n/a",
        )
        events_table.add_row(
            timestamp=1.3,
            duration=0.15,
            cue_type="n/a",
            stimulus_type="landscape",
        )
        cue_meanings_table.add_row(value="white circle", meaning="Times when the cue was a white circle.")
        cue_meanings_table.add_row(value="green square", meaning="Times when the cue was a green square.")
        stimulus_meanings_table.add_row(value="animal", meaning="Times when the stimulus was an animal.")
        stimulus_meanings_table.add_row(value="landscape", meaning="Times when the stimulus was a landscape.")

        # events_table.add_meanings(cue_meanings_table)
        # events_table.add_meanings(stimulus_meanings_table)

        assert events_table["timestamp"].data == [0.1, 0.3, 1.1, 1.3]
        assert events_table["duration"].data == [0.1, 0.15, 0.1, 0.15]
        assert events_table["cue_type"].data == ["white circle", "n/a", "green square", "n/a"]
        assert events_table["stimulus_type"].data == ["n/a", "animal", "n/a", "landscape"]


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
        cue_meanings_table = MeaningsTable(
            name="cue_type_meanings", description="Meanings for values in a CategoricalVectorData object."
        )
        stimulus_meanings_table = MeaningsTable(
            name="stimulus_type_meanings", description="Meanings for values in a CategoricalVectorData object."
        )
        columns = [
            CategoricalVectorData(
                name="cue_type", description="The cue type.", meanings=cue_meanings_table, filter_values=["n/a"]
            ),
            CategoricalVectorData(
                name="stimulus_type",
                description="The stimulus type.",
                meanings=stimulus_meanings_table,
                filter_values=["n/a"],
            ),
        ]
        meanings_tables = [cue_meanings_table, stimulus_meanings_table]
        events_table = EventsTable(
            name="stimulus_events",
            description="Metadata about stimulus events",
            columns=columns,
            meanings_tables=meanings_tables,
        )
        events_table.add_row(
            timestamp=0.1,
            duration=0.1,
            cue_type="white circle",
            stimulus_type="n/a",
        )
        events_table.add_row(
            timestamp=0.3,
            duration=0.15,
            cue_type="n/a",
            stimulus_type="animal",
        )
        events_table.add_row(
            timestamp=1.1,
            duration=0.1,
            cue_type="green square",
            stimulus_type="n/a",
        )
        events_table.add_row(
            timestamp=1.3,
            duration=0.15,
            cue_type="n/a",
            stimulus_type="landscape",
        )
        cue_meanings_table.add_row(value="white circle", meaning="Times when the cue was a white circle.")
        cue_meanings_table.add_row(value="green square", meaning="Times when the cue was a green square.")
        stimulus_meanings_table.add_row(value="animal", meaning="Times when the stimulus was an animal.")
        stimulus_meanings_table.add_row(value="landscape", meaning="Times when the stimulus was a landscape.")

        nwbfile = NdxEventsNWBFile(
            identifier="test", session_description="test", session_start_time=datetime.now().astimezone()
        )
        nwbfile.add_events_table(events_table)

        with NWBHDF5IO(self.path, mode="w") as io:
            io.write(nwbfile)

        with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            read_events_table = read_nwbfile.events["stimulus_events"]
            assert isinstance(read_events_table, EventsTable)
            assert read_events_table.description == "Metadata about stimulus events"
            assert all(read_events_table["timestamp"].data[:] == [0.1, 0.3, 1.1, 1.3])
            assert all(read_events_table["duration"].data[:] == [0.1, 0.15, 0.1, 0.15])

            read_cue_type = read_events_table["cue_type"]
            assert isinstance(read_cue_type, CategoricalVectorData)
            assert read_cue_type.description == "The cue type."
            assert all(read_cue_type.data[:] == ["white circle", "n/a", "green square", "n/a"])
            assert isinstance(read_cue_type.meanings, MeaningsTable)
            assert read_cue_type.meanings.name == "cue_type_meanings"
            assert read_cue_type.meanings.description == "Meanings for values in a CategoricalVectorData object."
            assert all(read_cue_type.meanings["value"].data[:] == ["white circle", "green square"])
            assert all(
                read_cue_type.meanings["meaning"].data[:]
                == ["Times when the cue was a white circle.", "Times when the cue was a green square."]
            )

            assert all(read_events_table["stimulus_type"].data[:] == ["n/a", "animal", "n/a", "landscape"])
