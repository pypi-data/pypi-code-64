import logging
from typing import (
    Any,
    Callable,
    Coroutine,
    Dict,
    Iterable,
    List,
    Optional,
    Tuple,
    Union,
)

import zigpy.device
import zigpy.endpoint
from zigpy.quirks.registry import DeviceRegistry
import zigpy.types as t
import zigpy.zcl
import zigpy.zcl.foundation as foundation

_LOGGER = logging.getLogger(__name__)

_DEVICE_REGISTRY = DeviceRegistry()


def get_device(device, registry=_DEVICE_REGISTRY):
    """Get a CustomDevice object, if one is available"""
    return registry.get_device(device)


class Registry(type):
    def __init__(cls, name, bases, nmspc):  # noqa: N805
        super(Registry, cls).__init__(name, bases, nmspc)
        if getattr(cls, "signature", None) is not None:
            _DEVICE_REGISTRY.add_to_registry(cls)


class CustomDevice(zigpy.device.Device, metaclass=Registry):
    replacement = {}
    signature = None

    def __init__(self, application, ieee, nwk, replaces):
        super().__init__(application, ieee, nwk)

        def set_device_attr(attr):
            if attr in self.replacement:
                setattr(self, attr, self.replacement[attr])
            else:
                setattr(self, attr, getattr(replaces, attr))

        for attr in ("lqi", "rssi", "last_seen", "relays"):
            setattr(self, attr, getattr(replaces, attr))

        set_device_attr("status")
        set_device_attr("node_desc")
        set_device_attr("manufacturer")
        set_device_attr("model")
        set_device_attr("skip_configuration")
        for endpoint_id, endpoint in self.replacement.get("endpoints", {}).items():
            self.add_endpoint(endpoint_id, replace_device=replaces)

    def add_endpoint(self, endpoint_id, replace_device=None):
        if endpoint_id not in self.replacement.get("endpoints", {}):
            return super().add_endpoint(endpoint_id)

        endpoints = self.replacement["endpoints"]

        if isinstance(endpoints[endpoint_id], tuple):
            custom_ep_type = endpoints[endpoint_id][0]
            replacement_data = endpoints[endpoint_id][1]
        else:
            custom_ep_type = CustomEndpoint
            replacement_data = endpoints[endpoint_id]

        ep = custom_ep_type(self, endpoint_id, replacement_data, replace_device)
        self.endpoints[endpoint_id] = ep
        return ep


class CustomEndpoint(zigpy.endpoint.Endpoint):
    def __init__(self, device, endpoint_id, replacement_data, replace_device):
        super().__init__(device, endpoint_id)

        def set_device_attr(attr):
            if attr in replacement_data:
                setattr(self, attr, replacement_data[attr])
            else:
                setattr(self, attr, getattr(replace_device[endpoint_id], attr))

        set_device_attr("profile_id")
        set_device_attr("device_type")
        self.status = zigpy.endpoint.Status.ZDO_INIT

        for c in replacement_data.get("input_clusters", []):
            if isinstance(c, int):
                cluster = None
                cluster_id = c
            else:
                cluster = c(self, is_server=True)
                cluster_id = cluster.cluster_id
            self.add_input_cluster(cluster_id, cluster)

        for c in replacement_data.get("output_clusters", []):
            if isinstance(c, int):
                cluster = None
                cluster_id = c
            else:
                cluster = c(self, is_server=False)
                cluster_id = cluster.cluster_id
            self.add_output_cluster(cluster_id, cluster)


