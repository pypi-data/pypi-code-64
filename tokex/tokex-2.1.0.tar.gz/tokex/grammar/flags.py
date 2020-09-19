# Singular Token Flags
NOT = "!"
QUOTED = "q"
UNQUOTED = "u"
CASE_SENSITIVE = "s"
CASE_INSENSITIVE = "i"

__MUTUALLY_EXCLUSIVE__ = (
    {CASE_SENSITIVE, CASE_INSENSITIVE},
    {QUOTED, UNQUOTED}
)

DEFAULTS = frozenset((
    CASE_INSENSITIVE,
))

__all__ = [
    "NOT",
    "QUOTED",
    "UNQUOTED",
    "CASE_SENSITIVE",
    "CASE_INSENSITIVE"
]
