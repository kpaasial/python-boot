#!/usr/bin/env python3.2

# Script for creating daily, weekly and monthly snapshots
# Instead of encoding TTL values into the names of the snapshots I'm
# using zfs user properties
# Snapshot naming is:
# dataset@type-YYYY-MM-DD_HH:MM:SS
# Command line arguments are:
# -a ttl    override the ttl value 
# -p	    specify prefix (without trailing dash) 
# -r	    make a recursive snapshot(s) of given datasets
# The name of the TTL property is 'zfs_snapshot:time_to_live'

# TODO: support template based naming of the snapshots

import getopt
from sys import argv,stderr
from subprocess import call
from time import strftime
from string import Template

from pbutils.zfsutils import ttl_to_seconds, TTL_PROPERTY
from pbutils.zfsutils import zfs_list

def main():
    prefix = 'snapshot'
    recursive = False
    ttlString = '1w'

    # Parse command line arguments
    try:
        opts, args = getopt.getopt(argv[1:], "a:p:r")
    except getopt.GetoptError as err:
        print(str(err))
        exit(2)

    for o,a in opts:
        if o == '-a':
            ttlString = a
        elif o == '-p':
            prefix = a 
        elif o == '-r':
            recursive = True 

    # TODO: check that the ttl is a valid ttl value
    ttl = ttl_to_seconds(ttlString)
    # Get list of all zfs datasets
    allDataSets = set(dataSet['name'] for dataSet in zfs_list())

    # Time now as YYYY-MM-DD_HH.MM.00
    timeNow = strftime("%Y-%m-%d_%H.%M") + '.00'
    #print timeNow
    # Construct the name of the snapshot
    # This could be user configurable
    snapNameTemplate = Template('${snapPrefix}-${snapTime}--${snapTTL}')
    snapShotName1 = snapNameTemplate.substitute(snapPrefix=prefix,
                                                snapTime=timeNow,
                                                snapTTL=ttlString)

    snapTemplate = Template('${snapDataSet}@${snapName}') 

    ttlProperty = TTL_PROPERTY + '=' + str(ttl)

    cmdLine = ['/sbin/zfs', 'snapshot']

    if not recursive is False:
        cmdLine.append('-r')

    cmdLine.append('-o')
    cmdLine.append(ttlProperty)

    for dataSet in args:
        if not dataSet in allDataSets:
            stderr.write('Warning: Dataset ' + dataSet +
                         ' not found, snapshot not created\n')
            continue
        snapShotName = snapTemplate.substitute(snapDataSet=dataSet,
                                               snapName=snapShotName1)

        #print(cmdLine + [ snapShotName ])
        call(cmdLine + [ snapShotName ])
        print(snapShotName)

if __name__ == "__main__":
    main()
