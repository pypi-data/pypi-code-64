#!/usr/bin/env python
# -*- coding: utf8 -*-

# (c) 2017-2020 caregraf

import os
import sys
import json
import shutil
from datetime import datetime
import re
from collections import defaultdict
from statistics import mean
try:
    from statistics import multimode
except: # 3.8 only
    pass

from .. import VISTA_DATA_BASE_DIR
from ..cacher.cacherUtils import FMQLReplyStore, convert_size, metaOfVistA
from .reportUtils import MarkdownTable, reportPercent, reportAbsAndPercent

"""
TODO:
- expand cacher to maintain and create file
  - cacher to expand the trackFilesCached with LIMIT used, CSTOP used + total actually cached => easy to see where FM wrong and by how much
    - add to utility to dynamically regenerate!
  - report on the FM mismatch + replace lookup of lastReply with this running total file
- ... then work [1] flips (see mults inside that matter) and [2] other reports of nuance (see shells)
"""
def reportCacheHealth(stationNumber):

    print("Loading Cache Data ...")
    dataLocn = "{}{}/Data/".format(VISTA_DATA_BASE_DIR, stationNumber)   
    fmqlReplyStore = FMQLReplyStore(dataLocn, makeDir=False)
    
    expectedCountByType = fmqlReplyStore.expectedTypeCounts()
    availableTypes = fmqlReplyStore.availableTypes()
    sizeByFileTypeByReplyFile = fmqlReplyStore.replySizeByType() # actual, compressed per reply

    stoppedTypes = fmqlReplyStore.stoppedTypes()    
    try: # TODO: this should move into the FMQLReplyStore?
        partialsAndZeros = json.load(
            open("{}{}/Logs/trackFilesCached.json".format(VISTA_DATA_BASE_DIR, stationNumber))
        )
    except:
        partialsAndZeros = {}
    zeroTypes = partialsAndZeros.get("zeros", [])
    partialTypes = partialsAndZeros.get("partials", [])
    print("... cache data loaded")

    meta = metaOfVistA(stationNumber)

    mu = """---
layout: default
title: {}
---

""".format("{} Cache".format(stationNumber))

    mu += "# Cache of _{}_\n\n".format(stationNumber)

    mu += """Reports are created from data cached from clones of production VistAs and the  __comprehensiveness and arrangement of data in caches is key both for effective reporting__ and for the longer term goal of creating __full fidelity copies of VistAs after they are retired__. 
    
The following _utility report_ shows the [1] completeness, [2] relative and recommended size and [3] 'skewness' of the data cached from a clone of VistA {} [{}], cut on {}. It is intended to [a] guide more effective re-caching of this system, [b] efficient caching of further systems and [c] reframing of cached data to better highlight underlying details.\n\n""".format(
        meta["name"],
        stationNumber,
        meta["cutDate"]
    )

    mu += muCompleteness(expectedCountByType, availableTypes, sizeByFileTypeByReplyFile, stoppedTypes, zeroTypes, partialTypes)   
    mu += muLimitToSize(expectedCountByType, sizeByFileTypeByReplyFile, fmqlReplyStore, stoppedTypes)
    mu += muSkewMultiples(expectedCountByType, sizeByFileTypeByReplyFile)
    
    mu += muFileManCountWrong() # TODO <------ need real vs est #'s
    mu += muFileManRecordSizeVsCount()

    open("{}{}/ReportSite/cache.md".format(VISTA_DATA_BASE_DIR, stationNumber), "w").write(mu)
        
