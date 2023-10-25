def test_example_usage():
    from datetime import datetime
    from ndx_events import EventsTable, EventTypesTable, TtlsTable, TtlTypesTable, Task
    import numpy as np
    from pynwb import NWBFile, NWBHDF5IO

    nwbfile = NWBFile(
        session_description="session description",
        identifier="cool_experiment_001",
        session_start_time=datetime.now().astimezone(),
    )

    # in this experiment, TTL pulses were sent by the stimulus computer
    # to signal important time markers during the experiment/trial,
    # when the stimulus was placed on the screen and removed from the screen,
    # when the question appeared, and the responses of the subject.

    # ref: https://www.nature.com/articles/s41597-020-0415-9, DANDI:000004

    # NOTE that when adding an TtlTypesTable to a Task, the TtlTypesTable
    # must be named "ttl_types" according to the spec
    ttl_types_table = TtlTypesTable(name="ttl_types", description="Metadata about TTL types")
    ttl_types_table.add_row(
        event_name="start experiment",
        event_type_description="Start of experiment",
        pulse_value=np.uint(55),
    )
    ttl_types_table.add_row(
        event_name="stimulus onset",
        event_type_description="Stimulus onset",
        pulse_value=np.uint(1),
    )
    ttl_types_table.add_row(
        event_name="stimulus offset",
        event_type_description="Stimulus offset",
        pulse_value=np.uint(2),
    )
    ttl_types_table.add_row(
        event_name="question onset",
        event_type_description="Question screen onset",
        pulse_value=np.uint(3),
    )
    learning_response_description = (
        "During the learning phase, subjects are instructed to respond to the following "
        "question: 'Is this an animal?' in each trial. Response are encoded as 'Yes, this "
        "is an animal' (20) and 'No, this is not an animal' (21)."
    )
    ttl_types_table.add_row(
        event_name="yes response during learning",
        event_type_description=learning_response_description,
        pulse_value=np.uint(20),
    )
    ttl_types_table.add_row(
        event_name="no response during learning",
        event_type_description=learning_response_description,
        pulse_value=np.uint(21),
    )
    recognition_response_description = (
        "During the recognition phase, subjects are instructed to respond to the following "
        "question: 'Have you seen this image before?' in each trial. Responses are encoded "
        "as: 31 (new, confident), 32 (new, probably), 33 (new, guess), 34 (old, guess), 35 "
        "(old, probably), 36 (old, confident)."
    )
    ttl_types_table.add_row(
        event_name="(new, confident) response during recognition",
        event_type_description=recognition_response_description,
        pulse_value=np.uint(31),
    )
    ttl_types_table.add_row(
        event_name="(new, probably) response during recognition",
        event_type_description=recognition_response_description,
        pulse_value=np.uint(32),
    )
    ttl_types_table.add_row(
        event_name="(new, guess) response during recognition",
        event_type_description=recognition_response_description,
        pulse_value=np.uint(33),
    )
    ttl_types_table.add_row(
        event_name="(old, guess) response during recognition",
        event_type_description=recognition_response_description,
        pulse_value=np.uint(34),
    )
    ttl_types_table.add_row(
        event_name="(old, probably) response during recognition",
        event_type_description=recognition_response_description,
        pulse_value=np.uint(35),
    )
    ttl_types_table.add_row(
        event_name="(old, confident) response during recognition",
        event_type_description=recognition_response_description,
        pulse_value=np.uint(36),
    )
    ttl_types_table.add_row(
        event_name="end trial",
        event_type_description="End of trial",
        pulse_value=np.uint(6),
    )
    ttl_types_table.add_row(
        event_name="end experiment",
        event_type_description="End of experiment",
        pulse_value=np.uint(66),
    )

    ttls_table = TtlsTable(description="Metadata about TTLs", target_tables={"ttl_type": ttl_types_table})
    ttls_table.add_row(
        timestamp=6820.092244,
        ttl_type=0,  # NOT the pulse value, but a row index into the ttl_types_table
    )
    ttls_table.add_row(
        timestamp=6821.208244,
        ttl_type=1,
    )
    ttls_table.add_row(
        timestamp=6822.210644,
        ttl_type=2,
    )
    ttls_table.add_row(
        timestamp=6822.711364,
        ttl_type=3,
    )
    ttls_table.add_row(
        timestamp=6825.934244,
        ttl_type=6,
    )
    ttls_table.timestamp.resolution = 1/50000.0  # specify the resolution of the timestamps (optional)

    # if TTLs are recorded, then the events table should hold any non-TTL events
    # recorded by the acquisition system
    # OR the events table can hold more processed information than the TTLs table
    # e.g., converting stimulus onset and offset into a single stimulus event with metadata.
    # this may be redundant with information in the trials table if the task is
    # structured into trials

    # NOTE that when adding an EventTypesTable to a Task, the EventTypesTable
    # must be named "event_types" according to the spec
    event_types_table = EventTypesTable(name="event_types", description="Metadata about event types")
    event_types_table.add_row(
        event_name="stimulus on",
        event_type_description="Times when the stimulus was on screen",
    )

    events_table = EventsTable(description="Metadata about events", target_tables={"event_type": event_types_table})
    events_table.add_column(name="category_name", description="Name of the category of the stimulus")
    events_table.add_column(
        name="stimulus_image_index",
        description="Frame index of the stimulus image in the StimulusPresentation object"
    )
    events_table.add_row(
        timestamp=6821.208244,
        category_name="smallAnimal",
        stimulus_image_index=0,
        event_type=0,
        duration=1.0024,  # this comes from the stimulus onset and offset TTLs
    )
    events_table.add_row(
        timestamp=6821.208244,
        category_name="phones",
        stimulus_image_index=1,
        event_type=0,
        duration=0.99484,
    )
    events_table.timestamp.resolution = 1/50000.0  # specify the resolution of the timestamps (optional)
    events_table.duration.resolution = 1/50000.0  # specify the resolution of the durations (optional)

    task = Task()
    task.event_types = event_types_table
    task.ttl_types = ttl_types_table
    nwbfile.add_lab_meta_data(task)
    nwbfile.add_acquisition(events_table)
    nwbfile.add_acquisition(ttls_table)

    # write nwb file
    filename = "test.nwb"
    with NWBHDF5IO(filename, "w") as io:
        io.write(nwbfile)

    # read nwb file and check its contents
    with NWBHDF5IO(filename, "r", load_namespaces=True) as io:
        read_nwbfile = io.read()
        print(read_nwbfile)
        # access the events table, ttls table, event types table, and ttl types table and print them
        print(read_nwbfile.get_lab_meta_data("task").event_types.to_dataframe())
        print(read_nwbfile.acquisition["EventsTable"].to_dataframe())
        print(read_nwbfile.get_lab_meta_data("task").ttl_types.to_dataframe())
        print(read_nwbfile.acquisition["TtlsTable"].to_dataframe())


if __name__ == "__main__":
    test_example_usage()
