"""
Example script that demonstrates how to write an EventsTable with a CategoricalVectorData and associated MeaningsTable
to store raw TTL pulses received by the acquisition system and processed stimulus presentation events.
"""

from datetime import datetime
from pynwb import NWBHDF5IO

from ndx_events import (
    EventsTable,
    CategoricalVectorData,
    MeaningsTable,
    NdxEventsNWBFile,
)

nwbfile = NdxEventsNWBFile(
    session_description="session description",
    identifier="cool_experiment_001",
    session_start_time=datetime.now().astimezone(),
)

# In this experiment, TTL pulses were sent by the stimulus computer
# to signal important time markers during the experiment/trial,
# when the stimulus was placed on the screen and removed from the screen,
# when the question appeared, and the responses of the subject.

# ref: https://www.nature.com/articles/s41597-020-0415-9, DANDI:000004

# We will first create an EventsTable to store the raw TTL pulses received by the acquisition system.
# Storing the raw TTL pulses is not necessary, but it can be useful for debugging and understanding the experiment.
# The data curator could
# Before doing so, we will create a CategoricalVectorData column for the possible integer values for the TTL pulse
# and associate it with a MeaningsTable that describes the meaning of each value.

pulse_value_meanings_table = MeaningsTable(
    name="pulse_value_meanings", description="The meanings of each integer value for a TTL pulse."
)
pulse_value_meanings_table.add_row(value=55, meaning="Start of experiment")
pulse_value_meanings_table.add_row(value=1, meaning="Stimulus onset")
pulse_value_meanings_table.add_row(value=2, meaning="Stimulus offset")
pulse_value_meanings_table.add_row(value=3, meaning="Question screen onset")

yes_animal_response_description = (
    "During the learning phase, subjects are instructed to respond to the following "
    "question: 'Is this an animal?' in each trial. The response is 'Yes, this is an animal'."
)
no_animal_response_description = (
    "During the learning phase, subjects are instructed to respond to the following "
    "question: 'Is this an animal?' in each trial. The response is 'No, this is not an animal'."
)
pulse_value_meanings_table.add_row(value=20, meaning=yes_animal_response_description)
pulse_value_meanings_table.add_row(value=21, meaning=no_animal_response_description)

new_confident_response_description = (
    "During the recognition phase, subjects are instructed to respond to the following "
    "question: 'Have you seen this image before?' in each trial. The response is 'New, confident'."
)
new_probably_response_description = (
    "During the recognition phase, subjects are instructed to respond to the following "
    "question: 'Have you seen this image before?' in each trial. The response is 'New, probably'."
)
new_guess_response_description = (
    "During the recognition phase, subjects are instructed to respond to the following "
    "question: 'Have you seen this image before?' in each trial. The response is 'New, guess'."
)
old_guess_response_description = (
    "During the recognition phase, subjects are instructed to respond to the following "
    "question: 'Have you seen this image before?' in each trial. The response is 'Old, guess'."
)
old_probably_response_description = (
    "During the recognition phase, subjects are instructed to respond to the following "
    "question: 'Have you seen this image before?' in each trial. The response is 'Old, probably'."
)
old_confident_response_description = (
    "During the recognition phase, subjects are instructed to respond to the following "
    "question: 'Have you seen this image before?' in each trial. The response is 'Old, confident'."
)

pulse_value_meanings_table.add_row(value=31, meaning=new_confident_response_description)
pulse_value_meanings_table.add_row(value=32, meaning=new_probably_response_description)
pulse_value_meanings_table.add_row(value=33, meaning=new_guess_response_description)
pulse_value_meanings_table.add_row(value=34, meaning=old_guess_response_description)
pulse_value_meanings_table.add_row(value=35, meaning=old_probably_response_description)
pulse_value_meanings_table.add_row(value=36, meaning=old_confident_response_description)

pulse_value_meanings_table.add_row(value=6, meaning="End of trial")
pulse_value_meanings_table.add_row(value=66, meaning="End of experiment")

pulse_value_column = CategoricalVectorData(
    name="pulse_value", description="Integer value of the TTL pulse", meanings=pulse_value_meanings_table
)

ttl_events_table = EventsTable(
    name="ttl_events",
    description="TTL events",
    columns=[pulse_value_column],
    meanings_tables=[pulse_value_meanings_table],
)
ttl_events_table.add_row(
    timestamp=6820.092244,
    pulse_value=55,
)
ttl_events_table.add_row(
    timestamp=6821.208244,
    pulse_value=1,
)
ttl_events_table.add_row(
    timestamp=6822.210644,
    pulse_value=2,
)
ttl_events_table.add_row(
    timestamp=6822.711364,
    pulse_value=3,
)
ttl_events_table.add_row(
    timestamp=6825.934244,
    pulse_value=31,
)
ttl_events_table.timestamp.resolution = 1 / 50000.0  # specify the resolution of the timestamps (optional)

# The data curator may want to create an EventsTable to store more processed information than the TTLs table
# e.g., converting stimulus onset and offset into a single stimulus event with metadata.
# This may be redundant with information in the trials table if the task is
# structured into trials.

stimulus_category_meanings_table = MeaningsTable(
    name="stimulus_category_meanings", description="The meanings of each stimulus category"
)
stimulus_category_meanings_table.add_row(value="smallAnimal", meaning="An image of a small animal was presented.")
stimulus_category_meanings_table.add_row(value="largeAnimal", meaning="An image of a large animal was presented.")

stimulus_category_column = CategoricalVectorData(
    name="stimulus_category", description="The category of the stimulus", meanings=stimulus_category_meanings_table
)

stimulus_presentation_table = EventsTable(
    name="stimulus_presentations",
    description="Metadata about stimulus presentations",
    columns=[stimulus_category_column],
    meanings_tables=[stimulus_category_meanings_table],
)
stimulus_presentation_table.add_column(
    name="stimulus_image_index", description="Frame index of the stimulus image in the StimulusPresentation object"
)  # this is an integer.
# One could make this a CategoricalVectorData column if there are a limited number of stimulus images and one
# wants to describe each one

stimulus_presentation_table.add_row(
    timestamp=6821.208244,
    duration=1.0024,  # this comes from the stimulus onset and offset TTLs
    stimulus_category="smallAnimal",
    stimulus_image_index=0,
)
stimulus_presentation_table.add_row(
    timestamp=6825.208244,
    duration=0.99484,
    stimulus_category="phones",
    stimulus_image_index=1,
)
stimulus_presentation_table.timestamp.resolution = 1 / 50000.0  # specify the resolution of the timestamps (optional)
stimulus_presentation_table.duration.resolution = 1 / 50000.0  # specify the resolution of the durations (optional)

nwbfile.add_events_table(ttl_events_table)
nwbfile.add_events_table(stimulus_presentation_table)

print(nwbfile.get_all_events())

# Write NWB file.
filename = "test_events.nwb"
with NWBHDF5IO(filename, "w") as io:
    io.write(nwbfile)

# Read NWB file and check its contents.
with NWBHDF5IO(filename, "r", load_namespaces=True) as io:
    read_nwbfile = io.read()
    print(read_nwbfile)
    print(read_nwbfile.events["ttl_events"].to_dataframe())
    print(read_nwbfile.events["stimulus_presentations"].to_dataframe())