"""
Report on what's done and what remains to be done
"""
def muCompleteness(expectedCountByType, availableTypes, sizeByFileTypeByReplyFile, stoppedTypes, zeroTypes, partialTypes): # based on FM numbers

    print("Reporting Completeness ...")
    
    mu = "\n## Completeness\n\n"
    
    MAXTHRESHOLDLABEL = "MORE THAN TEN MILLION"
    thresholds = [[10000000, "< TEN MILLION", False], [1000000, "< ONE MILLION", False], [100000, "< ONE HUNDRED THOUSAND", False], [50000, "< FIFTY THOUSAND", False], [10000, "< TEN THOUSAND", False], [1000, "< ONE THOUSAND", False], [100, "< ONE HUNDRED", False], [10, "< TEN", False], [2, "SINGLETONS", False], [1, "ZERO", False], [0, "LESS THAN ZERO (WRONG)", False]]
    thresholds.insert(0, [-1, MAXTHRESHOLDLABEL, False])

    currentThreshold = MAXTHRESHOLDLABEL
    typByThreshold = defaultdict(list)    
    totalRecords = sum(expectedCountByType[typ]["count"] for typ in expectedCountByType if expectedCountByType[typ]["count"] > 0)
    recordsCached = 0
    uncachedTypes = []
    typByThres = defaultdict(list)
    thresOfTyp = {}
    for i, typ in enumerate(sorted(expectedCountByType, key=lambda x: expectedCountByType[x]["count"], reverse=True), 1):
        for thresInfo in thresholds:
            if not thresInfo[2]:
                if expectedCountByType[typ]["count"] < thresInfo[0]:
                    thresId = thresInfo[1]
                    thresInfo[2] = True  
                    currentThreshold = thresId
                    break
        # TODO: ideally show up earlier (prior pass) - do md after pass summing up
        typByThreshold[currentThreshold].append(typ)
        thresOfTyp[typ] = currentThreshold
        if typ in availableTypes:
            recordsCached += expectedCountByType[typ]["count"] 
            continue
        if typ in stoppedTypes or typ in zeroTypes or typ in partialTypes:
            continue
        uncachedTypes.append(typ)
    incompleteTypes = set(stoppedTypes).union(set(partialTypes)).union(set(uncachedTypes))
                
    mu += """Of <span class='countHigh'>{:,}</span> file types, <span class='countHigh'>{}</span> with contents have been completely cached, <span class='countHigh'>{:,}</span> were partially cached and <span class='countHigh'>{}</span> were confirmed as empty. Of <span class='countHigh'>{:,}</span> expected records, <span class='countHigh'>{:,}</span> have been cached.
    
""".format(
        len(expectedCountByType),
    
        reportPercent(
            len(availableTypes),
            len(expectedCountByType)
        ),
        len(partialTypes) if len(partialTypes) < 50 else reportPercent(len(partialTypes), len(expectedCountByType)),
        reportPercent(
            len(zeroTypes),
            len(expectedCountByType)        
        ),
        totalRecords,
        recordsCached
    )
    
    if len(incompleteTypes):
        mu += "This leaves <span class='countHigh'>{}</span> wholly or incompletely cached types ...\n\n".format(reportAbsAndPercent(len(incompleteTypes), len(expectedCountByType)))
        
        tbl = MarkdownTable(["\#", ":Type", "Expected Size", "Incompleteness"], includeNo=False)
        currentThresId = ""
        for i, typ in enumerate(sorted(incompleteTypes, key=lambda x: expectedCountByType[x]["count"], reverse=True), 1):
            typThresId = thresOfTyp[typ]
            if currentThresId != typThresId:
                currentThresId = typThresId
                tbl.addRow([
                    "&nbsp;",
                    "&nbsp;",
                    "__{}__".format(
                        thresOfTyp[typ]                       
                    ),
                    "&nbsp;"
                ])
            incompleteness = "ALL"
            if typ in stoppedTypes:
                incompleteness = "STOPPED"
            elif typ in partialTypes:
                incompleteness = "PARTIAL"
            tbl.addRow([
                "{:,}".format(i), 
                f'__{expectedCountByType[typ]["label"]}__ [{re.sub("_", ".", typ)}]', 
                reportAbsAndPercent(expectedCountByType[typ]["count"], totalRecords),
                incompleteness
            ])                            

        mu += tbl.md() + "\n\n"
    
    print("... finished Completeness analysis")
    return mu
        
