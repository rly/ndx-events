from pynwb import register_map
from pynwb.io.file import NWBFileMap
from .events import NdxEventsNWBFile


# NOTE: When the NWBEP001 is merged into the core NWB schema and software, this class will be merged
# with the core NWBFileMap class.
@register_map(NdxEventsNWBFile)
class NdxEventsNWBFileMap(NWBFileMap):

    def __init__(self, spec):
        super().__init__(spec)

        # Map the "events" attribute on the NdxEventsNWBFile class to the EventsTable class
        events_spec = self.spec.get_group("events")
        self.unmap(events_spec)
        self.map_spec("events", events_spec.get_neurodata_type("EventsTable"))
