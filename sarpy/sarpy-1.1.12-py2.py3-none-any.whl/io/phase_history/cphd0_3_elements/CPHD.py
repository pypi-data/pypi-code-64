# -*- coding: utf-8 -*-
"""
The Compensated Phase History Data 0.3 definition.
"""

from typing import Union

from sarpy.io.phase_history.cphd1_elements.base import DEFAULT_STRICT
# noinspection PyProtectedMember
from sarpy.io.complex.sicd_elements.base import Serializable, _SerializableDescriptor, \
    _IntegerDescriptor, _StringDescriptor

from sarpy.io.complex.sicd_elements.CollectionInfo import CollectionInfoType
from sarpy.io.complex.sicd_elements.RadarCollection import RadarCollectionType
from sarpy.io.phase_history.cphd1_elements.CPHD import CPHDHeaderBase
from sarpy.io.phase_history.cphd0_3_elements.Data import DataType
from sarpy.io.phase_history.cphd0_3_elements.Global import GlobalType
from sarpy.io.phase_history.cphd0_3_elements.Channel import ChannelType
from sarpy.io.phase_history.cphd0_3_elements.SRP import SRPTyp
from sarpy.io.phase_history.cphd0_3_elements.Antenna import AntennaType
from sarpy.io.phase_history.cphd0_3_elements.VectorParameters import VectorParametersType

__classification__ = "UNCLASSIFIED"
__author__ = "Thomas McCullough"


#########
# Module variables
_CPHD_SPECIFICATION_VERSION = '0.3'
_CPHD_SPECIFICATION_DATE = '2011-04-15T00:00:00Z'
_CPHD_SPECIFICATION_NAMESPACE = 'urn:CPHD:0.3'


#########
# CPHD header object

class CPHDHeader(CPHDHeaderBase):
    _fields = (
        'XML_DATA_SIZE', 'XML_BYTE_OFFSET', 'VB_DATA_SIZE', 'VB_BYTE_OFFSET',
        'CPHD_DATA_SIZE', 'CPHD_BYTE_OFFSET', 'CLASSIFICATION', 'RELEASE_INFO')
    _required = (
        'XML_DATA_SIZE', 'XML_BYTE_OFFSET', 'VB_DATA_SIZE', 'VB_BYTE_OFFSET',
        'CPHD_DATA_SIZE', 'CPHD_BYTE_OFFSET')
    # descriptor
    XML_DATA_SIZE = _IntegerDescriptor(
        'XML_DATA_SIZE', _required, strict=True,
        docstring='Size of the XML Metadata in bytes. Does not include the 2 bytes '
                  'of the section terminator.')  # type: int
    XML_BYTE_OFFSET = _IntegerDescriptor(
        'XML_BYTE_OFFSET', _required, strict=True,
        docstring='Offset to the first byte of the XML Metadata in bytes.')  # type: int
    VB_DATA_SIZE = _IntegerDescriptor(
        'VB_DATA_SIZE', _required, strict=True,
        docstring='Size of the Vector Based Metadata in bytes.')  # type: int
    VB_BYTE_OFFSET = _IntegerDescriptor(
        'VB_BYTE_OFFSET', _required, strict=True,
        docstring='Offset to the first byte of the Vector Based Metadata in bytes.')  # type: int
    CPHD_DATA_SIZE = _IntegerDescriptor(
        'CPHD_DATA_SIZE', _required, strict=True,
        docstring='Size of the Compensated PHD arrays in bytes.')  # type: int
    CPHD_BYTE_OFFSET = _IntegerDescriptor(
        'CPHD_BYTE_OFFSET', _required, strict=True,
        docstring='Offset to the first byte of the CPHD data in bytes.')  # type: int
    CLASSIFICATION = _StringDescriptor(
        'CLASSIFICATION', _required, strict=True, default_value='UNCLASSIFIED',
        docstring='Product classification information that is the human-readable banner.')  # type: str
    RELEASE_INFO = _StringDescriptor(
        'RELEASE_INFO', _required, strict=True, default_value='UNRESTRICTED',
        docstring='Product release information.')  # type: str

    def __init__(self, XML_DATA_SIZE=None, XML_BYTE_OFFSET=None,
                 VB_DATA_SIZE=None, VB_BYTE_OFFSET=None,
                 CPHD_DATA_SIZE=None, CPHD_BYTE_OFFSET=None,
                 CLASSIFICATION='UNCLASSIFIED', RELEASE_INFO='UNRESTRICTED'):
        self.XML_DATA_SIZE = XML_DATA_SIZE
        self.XML_BYTE_OFFSET = XML_BYTE_OFFSET
        self.VB_DATA_SIZE = VB_DATA_SIZE
        self.VB_BYTE_OFFSET = VB_BYTE_OFFSET
        self.CPHD_DATA_SIZE = CPHD_DATA_SIZE
        self.CPHD_BYTE_OFFSET = CPHD_BYTE_OFFSET
        self.CLASSIFICATION = CLASSIFICATION
        self.RELEASE_INFO = RELEASE_INFO
        super(CPHDHeader, self).__init__()


