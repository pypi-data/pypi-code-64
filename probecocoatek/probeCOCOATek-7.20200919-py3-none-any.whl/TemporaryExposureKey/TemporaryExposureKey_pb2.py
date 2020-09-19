# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: TemporaryExposureKey.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='TemporaryExposureKey.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1aTemporaryExposureKey.proto\"\xfe\x01\n\x1aTemporaryExposureKeyExport\x12\x17\n\x0fstart_timestamp\x18\x01 \x01(\x06\x12\x15\n\rend_timestamp\x18\x02 \x01(\x06\x12\x0e\n\x06region\x18\x03 \x01(\t\x12\x11\n\tbatch_num\x18\x04 \x01(\x05\x12\x12\n\nbatch_size\x18\x05 \x01(\x05\x12\'\n\x0fsignature_infos\x18\x06 \x03(\x0b\x32\x0e.SignatureInfo\x12#\n\x04keys\x18\x07 \x03(\x0b\x32\x15.TemporaryExposureKey\x12+\n\x0crevised_keys\x18\x08 \x03(\x0b\x32\x15.TemporaryExposureKey\"\x97\x01\n\rSignatureInfo\x12 \n\x18verification_key_version\x18\x03 \x01(\t\x12\x1b\n\x13verification_key_id\x18\x04 \x01(\t\x12\x1b\n\x13signature_algorithm\x18\x05 \x01(\tJ\x04\x08\x01\x10\x02J\x04\x08\x02\x10\x03R\rapp_bundle_idR\x0f\x61ndroid_package\"\xec\x02\n\x14TemporaryExposureKey\x12\x10\n\x08key_data\x18\x01 \x01(\x0c\x12#\n\x17transmission_risk_level\x18\x02 \x01(\x05\x42\x02\x18\x01\x12%\n\x1drolling_start_interval_number\x18\x03 \x01(\x05\x12\x1b\n\x0erolling_period\x18\x04 \x01(\x05:\x03\x31\x34\x34\x12\x35\n\x0breport_type\x18\x05 \x01(\x0e\x32 .TemporaryExposureKey.ReportType\x12$\n\x1c\x64\x61ys_since_onset_of_symptoms\x18\x06 \x01(\x11\"|\n\nReportType\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x12\n\x0e\x43ONFIRMED_TEST\x10\x01\x12 \n\x1c\x43ONFIRMED_CLINICAL_DIAGNOSIS\x10\x02\x12\x0f\n\x0bSELF_REPORT\x10\x03\x12\r\n\tRECURSIVE\x10\x04\x12\x0b\n\x07REVOKED\x10\x05\"5\n\x10TEKSignatureList\x12!\n\nsignatures\x18\x01 \x03(\x0b\x32\r.TEKSignature\"p\n\x0cTEKSignature\x12&\n\x0esignature_info\x18\x01 \x01(\x0b\x32\x0e.SignatureInfo\x12\x11\n\tbatch_num\x18\x02 \x01(\x05\x12\x12\n\nbatch_size\x18\x03 \x01(\x05\x12\x11\n\tsignature\x18\x04 \x01(\x0c'
)



_TEMPORARYEXPOSUREKEY_REPORTTYPE = _descriptor.EnumDescriptor(
  name='ReportType',
  full_name='TemporaryExposureKey.ReportType',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CONFIRMED_TEST', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CONFIRMED_CLINICAL_DIAGNOSIS', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SELF_REPORT', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='RECURSIVE', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='REVOKED', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=682,
  serialized_end=806,
)
_sym_db.RegisterEnumDescriptor(_TEMPORARYEXPOSUREKEY_REPORTTYPE)


_TEMPORARYEXPOSUREKEYEXPORT = _descriptor.Descriptor(
  name='TemporaryExposureKeyExport',
  full_name='TemporaryExposureKeyExport',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='start_timestamp', full_name='TemporaryExposureKeyExport.start_timestamp', index=0,
      number=1, type=6, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='end_timestamp', full_name='TemporaryExposureKeyExport.end_timestamp', index=1,
      number=2, type=6, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='region', full_name='TemporaryExposureKeyExport.region', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='batch_num', full_name='TemporaryExposureKeyExport.batch_num', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='batch_size', full_name='TemporaryExposureKeyExport.batch_size', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='signature_infos', full_name='TemporaryExposureKeyExport.signature_infos', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='keys', full_name='TemporaryExposureKeyExport.keys', index=6,
      number=7, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='revised_keys', full_name='TemporaryExposureKeyExport.revised_keys', index=7,
      number=8, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=31,
  serialized_end=285,
)


_SIGNATUREINFO = _descriptor.Descriptor(
  name='SignatureInfo',
  full_name='SignatureInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='verification_key_version', full_name='SignatureInfo.verification_key_version', index=0,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='verification_key_id', full_name='SignatureInfo.verification_key_id', index=1,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='signature_algorithm', full_name='SignatureInfo.signature_algorithm', index=2,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=288,
  serialized_end=439,
)


