from datetime import datetime
from typing import Generic, List, Literal, Optional, TypeVar

from dateutil.parser import isoparse
from dateutil.tz import tzlocal
from dateutil.utils import default_tzinfo
from pydantic import create_model
from pydantic.generics import GenericModel

T = TypeVar("T")

class Error(GenericModel, Generic[T]):
    data  : Literal[None] = None
    error : T

    class Config:
        extra = "allow"

class OK(GenericModel, Generic[T]):
    data  : Optional[T]
    error : Literal[None] = None

    class Config:
        extra = "allow"

class IsoDatetime(datetime):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, datetime):
            if v.tzinfo is None:
                return default_tzinfo(v, tzlocal())

            return v
        else:
            return isoparse(v).astimezone()

class _GenericMeta(type):
    def __getitem__(self, t):
        return type(self.__name__, (self,), { "__concrete_type__": t })

class CommaSeperatedList(List[T], metaclass=_GenericMeta):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, list):
            pass
        elif isinstance(v, str):
            v = v.split(",")
        else:
            raise ValueError("list or comma seperated str expected")

        m = create_model("V", xs=(List[cls.__concrete_type__], ...))
        o = m(xs=v)

        return o.xs
