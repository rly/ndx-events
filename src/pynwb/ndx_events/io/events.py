from pynwb import register_map
from pynwb.io.core import NWBContainerMapper
from hdmf.common.io.table import DynamicTableMap
from hdmf.build import ObjectMapper, BuildManager
from hdmf.common import VectorData
from hdmf.utils import getargs, docval
from hdmf.spec import AttributeSpec

from ..events import Events, LabeledEvents, AnnotatedEvents


@register_map(Events)
class EventsMap(NWBContainerMapper):

    def __init__(self, spec):
        super().__init__(spec)
        timestamps_spec = self.spec.get_dataset('timestamps')
        self.map_spec('unit', timestamps_spec.get_attribute('unit'))
        self.map_spec('resolution', timestamps_spec.get_attribute('resolution'))


@register_map(LabeledEvents)
class LabeledEventsMap(EventsMap):

    def __init__(self, spec):
        super().__init__(spec)
        label_keys_spec = self.spec.get_dataset('label_keys')
        self.map_spec('labels', label_keys_spec.get_attribute('labels'))


@register_map(AnnotatedEvents)
class AnnotatedEventsMap(DynamicTableMap):

    def __init__(self, spec):
        super().__init__(spec)
        event_times_spec = self.spec.get_dataset('event_times')
        self.map_spec('resolution', event_times_spec.get_attribute('resolution'))

    @DynamicTableMap.constructor_arg('resolution')
    def resolution_carg(self, builder, manager):
        if 'event_times' in builder:
            return builder['event_times'].attributes.get('resolution')
        return None


@register_map(VectorData)
class VectorDataMap(ObjectMapper):

    # TODO fold this into pynwb.io.core.VectorDataMap

    @docval({"name": "spec", "type": AttributeSpec, "doc": "the spec to get the attribute value for"},
            {"name": "container", "type": VectorData, "doc": "the container to get the attribute value from"},
            {"name": "manager", "type": BuildManager, "doc": "the BuildManager used for managing this build"},
            returns='the value of the attribute')
    def get_attr_value(self, **kwargs):
        ''' Get the value of the attribute corresponding to this spec from the given container '''
        spec, container, manager = getargs('spec', 'container', 'manager', kwargs)

        # handle custom mapping of container AnnotatedEvents.resolution -> spec AnnotatedEvents.event_times.resolution
        if isinstance(container.parent, AnnotatedEvents):
            if container.name == 'event_times':
                if spec.name == 'resolution':
                    return container.parent.resolution
        return super().get_attr_value(**kwargs)