_TEMPORARYEXPOSUREKEY = _descriptor.Descriptor(
  name='TemporaryExposureKey',
  full_name='TemporaryExposureKey',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key_data', full_name='TemporaryExposureKey.key_data', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='transmission_risk_level', full_name='TemporaryExposureKey.transmission_risk_level', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='rolling_start_interval_number', full_name='TemporaryExposureKey.rolling_start_interval_number', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='rolling_period', full_name='TemporaryExposureKey.rolling_period', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=144,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='report_type', full_name='TemporaryExposureKey.report_type', index=4,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='days_since_onset_of_symptoms', full_name='TemporaryExposureKey.days_since_onset_of_symptoms', index=5,
      number=6, type=17, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _TEMPORARYEXPOSUREKEY_REPORTTYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=442,
  serialized_end=806,
)


_TEKSIGNATURELIST = _descriptor.Descriptor(
  name='TEKSignatureList',
  full_name='TEKSignatureList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='signatures', full_name='TEKSignatureList.signatures', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=808,
  serialized_end=861,
)


_TEKSIGNATURE = _descriptor.Descriptor(
  name='TEKSignature',
  full_name='TEKSignature',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='signature_info', full_name='TEKSignature.signature_info', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='batch_num', full_name='TEKSignature.batch_num', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='batch_size', full_name='TEKSignature.batch_size', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='signature', full_name='TEKSignature.signature', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=863,
  serialized_end=975,
)

_TEMPORARYEXPOSUREKEYEXPORT.fields_by_name['signature_infos'].message_type = _SIGNATUREINFO
_TEMPORARYEXPOSUREKEYEXPORT.fields_by_name['keys'].message_type = _TEMPORARYEXPOSUREKEY
_TEMPORARYEXPOSUREKEYEXPORT.fields_by_name['revised_keys'].message_type = _TEMPORARYEXPOSUREKEY
_TEMPORARYEXPOSUREKEY.fields_by_name['report_type'].enum_type = _TEMPORARYEXPOSUREKEY_REPORTTYPE
_TEMPORARYEXPOSUREKEY_REPORTTYPE.containing_type = _TEMPORARYEXPOSUREKEY
_TEKSIGNATURELIST.fields_by_name['signatures'].message_type = _TEKSIGNATURE
_TEKSIGNATURE.fields_by_name['signature_info'].message_type = _SIGNATUREINFO
DESCRIPTOR.message_types_by_name['TemporaryExposureKeyExport'] = _TEMPORARYEXPOSUREKEYEXPORT
DESCRIPTOR.message_types_by_name['SignatureInfo'] = _SIGNATUREINFO
DESCRIPTOR.message_types_by_name['TemporaryExposureKey'] = _TEMPORARYEXPOSUREKEY
DESCRIPTOR.message_types_by_name['TEKSignatureList'] = _TEKSIGNATURELIST
DESCRIPTOR.message_types_by_name['TEKSignature'] = _TEKSIGNATURE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TemporaryExposureKeyExport = _reflection.GeneratedProtocolMessageType('TemporaryExposureKeyExport', (_message.Message,), {
  'DESCRIPTOR' : _TEMPORARYEXPOSUREKEYEXPORT,
  '__module__' : 'TemporaryExposureKey_pb2'
  # @@protoc_insertion_point(class_scope:TemporaryExposureKeyExport)
  })
_sym_db.RegisterMessage(TemporaryExposureKeyExport)

SignatureInfo = _reflection.GeneratedProtocolMessageType('SignatureInfo', (_message.Message,), {
  'DESCRIPTOR' : _SIGNATUREINFO,
  '__module__' : 'TemporaryExposureKey_pb2'
  # @@protoc_insertion_point(class_scope:SignatureInfo)
  })
_sym_db.RegisterMessage(SignatureInfo)

TemporaryExposureKey = _reflection.GeneratedProtocolMessageType('TemporaryExposureKey', (_message.Message,), {
  'DESCRIPTOR' : _TEMPORARYEXPOSUREKEY,
  '__module__' : 'TemporaryExposureKey_pb2'
  # @@protoc_insertion_point(class_scope:TemporaryExposureKey)
  })
_sym_db.RegisterMessage(TemporaryExposureKey)

TEKSignatureList = _reflection.GeneratedProtocolMessageType('TEKSignatureList', (_message.Message,), {
  'DESCRIPTOR' : _TEKSIGNATURELIST,
  '__module__' : 'TemporaryExposureKey_pb2'
  # @@protoc_insertion_point(class_scope:TEKSignatureList)
  })
_sym_db.RegisterMessage(TEKSignatureList)

TEKSignature = _reflection.GeneratedProtocolMessageType('TEKSignature', (_message.Message,), {
  'DESCRIPTOR' : _TEKSIGNATURE,
  '__module__' : 'TemporaryExposureKey_pb2'
  # @@protoc_insertion_point(class_scope:TEKSignature)
  })
_sym_db.RegisterMessage(TEKSignature)


_TEMPORARYEXPOSUREKEY.fields_by_name['transmission_risk_level']._options = None
# @@protoc_insertion_point(module_scope)
