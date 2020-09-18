#!/usr/bin/env python
# -*- coding: utf8 -*-

# (c) 2015-2020 caregraf

import os
import re 
import sys
import json
from datetime import datetime
from collections import defaultdict
import logging

from fmqlutils.cacher.cacherUtils import LOG_LOCN_TEMPL

def reportTrackedFiles(stationNo):
    trackZeroFile = "{}trackZeroFiles.json".format(LOG_LOCN_TEMPL.format(stationNumber))
    trackZeroNPartial = json.load(open(trackZeroFile))
    print("Partials", json.dumps(trackZeroNPartial["partials"]))
    print()
    print("Zeros", json.dumps(trackZeroNPartial["zeros"]))
    print()
    
# ################################# DRIVER #######################

def main():

    assert sys.version_info >= (3, 6)

    try:
        stationNo = sys.argv[1]
    except IndexError:
        raise SystemExit("Usage _EXE_ STATIONNO")
        
    reportTrackedFiles(stationNo)
