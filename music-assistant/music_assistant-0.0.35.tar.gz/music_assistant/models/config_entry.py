"""Model and helpers for Config entries."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List, Tuple

from mashumaro import DataClassDictMixin


class ConfigEntryType(Enum):
    """Enum for the type of a config entry."""

    BOOL = "boolean"
    STRING = "string"
    PASSWORD = "password"
    INT = "integer"
    FLOAT = "float"
    LABEL = "label"
    HEADER = "header"


@dataclass
class ConfigEntry(DataClassDictMixin):
    """Model for a Config Entry."""

    entry_key: str
    entry_type: ConfigEntryType
    default_value: Any = None
    values: List[Any] = field(default_factory=list)  # select from list of values
    range: Tuple[Any] = ()  # select values within range
    description_key: str = None  # key in the translations file
    help_key: str = None  # key in the translations file
    multi_value: bool = False  # allow multiple values from the list
    depends_on: str = ""  # needs to be set before this setting shows up in frontend
    hidden: bool = False  # hide from UI
    value: Any = None  # set by the configuration manager
    store_hashed: bool = False  # value will be hashed, non reversible