"""
Calculates new limits based on a TARGET REPLY SIZE IN BYTES - don't want to exceed it but want to be close to it

Issue: for multiple-rich which skew right (extremes large but most smaller), this means the mean and median will be very small. Only working CSTOP can change this where a 
custom but reasonable CSTOP would leave STOPPED replies that are handled in a further pass.
  
TODO: slow part is loading last reply in all cases to get the actual limit used. Will be replaced by actual calculation later.
"""
def muLimitToSize(expectedCountByType, sizeByFileTypeByReplyFile, fmqlReplyStore, stoppedTypes):

    print("Reporting Size and Limits ...")

    TARGET_REPLY_IN_BYTES = 8900000 # 8.5MB - raw or actual, not zipped
    DEFAULT_CSTOP = 1000

    mu = "## New Limit Specifications\n\n"
                      
    typsWithNewLimits = {}
    increased = 0
    tbl = MarkdownTable([
        ":Type", "\# Replies", "Limit", "CSTOP", "New Limit"
    ])
    for i, flTyp in enumerate(sorted(sizeByFileTypeByReplyFile, key=lambda x: float(re.sub(r'\_', '.', x))), 1):
        if i % 100 == 0:
            print(f'Analyzed another 100 file types to {i}')
        sizes = [sizeByFileTypeByReplyFile[flTyp][fl]["actual"] for fl in sizeByFileTypeByReplyFile[flTyp]]        
        noReplies = len(sizeByFileTypeByReplyFile[flTyp])
        fraction = round((float(max(sizes)) / float(TARGET_REPLY_IN_BYTES)), 1)
        """
        Don't be too exact - within 0.9 to 1.1 of the size is fine
        and if only one reply that's small - then that's fine
        """
        if (noReplies > 1 and (fraction > 1.1 or fraction < 0.9)) or (noReplies == 1 and fraction > 1.1):
            # get limit from last reply
            lastReply = fmqlReplyStore.lastReplyOfType(flTyp)
            limit = int(lastReply["fmql"]["LIMIT"])
            cstop = int(lastReply["fmql"]["CSTOP"])
            if flTyp in stoppedTypes:
                cstopMU = "__{:,}__ [STOPPED]".format(cstop)
            elif cstop != DEFAULT_CSTOP:
                cstopMU = "__{:,}__".format(cstop)
            else:
                cstopMU = cstop
            newLimit = int(round(limit / fraction, 0)) 
            typsWithNewLimits[flTyp] = str(newLimit)
            newLimitMU = "__{}__".format(newLimit) if fraction >= 3 or fraction <= 0.3 else newLimit
            if newLimit > limit:
                increased += 1
            row = [
                f'__{expectedCountByType[flTyp]["label"]}__ [{re.sub("_", ".", flTyp)}]',
                noReplies,  
                limit, 
                cstopMU,
                f'{newLimitMU} [{fraction}]' if newLimit > limit else f'{newLimitMU} [{fraction}]'
            ]
            tbl.addRow(row)

    mu += "Based on a reply size threshold of <span class='countHigh'>{}</span> and only allowing .9 to 1.1 variation, <span class='countHigh'>{}</span> of cached file types need new limits. <span class='countHigh'>{}</span> need an increase, <span class='countHigh'>{}</span> a decrease.\n\n".format(
        convert_size(TARGET_REPLY_IN_BYTES),
        reportPercent(
            len(typsWithNewLimits),
            len(sizeByFileTypeByReplyFile)
        ),
        reportPercent(
            increased,
            i
        ),
        reportPercent(
            i - increased,
            i
        )
    )
    mu += tbl.md() + "\n\n"
    
    mu += "Dump:\n\n"
    mu += "> {}\n\n".format(json.dumps(typsWithNewLimits))
    
    print("Finished size and limit report")
    return mu
    
