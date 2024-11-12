from pynwb import get_class, register_class, NWBFile
from hdmf.utils import docval, get_docval
import pandas as pd


TimestampVectorData = get_class("TimestampVectorData", "ndx-events")
DurationVectorData = get_class("DurationVectorData", "ndx-events")
CategoricalVectorData = get_class("CategoricalVectorData", "ndx-events")
MeaningsTable = get_class("MeaningsTable", "ndx-events")
EventsTable = get_class("EventsTable", "ndx-events")


# Replace the __getitem__ method with a custom one from DynamicTable instead of the one from MultiContainerInterface
# NOTE: When the NWBEP001 is merged into the core NWB schema and software, this class will be explicitly defined
# in PyNWB and will use the following __getitem__ method.
def __new_getitem__(self, key):
    """Get the table row, column, or selection of cells with the given name."""
    ret = self.get(key)
    if ret is None:
        raise KeyError(key)
    return ret


EventsTable.__getitem__ = __new_getitem__
del __new_getitem__


# NOTE: When the NWBEP001 is merged into the core NWB schema and software, this class will be merged
# with the core NWBFile class.
@register_class("NdxEventsNWBFile", "ndx-events")
class NdxEventsNWBFile(NWBFile):
    __clsconf__ = [
        {
            "attr": "events",
            "add": "add_events_table",
            "type": EventsTable,
            "create": "create_events_table",
            "get": "get_events_table",
        },
    ]

    @docval(
        *get_docval(NWBFile.__init__),
        {"name": "events", "type": (list, tuple), "doc": "Any EventsTable tables storing events", "default": None},
    )
    def __init__(self, **kwargs):
        events = kwargs.pop("events", None)
        super().__init__(**kwargs)
        self.events = events

    def merge_events_tables(self, tables):  # tables: list[EventsTable]
        return pd.concat([table.to_dataframe().set_index("timestamp") for table in tables], sort=True)

    def get_all_events(self):
        return self.merge_events_tables(list(self.events.values()))
