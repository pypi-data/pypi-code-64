#!/usr/bin/env python
# -*- coding: utf8 -*-

# (c) 2017-2020 caregraf

import os
import sys
import re
import json
from collections import defaultdict, Counter
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging

from .. import VISTA_DATA_BASE_DIR
from ..cacher.cacherUtils import FMQLReplyStore, FilteredResultIterator
from .reduceReportType import TYPER_REDUCTIONS_LOCN_TEMPL
from .reduceType import DEFAULT_MAX_NOMINAL_VALUES
from ..reporter.reportUtils import muBVC

"""
Expect 1 ALL (returned first) and many sub's with one or more properties. Note
that may have > that number of properties in split. 'expectSubTypeProperty' 
enforces the minimum.
"""
def splitTypeDatas(stationNo, typ, reductionLabel="", expectSubTypeProperties=[], expectSubTypeProperty="", expectNotEfficientWalked=False):
    if expectSubTypeProperty: # for backward compatibility
        expectSubTypeProperties = [expectSubTypeProperty]
    typeDatas = json.load(open(TYPER_REDUCTIONS_LOCN_TEMPL.format(stationNo) + "{}{}Reduction.json".format(typ, reductionLabel)))
    if isinstance(typeDatas, dict): # old and dictionary only of ALL
        return typeDatas, []
    allTypeDatas = [typeData for typeData in typeDatas if "_subTypeId" not in typeData]
    if len(allTypeDatas):
        if len(allTypeDatas) != 1:
            raise Exception("Expect one and only one ALL type data in a type data list")
    allTypeData = allTypeDatas[0]
    if expectNotEfficientWalked and "_efficientWalked" in allTypeData:
        raise Exception("Was efficient walked and shouldn't be")
    subTypeDatas = [typeData for typeData in typeDatas if "_subTypeId" in typeData]
    if len(subTypeDatas) and len(expectSubTypeProperties):
        subTypeProps = set(subTypeDatas[0]["_subTypeId"].split(":")[0].split("-"))
        if subTypeProps != set(expectSubTypeProperties):
            raise Exception("Expect sub type prop(s) \"{}\" but st has \"{}\"".format(":".join(sorted(expectSubTypeProperties)), subTypeDatas[0]["_subTypeId"]))
    elif expectSubTypeProperty:
        raise Exception("No sub type datas but expect {} as sub type property".format(expectSubTypeProperty))
    return allTypeData, subTypeDatas
    
"""
Combine sub types to broader criteria (including no criteria)

ex/ combineSubTypes(sts, ["prop1"]) where break is prop1, pr...
"""
def combineSubTypes(sts, subTypePropsSubset=[], forceCountProps=[], forceCountAllProps=False):
    def makeWantedSubTypeId(st, propsWanted):
        propsWanted = sorted(propsWanted)
        pieces = st["_subTypeId"].split(":")
        props = pieces[0].split("-")
        if len(set(propsWanted) - set(props)):
            raise Exception("Expect props wanted to be subset of those in st")
        allValues = [pieces[i] for i in range(1, len(pieces))]
        values = []
        for i, prop in enumerate(props):
            if prop in propsWanted:
                values.append(allValues[i])
        return "{}:{}".format("-".join(propsWanted), ":".join(values))
    stsBySTIdWanted = defaultdict(list)
    # ALL or broader groups
    if len(subTypePropsSubset):
        try:
            makeWantedSubTypeId(sts[0], subTypePropsSubset)
        except:
            raise Exception("Can't combine as subtype properties wanted aren't all in sts")
        for st in sts:
            stIdWanted = makeWantedSubTypeId(st, subTypePropsSubset)
            stsBySTIdWanted[stIdWanted].append(st)
    else:
        stsBySTIdWanted["ALL"] = sts
    createDateProp = "" if "_createDateProp" not in sts[0] else sts[0]["_createDateProp"]
    csts = []
    for stIdWanted in sorted(stsBySTIdWanted):
        # only prop kept  
        cst = {"_subTypeId": stIdWanted, "_total": 0}
        if createDateProp:
            cst["_createDateProp"] = createDateProp
        csts.append(cst)
        """
        For now, not taking 'rangeTypes', "firstCreateDate" or "range" and not
        the reduction of LIST ie/ just the counters and counts
        """
        for st in stsBySTIdWanted[stIdWanted]:
            cst["_total"] += st["_total"]
            for prop in st:
                if re.match(r'_', prop):
                    continue
                if prop not in cst:
                    cst[prop] = dict((field, st[prop][field]) for field in st[prop] if field in ["count", "type", "byValueCount", "byWeekDay", "firstCreateDate", "lastCreateDate"])
                    continue
                if "firstCreateDate" in cst[prop] and "lastCreateDate" in cst[prop]:
                    if "firstCreateDate" in st[prop] and "lastCreateDate" in st[prop]:
                        if st[prop]["firstCreateDate"] < cst[prop]["firstCreateDate"]:
                            cst[prop]["firstCreateDate"] = st[prop]["firstCreateDate"]
                        if st[prop]["lastCreateDate"] > cst[prop]["lastCreateDate"]:
                            cst[prop]["lastCreateDate"] = st[prop]["lastCreateDate"]                        
                    else: # may be overly cautious
                        del cst[prop]["firstCreateDate"]
                        del cst[prop]["lastCreateDate"]
                cst[prop]["count"] += st[prop]["count"]
                # merge counter only if in cst already; otherwise ignore. If not in st
                # then remove from cst ie/ either all with prop have cntType or no merge
                for cntType in ["byValueCount", "byWeekDay"]:
                    if cntType in cst[prop]:
                        if cntType in st[prop]: 
                            cst[prop][cntType] = Counter(cst[prop][cntType]) + Counter(st[prop][cntType])
                            # can get huge - ex IPs in user etc (typer does the same)
                            if forceCountAllProps == False and prop not in forceCountProps and len(cst[prop][cntType]) > DEFAULT_MAX_NOMINAL_VALUES:
                                del cst[prop][cntType]
                        else: # only delete from cst if another st with prop has none
                            del cst[prop][cntType]
    return csts
    
