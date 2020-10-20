from pynwb import register_map
from pynwb.io.core import NWBContainerMapper
from hdmf.common.io.table import DynamicTableMap
from hdmf.build import ObjectMapper, BuildManager
from hdmf.common import VectorData
from hdmf.utils import getargs, docval
from hdmf.spec import AttributeSpec

from ..events import Events, LabeledEvents, AnnotatedEventsTable


@register_map(Events)
class EventsMap(NWBContainerMapper):

    def __init__(self, spec):
        super().__init__(spec)
        # map object attribute Events.unit -> spec Events/timestamps.unit
        # map object attribute Events.resolution -> spec Events/timestamps.resolution
        timestamps_spec = self.spec.get_dataset('timestamps')
        self.map_spec('unit', timestamps_spec.get_attribute('unit'))
        self.map_spec('resolution', timestamps_spec.get_attribute('resolution'))


@register_map(LabeledEvents)
class LabeledEventsMap(EventsMap):

    def __init__(self, spec):
        super().__init__(spec)
        # map object attribute LabeledEvents.labels -> spec LabeledEvents/data.labels
        data_spec = self.spec.get_dataset('data')
        self.map_spec('labels', data_spec.get_attribute('labels'))


@register_map(AnnotatedEventsTable)
class AnnotatedEventsTableMap(DynamicTableMap):

    def __init__(self, spec):
        super().__init__(spec)
        # map object attribute AnnotatedEventsTable.resolution -> spec AnnotatedEventsTable/event_times.resolution
        event_times_spec = self.spec.get_dataset('event_times')
        self.map_spec('resolution', event_times_spec.get_attribute('resolution'))

    @DynamicTableMap.constructor_arg('resolution')
    def resolution_carg(self, builder, manager):
        # on construct, map builder for AnnotatedEventsTable.datasets['event_times'].attributes['resolution']
        # -> AnnotatedEventsTable.__init__ argument 'resolution'
        if 'event_times' in builder:
            return builder['event_times'].attributes.get('resolution')
        return None


@register_map(VectorData)
class VectorDataMap(ObjectMapper):

    # TODO when merging into NWB core, fold this into pynwb.io.core.VectorDataMap

    @docval({"name": "spec", "type": AttributeSpec, "doc": "the spec to get the attribute value for"},
            {"name": "container", "type": VectorData, "doc": "the container to get the attribute value from"},
            {"name": "manager", "type": BuildManager, "doc": "the BuildManager used for managing this build"},
            returns='the value of the attribute')
    def get_attr_value(self, **kwargs):
        ''' Get the value of the attribute corresponding to this spec from the given container '''
        spec, container, manager = getargs('spec', 'container', 'manager', kwargs)

        # on build of VectorData objects, map object attribute AnnotatedEventsTable.resolution
        # -> spec AnnotatedEventsTable/event_times.resolution
        if isinstance(container.parent, AnnotatedEventsTable):
            if container.name == 'event_times':
                if spec.name == 'resolution':
                    return container.parent.resolution
        return super().get_attr_value(**kwargs)
