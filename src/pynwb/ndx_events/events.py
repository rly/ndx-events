import numpy as np

from pynwb import register_class, get_class
from pynwb.core import NWBDataInterface, DynamicTable
from hdmf.utils import docval, getargs, popargs, get_docval


EventTypesTable = get_class('EventTypesTable', 'ndx-events')
EventsTable = get_class('EventsTable', 'ndx-events')
# TTLTypesTable = get_class('TTLTypesTable', 'ndx-events')