"""
Check Data: array of fileType and what's needed (array)
... ALL | TYPE | {REDUCTIONLABEL}

TODO/CONSIDER: -S variation ex fl = re.sub(r'\-0', '-S-0', fl) but consider
whether to just warn and force a STOP

Ex/ [{"fileType": "3_081", "check": "TYPE"}]
"""
def checkDataPresent(stationNumber, dataToCheck):
    hasAll = True
    for dataInfo in dataToCheck:
        ftyp = dataInfo["fileType"]
        if not isinstance(dataInfo["check"], list):
            dataInfo["check"] = [dataInfo["check"]]
        checked = {}
        for toCheck in dataInfo["check"]:
            if re.match("ALL", toCheck):
                if toCheck == "ALL":
                    # note: doesn't check completeness. One will do!
                    fl = "{}{}/Data/{}".format(VISTA_DATA_BASE_DIR, stationNumber, "{}-0.zip".format(ftyp))
                elif toCheck == "ALLRF":
                    fl = "{}{}/DataRF/{}".format(VISTA_DATA_BASE_DIR, stationNumber, "{}-0.zip".format(ftyp))
                else:
                    raise Exception("ALL options are ALL|ALLRF")
                if not os.path.isfile(fl):
                    checked[toCheck] = False
                    hasAll = False
                else:
                    checked[toCheck] = True
                continue
            reductionLabel = toCheck if toCheck != "TYPE" else ""
            fl = TYPER_REDUCTIONS_LOCN_TEMPL.format(stationNumber) + "{}{}Reduction.json".format(ftyp, reductionLabel)
            if not os.path.isfile(fl):
                checked[toCheck] = False
                hasAll = False
            else:
                checked[toCheck] = True
        del dataInfo["check"]
        dataInfo["checked"] = checked
    return hasAll, dataToCheck
    
"""
Convenience function for manipulating type reductions

Note: no need for singleValueCount as if singleValue => red[prop]["count"] has value
"""
def singleValue(typeRed, prop, ifMissingValue=""):
    if prop not in typeRed:
        if ifMissingValue:
            return ifMissingValue
        raise Exception("Unexpected missing property {} of reduction".format(prop))
    if not ("byValueCount" in typeRed[prop] and len(typeRed[prop]["byValueCount"]) == 1):
        raise Exception("Unexpected > 1 value for prop {} of reduction".format(prop))
    return list(typeRed[prop]["byValueCount"])[0]
    
"""
mu a bvc

Note: forceShowCount is to allow an ST BVC use to force a count for
a single value if count < total
"""
def muBVCOfSTProp(st, prop, separator=", ", addNotSet=True):
    if prop not in st:
        return "" # don't say NOTSET - just leave blank
    valueInfo = st[prop]
    if "byValueCount" not in valueInfo:
        raise Exception("Value missing BVC")
    bvc = valueInfo["byValueCount"]
    if addNotSet and st[prop]["count"] < st["_total"]:
        bvc["NOTSET"] = st["_total"] - st[prop]["count"]
    return muBVC(bvc, separator, st["_total"] != st[prop]["count"])
    
