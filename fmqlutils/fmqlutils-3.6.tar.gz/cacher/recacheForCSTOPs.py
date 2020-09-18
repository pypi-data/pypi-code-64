#!/usr/bin/env python
# -*- coding: utf8 -*-

# (c) 2019-2020 caregraf

import sys
import os
import json
import re
from fmqlutils.cacher.cacher import makeFMQLIF
from fmqlutils.cacher.cacherUtils import FMQLReplyStore, DATA_LOCN_TEMPL, configLogging, recacheForCSTOPs

def cacheStopped(config, onlies=None):

    dmLocation = DATA_LOCN_TEMPL.format(config["stationNumber"])
    fmqlReplyStore = FMQLReplyStore(dmLocation, makeDir=False)
    stoppedTypes = fmqlReplyStore.stoppedTypes()
    if onlies:
        print("Only recaching {}".format(
            ", ".join(sorted(list(onlies)))
        ))
        if len(set(onlies) - set(stoppedTypes)):
            print("Removed {} from list of 'only types' as not stopped".format(
                ", ".join(sorted(list(set(onlies) - set(stoppedTypes))))
            ))
        stoppedTypes = set(onlies).intersection(set(stoppedTypes))
    if len(stoppedTypes) == 0:
        raise SystemExit("No stopped types to recache - exiting") 
    cantRecacheTyps = {}
    recached = set()
    for typ in stoppedTypes:
        try:
            recacheForCSTOPs(config["stationNumber"], typ, makeFMQLIF(config))
        except Exception as e:
            cantRecacheTyps[typ] = e
            print("Can't recache {}".format(typ))
        else:
            recached.add(typ)
    print("Done with {:,} stopped types - {:,} succeeded , {:,} failed - {}".format(
        len(stoppedTypes),
        len(recached),
        len(cantRecacheTyps),
        ", ".join(sorted(list(cantRecacheTyps)))
    ))
 
"""
> {EXE} SNO_Config -- all stopped types
or
> {EXE} SNO_Config TYP -- one stopped type
"""   
def main():

    assert sys.version_info >= (3, 6)
    
    try:
        sysConfigName = sys.argv[1].split(".")[0]
    except IndexError:
        raise SystemExit("Usage _EXE_ {SYSTEM CONFIG FILE} [{typ}]")
    
    if not os.path.isfile("{}.json".format(sysConfigName)):
        raise SystemExit("No system config file {}.json - exiting".format(sysConfigName))
    try:
        config = json.load(open("{}.json".format(sysConfigName)))
    except:
        raise SystemExit("Invalid system config {}.json - can't parse".format(sysConfigName))

    configLogging(config["stationNumber"], "cacherLog", config["logLevel"] if "logLevel" in config else "INFO")
    
    onlies = None
    if len(sys.argv) > 2:
        onlies = [sys.argv[2]]
    cacheStopped(config, onlies)

if __name__ == "__main__":
    main()