class CustomCluster(zigpy.zcl.Cluster):
    _skip_registry = True
    _CONSTANT_ATTRIBUTES: Optional[Dict[int, Any]] = None
    manufacturer_attributes: Dict[int, Tuple[str, Callable]] = {}
    manufacturer_client_commands: Dict[int, Tuple[str, Tuple, bool]] = {}
    manufacturer_server_commands: Dict[int, Tuple[str, Tuple, bool]] = {}

    @property
    def _is_manuf_specific(self) -> bool:
        """Return True if cluster_id is within manufacturer specific range."""
        return 0xFC00 <= self.cluster_id <= 0xFFFF

    def _has_manuf_attr(self, attrs_to_process: Union[Iterable, List, Dict]) -> bool:
        """Return True if contains a manufacturer specific attribute."""
        return self._is_manuf_specific or (
            set.intersection(set(self.manufacturer_attributes), attrs_to_process)
        )

    def command(
        self,
        command_id: Union[foundation.Command, int, t.uint8_t],
        *args,
        manufacturer: Optional[Union[int, t.uint16_t]] = None,
        expect_reply: bool = True,
        tsn: Optional[Union[int, t.uint8_t]] = None,
    ) -> Coroutine:
        schema = self.server_commands[command_id][1]
        if manufacturer is None and (
            command_id in self.manufacturer_server_commands or self._is_manuf_specific
        ):
            manufacturer = self.endpoint.manufacturer_id
        return self.request(
            False,
            command_id,
            schema,
            *args,
            manufacturer=manufacturer,
            expect_reply=expect_reply,
            tsn=tsn,
        )

    def client_command(
        self,
        command_id: Union[foundation.Command, int, t.uint8_t],
        *args,
        manufacturer: Optional[Union[int, t.uint16_t]] = None,
        tsn: Optional[Union[int, t.uint8_t]] = None,
    ) -> Coroutine:
        schema = self.client_commands[command_id][1]
        if manufacturer is None and (
            command_id in self.manufacturer_client_commands or self._is_manuf_specific
        ):
            manufacturer = self.endpoint.manufacturer_id
        return self.reply(
            False, command_id, schema, *args, manufacturer=manufacturer, tsn=tsn
        )

    async def read_attributes_raw(self, attributes, manufacturer=None):
        if not self._CONSTANT_ATTRIBUTES:
            return await super().read_attributes_raw(
                attributes, manufacturer=manufacturer
            )

        succeeded = [
            foundation.ReadAttributeRecord(
                attr, foundation.Status.SUCCESS, foundation.TypeValue()
            )
            for attr in attributes
            if attr in self._CONSTANT_ATTRIBUTES
        ]
        for record in succeeded:
            record.value.value = self._CONSTANT_ATTRIBUTES[record.attrid]

        attrs_to_read = [
            attr for attr in attributes if attr not in self._CONSTANT_ATTRIBUTES
        ]

        if not attrs_to_read:
            return [succeeded]

        results = await super().read_attributes_raw(
            attrs_to_read, manufacturer=manufacturer
        )
        if not isinstance(results[0], list):
            for attrid in attrs_to_read:
                succeeded.append(
                    foundation.ReadAttributeRecord(
                        attrid,
                        results[0],
                        foundation.TypeValue(),
                    )
                )
        else:
            succeeded.extend(results[0])
        return [succeeded]

    def _configure_reporting(
        self, args: List[foundation.Attribute], manufacturer: Optional[int] = None
    ):
        """Configure reporting ZCL foundation command."""
        if manufacturer is None and self._has_manuf_attr([a.attrid for a in args]):
            manufacturer = self.endpoint.manufacturer_id
        return super()._configure_reporting(args, manufacturer=manufacturer)

    def _read_attributes(
        self, args: List[t.uint16_t], manufacturer: Optional[int] = None
    ):
        """Read attributes ZCL foundation command."""
        if manufacturer is None and self._has_manuf_attr(args):
            manufacturer = self.endpoint.manufacturer_id
        return super()._read_attributes(args, manufacturer=manufacturer)

    def _write_attributes(
        self, args: List[foundation.Attribute], manufacturer: Optional[int] = None
    ):
        """Write attribute ZCL foundation command."""
        if manufacturer is None and self._has_manuf_attr([a.attrid for a in args]):
            manufacturer = self.endpoint.manufacturer_id
        return super()._write_attributes(args, manufacturer=manufacturer)

    def _write_attributes_undivided(
        self, args: List[foundation.Attribute], manufacturer: Optional[int] = None
    ):
        """Write attribute undivided ZCL foundation command."""
        if manufacturer is None and self._has_manuf_attr([a.attrid for a in args]):
            manufacturer = self.endpoint.manufacturer_id
        return super()._write_attributes_undivided(args, manufacturer=manufacturer)
