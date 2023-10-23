# def test_example_usage():
#     from datetime import datetime
#     from ndx_events import Events, EventsTable, EventTypesTable
#     from pynwb import NWBFile, NWBHDF5IO

#     nwb = NWBFile(
#         session_description="session description",
#         identifier="cool_experiment_001",
#         session_start_time=datetime.now().astimezone(),
#     )

#     # create a basic events object
#     basic_tone_event = Events(
#         name="tone_onset",
#         timestamps=[0.0, 0.1, 0.3, 0.5, 0.6],
#         description="Times when a tone was played.",
#     )

#     # add the basic events object to the NWBFile object
#     nwb.add_acquisition(basic_tone_event)

#     # create an event types table
#     event_types_table = EventTypesTable(
#         name="EventTypesTable",
#         description="metadata about event types",
#     )

#     # create a new custom column with additional metadata
#     event_types_table.add_column(
#         name="extra_metadata",
#         description="some additional metadata about each event type",
#     )

#     # add event types one by one
#     event_types_table.add_row(
#         id=0, event_name="trial start", extra_metadata="more metadata"
#     )
#     event_types_table.add_row(
#         id=1, event_name="cue onset", extra_metadata="more metadata"
#     )
#     event_types_table.add_row(
#         id=2, event_name="cue offset", extra_metadata="more metadata"
#     )
#     event_types_table.add_row(
#         id=3, event_name="nosepoke left", extra_metadata="more metadata"
#     )
#     event_types_table.add_row(
#         id=4, event_name="nosepoke right", extra_metadata="more metadata"
#     )
#     event_types_table.add_row(id=5, event_name="reward", extra_metadata="more metadata")

#     # add the event types table to the acquisition group for now
#     # it should be added to the /general/tasks group when merged with core
#     nwb.add_acquisition(event_types_table)

#     # create a new EventsTable type to hold events recorded from the data acquisition system
#     events_table = EventsTable(
#         name="EventsTable",
#         description="events from my experiment",
#     )
#     # set the dynamic table region link
#     events_table["event_type"].table = event_types_table

#     # add events one by one
#     events_table.add_row(timestamp=0.1, event_type=0, duration=0.0)
#     events_table.add_row(timestamp=0.3, event_type=1, duration=0.0)
#     events_table.add_row(timestamp=0.4, event_type=2, duration=0.0)
#     events_table.add_row(timestamp=0.8, event_type=4, duration=0.1)
#     events_table.add_row(timestamp=0.85, event_type=5, duration=0.0)

#     # add the EventsTable type to the acquisition group of the NWB file
#     nwb.add_acquisition(events_table)

#     # write nwb file
#     filename = "test.nwb"
#     with NWBHDF5IO(filename, "w") as io:
#         io.write(nwb)

#     # read nwb file and check its contents
#     with NWBHDF5IO(filename, "r", load_namespaces=True) as io:
#         nwb = io.read()
#         print(nwb)
#         # access the events table and event types table by name from the NWBFile acquisition group and print it
#         print(nwb.acquisition["tone_onset"])
#         print(nwb.acquisition["EventTypesTable"])
#         print(nwb.acquisition["EventsTable"])
#         print(nwb.acquisition["EventsTable"].to_dataframe())
#         print(nwb.acquisition["EventsTable"][0, "event_type"])


# if __name__ == "__main__":
#     test_example_usage()
