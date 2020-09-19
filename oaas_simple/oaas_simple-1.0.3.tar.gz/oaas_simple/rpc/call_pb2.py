# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: call.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="call.proto",
    package="gr",
    syntax="proto3",
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
    serialized_pb=b'\n\ncall.proto\x12\x02gr"*\n\x04\x44\x61ta\x12\t\n\x01s\x18\x01 \x01(\t\x12\t\n\x01\x62\x18\x02 \x01(\x0c\x12\x0c\n\x04json\x18\x03 \x01(\t"8\n\x10ServiceCallParam\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x16\n\x04\x64\x61ta\x18\x02 \x01(\x0b\x32\x08.gr.Data"|\n\x0bServiceCall\x12\x11\n\tnamespace\x18\x01 \x01(\t\x12\x0f\n\x07service\x18\x02 \x01(\t\x12\x0f\n\x07version\x18\x03 \x01(\t\x12\x0e\n\x06method\x18\x04 \x01(\t\x12(\n\nparameters\x18\x05 \x03(\x0b\x32\x14.gr.ServiceCallParam2=\n\x0eServiceInvoker\x12+\n\x0cInvokeMethod\x12\x0f.gr.ServiceCall\x1a\x08.gr.Data"\x00\x62\x06proto3',
)


_DATA = _descriptor.Descriptor(
    name="Data",
    full_name="gr.Data",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="s",
            full_name="gr.Data.s",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="b",
            full_name="gr.Data.b",
            index=1,
            number=2,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"",
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="json",
            full_name="gr.Data.json",
            index=2,
            number=3,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=18,
    serialized_end=60,
)


_SERVICECALLPARAM = _descriptor.Descriptor(
    name="ServiceCallParam",
    full_name="gr.ServiceCallParam",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="name",
            full_name="gr.ServiceCallParam.name",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="data",
            full_name="gr.ServiceCallParam.data",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=62,
    serialized_end=118,
)


_SERVICECALL = _descriptor.Descriptor(
    name="ServiceCall",
    full_name="gr.ServiceCall",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="namespace",
            full_name="gr.ServiceCall.namespace",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="service",
            full_name="gr.ServiceCall.service",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="version",
            full_name="gr.ServiceCall.version",
            index=2,
            number=3,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="method",
            full_name="gr.ServiceCall.method",
            index=3,
            number=4,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="parameters",
            full_name="gr.ServiceCall.parameters",
            index=4,
            number=5,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=120,
    serialized_end=244,
)

_SERVICECALLPARAM.fields_by_name["data"].message_type = _DATA
_SERVICECALL.fields_by_name["parameters"].message_type = _SERVICECALLPARAM
DESCRIPTOR.message_types_by_name["Data"] = _DATA
DESCRIPTOR.message_types_by_name["ServiceCallParam"] = _SERVICECALLPARAM
DESCRIPTOR.message_types_by_name["ServiceCall"] = _SERVICECALL
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Data = _reflection.GeneratedProtocolMessageType(
    "Data",
    (_message.Message,),
    {
        "DESCRIPTOR": _DATA,
        "__module__": "call_pb2"
        # @@protoc_insertion_point(class_scope:gr.Data)
    },
)
_sym_db.RegisterMessage(Data)

ServiceCallParam = _reflection.GeneratedProtocolMessageType(
    "ServiceCallParam",
    (_message.Message,),
    {
        "DESCRIPTOR": _SERVICECALLPARAM,
        "__module__": "call_pb2"
        # @@protoc_insertion_point(class_scope:gr.ServiceCallParam)
    },
)
_sym_db.RegisterMessage(ServiceCallParam)

ServiceCall = _reflection.GeneratedProtocolMessageType(
    "ServiceCall",
    (_message.Message,),
    {
        "DESCRIPTOR": _SERVICECALL,
        "__module__": "call_pb2"
        # @@protoc_insertion_point(class_scope:gr.ServiceCall)
    },
)
_sym_db.RegisterMessage(ServiceCall)


_SERVICEINVOKER = _descriptor.ServiceDescriptor(
    name="ServiceInvoker",
    full_name="gr.ServiceInvoker",
    file=DESCRIPTOR,
    index=0,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
    serialized_start=246,
    serialized_end=307,
    methods=[
        _descriptor.MethodDescriptor(
            name="InvokeMethod",
            full_name="gr.ServiceInvoker.InvokeMethod",
            index=0,
            containing_service=None,
            input_type=_SERVICECALL,
            output_type=_DATA,
            serialized_options=None,
            create_key=_descriptor._internal_create_key,
        ),
    ],
)
_sym_db.RegisterServiceDescriptor(_SERVICEINVOKER)

DESCRIPTOR.services_by_name["ServiceInvoker"] = _SERVICEINVOKER

# @@protoc_insertion_point(module_scope)
