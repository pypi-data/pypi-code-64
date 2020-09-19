import logging

from importlib_metadata import version

from logtron.autodiscover import autodiscover

try:
    __version__ = version(__package__)
except:
    __version__ = "unspecified"


def flush(name=None):
    for i in logging.getLogger(name).handlers:
        i.flush()