class CPHDType(Serializable):
    """
    """

    _fields = (
        'CollectionInfo', 'Data', 'Global', 'Channel', 'SRP', 'RadarCollection', 'Antenna',
        'VectorParameters')
    _required = (
        'CollectionInfo', 'Data', 'Global', 'Channel', 'SRP', 'VectorParameters')
    # descriptors
    CollectionInfo = _SerializableDescriptor(
        'CollectionInfo', CollectionInfoType, _required, strict=DEFAULT_STRICT,
        docstring='General information about the collection.')  # type: CollectionInfoType
    Data = _SerializableDescriptor(
        'Data', DataType, _required, strict=DEFAULT_STRICT,
        docstring='Parameters that describe binary data components contained in the '
                  'product.')  # type: DataType
    Global = _SerializableDescriptor(
        'Global', GlobalType, _required, strict=DEFAULT_STRICT,
        docstring='Global parameters that apply to metadata components and CPHD '
                  'signal arrays.')  # type: GlobalType
    Channel = _SerializableDescriptor(
        'Channel', ChannelType, _required, strict=DEFAULT_STRICT,
        docstring='Channel specific parameters for CPHD channels.')  # type: ChannelType
    SRP = _SerializableDescriptor(
        'SRP', SRPTyp, _required, strict=DEFAULT_STRICT,
        docstring='The Stabilization Reference Point (SRP) parameters.')  # type: SRPTyp
    RadarCollection = _SerializableDescriptor(
        'RadarCollection', RadarCollectionType, _required, strict=DEFAULT_STRICT,
        docstring='')  # type: Union[None, RadarCollectionType]
    Antenna = _SerializableDescriptor(
        'Antenna', AntennaType, _required, strict=DEFAULT_STRICT,
        docstring='Antenna parameters that describe antenna orientation, mainlobe '
                  'steering and gain patterns vs. '
                  'time.')  # type: Union[None, AntennaType]
    VectorParameters = _SerializableDescriptor(
        'VectorParameters', VectorParametersType, _required, strict=DEFAULT_STRICT,
        docstring='Structure specifying the Vector parameters provided for '
                  'each channel of a given product.')  # type: VectorParametersType

    def __init__(self, CollectionInfo=None, Data=None, Global=None, Channel=None,
                 SRP=None, RadarCollection=None, Antenna=None, VectorParameters=None, **kwargs):
        """

        Parameters
        ----------
        CollectionInfo : CollectionInfoType
        Data : DataType
        Global : GlobalType
        Channel : ChannelType
        SRP : SRPTyp
        RadarCollection : None|RadarCollectionType
        Antenna : None|AntennaType
        VectorParameters : VectorParametersType
        kwargs
        """

        if '_xml_ns' in kwargs:
            self._xml_ns = kwargs['_xml_ns']
        if '_xml_ns_key' in kwargs:
            self._xml_ns_key = kwargs['_xml_ns_key']
        self.CollectionInfo = CollectionInfo
        self.Data = Data
        self.Global = Global
        self.Channel = Channel
        self.SRP = SRP
        self.RadarCollection = RadarCollection
        self.Antenna = Antenna
        self.VectorParameters = VectorParameters
        super(CPHDType, self).__init__(**kwargs)

    def to_xml_bytes(self, urn=None, tag=None, check_validity=False, strict=DEFAULT_STRICT):
        return super(CPHDType, self).to_xml_bytes(
            urn=_CPHD_SPECIFICATION_NAMESPACE, tag=tag, check_validity=check_validity, strict=strict)