"""
Skews are not normal - they skew left (small outliers) or right (big outliers) are due
to:
- large numbers of properties not been used in some cases but are used in others
- word proc properties varying in size
- MAINLY: multiples ... Flip Candidates [want to make graph, not hier docs and highlight distinct data]
Note that new limit has no effect on the below 

TODO: separate out flip/multiple candidates.

FLIP from before: TODO revise
    ["2", "3_9", "38_1", "53_41", "53_51", "55", "58_601", "63", "67_9", "68", "357_1", "396_4", "2006_82", "19908_5"]
... most resonate with WWW data but not all and WWW has alot more.

skewness is a measure of the asymmetry
https://en.wikipedia.org/wiki/Skewness#Pearson's_moment_coefficient_of_skewness

"""
def muSkewMultiples(expectedCountByType, sizeByFileTypeByReplyFile):

    """
    Usefulness or otherwise of stats here: sigma (std div) and mean (mu) don't play as 
    much as iqr, median for spread as the reply sizes of interest are not normally     
    distributed, are skewed.

    For CSTOPabble, multiple bearing types, we DON'T expect a normal distribution of sizes 
    where mean=median. We expect a scew left (small pull) where mean < median or scew 
    right with large values pulling the mean > median.
    """
    def distribution(sizes):
        # mid pt between smallest and median, median, mid point between smallest and highest
        try: # tmp allow for < 3.8
            quartiles = statistics.quantiles(sizes, method="inclusive") # inc matched numpy
        except:
            import numpy
            quartiles = [numpy.percentile(sizes, 25), numpy.percentile(sizes, 50), numpy.percentile(sizes, 75)]
        iqr = quartiles[2] - quartiles[0] # interquartile range
        return quartiles, iqr

    print("Reporting Skews ...")

    mu = "## Skewed Types\n\n"
    
    mu += "In the following, a type is _skewed_ if it has _3 or more replies_ and the range of those replies is more than _50%_ of the median size. Such skews either mean [1] many optional properties or [2] variety of volumes of multiple containment. The latter suggests reframing of cached data to conform to a graph rather than a hierarchal document model. Such a re-arrangement would properly highlight distinct data now hidden under another type.\n\n"
                              
    tbl = MarkdownTable([
        ":Type", 
        "\# Replies", 
        "Smallest",
        "Largest",
        "Skew", 
        "Range % Median"
    ])
    i = 0
    for flTyp in sorted([flTyp for flTyp in sizeByFileTypeByReplyFile], key=lambda x: float(re.sub(r'\_', '.', x))):
        noReplies = len(sizeByFileTypeByReplyFile[flTyp])
        if noReplies < 3: # need two regular and then others
            continue
        if i % 100 == 0:
            print(f'Analyzed another 100 file types to {i}')
        sizes = [sizeByFileTypeByReplyFile[flTyp][fl]["actual"] for fl in sizeByFileTypeByReplyFile[flTyp]][0:-1] # drop the last (partial) reply
        quartiles, iqr = distribution(sizes)
        smallest = min(sizes)
        biggest = max(sizes)
        rng = biggest - smallest
        if rng/quartiles[1] < .5: # cutting off at range < .5
            continue # want 
        skew = "LEFT" if mean(sizes) < quartiles[1] else "RIGHT"
        romMU = reportPercent(rng, quartiles[1])
        # Highlight if over 50 -- indication of FLIP?
        romMU = "__{}__".format(romMU) if rng/quartiles[1] > 0.5 else romMU
        row = [
            f'__{expectedCountByType[flTyp]["label"]}__ [{re.sub("_", ".", flTyp)}]',
            noReplies,
            convert_size(min(sizes)),
            convert_size(max(sizes)),
            skew,
            romMU
        ]
        tbl.addRow(row)

    mu += tbl.md() + "\n\n"
        
    print("... Finished Skew (Multiple) Report")
    return mu 
    
"""
Reported as zero or -1 but not (want real count)
Actually 0 though reported as 

CACHER SHOULD LOG more than partials etc to let this report in all avoid
having to go into the cache (if file missing => must go in)
"""
def muFileManCountWrong():
    return ""
    
"""
Show the spread of record size, #'s and total space - suggest Mongo or otherwise
containment for smaller (singleton metas) etc

... want to fix this in config so biggest files (in reality) get enough time
"""
def muFileManRecordSizeVsCount():
    return ""

# ############################# Driver ####################################

def main():

    assert sys.version_info >= (3, 6)

    USAGE = "Usage _EXE_ STATIONNO"
    try:
        stationNumber = sys.argv[1]
    except IndexError:
        raise SystemExit(USAGE)

    reportCacheHealth(stationNumber)
    
if __name__ == "__main__":
    main()
