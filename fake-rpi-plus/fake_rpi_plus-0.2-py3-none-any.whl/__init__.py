###############################################
# The MIT License (MIT)
# Copyright (c) 2017 Kevin Walchko
# see LICENSE for full details
##############################################
# from __future__ import print_function
import fake_rpi.RPi
import fake_rpi.smbus

from . import picamera, serial
from .Adafruit import LSM303
from .wrappers import printf, toggle_print

try:
    from importlib.metadata import version  # type: ignore
except ImportError:
    from importlib_metadata import version  # type: ignore
