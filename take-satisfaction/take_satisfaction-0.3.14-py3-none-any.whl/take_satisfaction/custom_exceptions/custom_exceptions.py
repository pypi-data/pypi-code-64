__author__ = 'Milo Utsch'
__version__ = '0.1.0'
__all__ = [
    'InvalidDataframeError',
    'AbsentColumnError',
    'NoSuitableTranslationError',
    'InvalidActionType'
]


class InvalidDataframeError(Exception):
    pass


class AbsentColumnError(Exception):
    pass


class NoSuitableTranslationError(Exception):
    pass


class InvalidActionType(Exception):
    pass
