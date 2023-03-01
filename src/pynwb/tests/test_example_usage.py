def test_example_usage():
    from datetime import datetime

    from pynwb import NWBFile, NWBHDF5IO
    from ndx_events import LabeledEvents, EventTypesTable

    nwb = NWBFile(
        session_description='session description',
        identifier='cool_experiment_001',
        session_start_time=datetime.now().astimezone()
    )

    event_types_table = EventTypesTable(
        name="EventTypesTable",
        description="metadata about event types",
    )

    event_types_table.add_row(id=0, label="trial start")
    event_types_table.add_row(id=1, label="cue onset")
    event_types_table.add_row(id=2, label="cue offset")
    event_types_table.add_row(id=3, label="response left")
    event_types_table.add_row(id=4, label="response right")
    event_types_table.add_row(id=5, label="reward")

    nwb.add_acquisition(event_types_table)  # place here for now

    # create a new LabeledEvents type to hold events recorded from the data acquisition system
    events = LabeledEvents(
        name='LabeledEvents',
        description='events from my experiment',
        timestamps=[0., 0.5, 0.6, 2., 2.05, 3., 3.5, 3.6, 4.],
        resolution=1e-5,  # resolution of the timestamps, i.e., smallest possible difference between timestamps
        data=[0, 1, 2, 3, 5, 0, 1, 2, 4],
        event_types=event_types_table,
    )

    # add the LabeledEvents type to the acquisition group of the NWB file
    nwb.add_acquisition(events)

    # # create a new AnnotatedEventsTable type to hold annotated events
    # # each row of the table represents a single event type
    # annotated_events = AnnotatedEventsTable(
    #     name='AnnotatedEventsTable',
    #     description='annotated events from my experiment',
    #     resolution=1e-5  # resolution of the timestamps, i.e., smallest possible difference between timestamps
    # )
    # # add a custom indexed (ragged) column to represent whether each event time was a bad event
    # annotated_events.add_column(
    #     name='bad_event',
    #     description='whether each event time should be excluded',
    #     index=True
    # )
    # # add an event type (row) to the AnnotatedEventsTable instance
    # annotated_events.add_event_type(
    #     label='Reward',
    #     event_description='Times when the subject received juice reward.',
    #     event_times=[1., 2., 3.],
    #     bad_event=[False, False, True],
    #     id=3
    # )
    # # convert the AnnotatedEventsTable to a pandas.DataFrame and print it
    # print(annotated_events.to_dataframe())

    # # create a processing module in the NWB file to hold processed events data
    # events_module = nwb.create_processing_module(
    #     name='events',
    #     description='processed event data'
    # )

    # # add the AnnotatedEventsTable instance to the processing module
    # events_module.add(annotated_events)

    # write nwb file
    filename = 'test.nwb'
    with NWBHDF5IO(filename, 'w') as io:
        io.write(nwb)

    # read nwb file and check its contents
    with NWBHDF5IO(filename, 'r', load_namespaces=True) as io:
        nwb = io.read()
        print(nwb)
        # access the LabeledEvents container by name from the NWBFile acquisition group and print it
        print(nwb.acquisition['EventTypesTable'])
        print(nwb.acquisition['LabeledEvents'])
        # access the AnnotatedEventsTable by name from the 'events' processing module, convert it to
        # a pandas.DataFrame, and print that
        # print(nwb.processing['events']['AnnotatedEventsTable'].to_dataframe())


if __name__ == "__main__":
    test_example_usage()