def thresholdProps(typeData):
    thresholds = [1.0, 0.99, 0.95, 0.9, 0.8, 0.5, 0.25, 0.1, 0.05]
    currentThresholdIndex = 0
    byThreshold = defaultdict(list)
    total = typeData["_total"]
    for j, prop in enumerate(sorted([key for key in typeData if not re.match(r'\_', key)], key=lambda x: typeData[x]["count"], reverse=True), 1):
        level = float(typeData[prop]["count"])/float(total)
        thresholdIndex = [i for i, t in enumerate(thresholds) if level <= t][-1]
        if thresholdIndex != currentThresholdIndex:
            currentThresholdIndex = thresholdIndex
        byThreshold[thresholds[currentThresholdIndex]].append(prop)
    return byThreshold

# ex/ refsOfST(st, "200") <=> userRefsOfST
def refsOfST(st, typ):
    refs = set()
    for prop in st:
        if re.match(r'\_', prop):
            continue
        if st[prop]["type"] == "LIST":
            refs |= refsOfST(st[prop]["reduction"], typ)
        if "rangeTypes" not in st[prop]:
            continue
        if typ not in st[prop]["rangeTypes"]:
            continue
        if "byValueCount" not in st[prop]:
            raise Exception("By Value Count not supported for {}/{}".format(st["_subTypeId"], prop))
        for ref in st[prop]["byValueCount"]:
            if not re.search(f'{typ}\-', ref):
                continue
            refs.add(ref)
    return refs 

"""
Time Series CSV for a type, using a day prop.

You can use upToDay (typically cutDate) but ONLY when dayProp is the type's creation property. timeBack is of form:
    {"months": #} or {"days": #} or {"years": #} or a combination ie/ > 1 arg

Specifically, header row and array of data rows as single string values
    "Date,ColId1,ColId2..."
    "2020-...,#,#"
    ...
where ColId1 ... breakdown by the Splitter. If there is no Splitter then
you see
    "Date,ALL"
    
Ex/ Splitter

    class Splitter:
        def __init__(self, stationNo):
            self.__stationNo = stationNo
        def split(self, resource):
            if ...
                return "" # suppress
            ... categorize
            return colId
    
Splitter can also SUPPRESS entries (ex/ if walking visits and only want encounters,
then can suppress the irrelevant)
    
Returns rows

Fits into a Pandas DF
    df = pd.read_csv(
        io.StringIO("\n".join(rows)),
        index_col=0, 
        parse_dates=True
    )
(not returning as easier to just serialize string for now)
    
To get colIds for display:
    rows[0].split(",")[1:]
"""        
def makeTypeTSCSVByDay(stationNo, typId, dayProp, upToDay="", timeBack=None, splitter=None):

    dataLocn = "{}{}/Data/".format(VISTA_DATA_BASE_DIR, stationNo) 
    if upToDay and timeBack:
        upToDayDT = datetime.strptime(upToDay.split("T")[0], "%Y-%m-%d")
        # timeBack == {"years": #} etc.
        onAndAfterDayDT = upToDayDT - relativedelta(**timeBack)
        onAndAfterDay = datetime.strftime(onAndAfterDayDT, "%Y-%m-%d")
        store = FMQLReplyStore(dataLocn)
        startAtReply = store.firstReplyFileOnOrAfterCreateDay(typId, dayProp, onAndAfterDay)
        print(f'TS CSV: iterating {typId} starting with reply {startAtReply} from {onAndAfterDay} to {upToDay} for creation property {dayProp}')
    else:
        onAndAfterDay = ""
        print(f'TS CSV: iterating {typId} from the start of data for property {dayProp}')
    resourceIter = FilteredResultIterator(dataLocn, typId, startAtReply=startAtReply)
    dayCounts = defaultdict(lambda: Counter())
    colIds = set()
    colId = "ALL"
    for resource in resourceIter:
        if dayProp not in resource:
            print(f'** Warning: missing {dayProp} from resource {resource["_id"]} - skipping')
            continue
        dt = resource[dayProp]["value"].split("T")[0]
        if onAndAfterDay:
            if dt < onAndAfterDay:
                continue
            if dt >= upToDay:
                break # assuming order
        if splitter:
            colId = splitter.split(resource)
            if colId == "": # can suppress
                continue
            colIds.add(colId)
        dayCounts[dt][colId] += 1
    colIds = sorted(list(colIds)) if len(colIds) else ["ALL"]
    rows = [f'Date,{",".join(colIds)}']
    for dt in sorted(dayCounts):
        row = [dt]
        for colId in colIds:
            cnt = 0 if colId not in dayCounts[dt] else dayCounts[dt][colId]
            row.append(str(cnt))
        rows.append(",".join(row))
    print(f'Returning TS with {len(colIds)} criteria over {len(rows)-1} dates from {rows[1].split(",")[0]} to {rows[-1].split(",")[0]}')
    return rows
