# This file is part of ts_idl.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License

__all__ = ["ChillerStatus", "PumpStatusFlag", "AlarmStatusFlag", "WarningStatusFlag"]

import enum


class ChillerStatus(enum.IntEnum):
    STANDBY = 1
    RUNNING = 2


class PumpStatusFlag(enum.IntEnum):
    PUMPOFF = 1
    PUMPON = 2


class AlarmStatusFlag(enum.IntEnum):
    NOALARM = 1
    ALARMPRESENT = 2


class WarningStatusFlag(enum.IntEnum):
    NOWARNING = 1
    WARNINGPRESENT = 2
