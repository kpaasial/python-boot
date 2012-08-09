#!/usr/bin/env python3.2

# This script loops trough all zfs datasets that are of type snapshot and decides
# if they are older than what their TTL values specify.
# Names of expired snapshots are output into the standard output, one name per line.
#
# Creation dates of the snapshots are taken from the 'created' attribute
# TTL value is stored in a zfs property named 'zfs_snapshot:time_to_live'

# Usage of this script for deleting expired snapshots would be something like
# zfSnap-expired.py <options> | xargs -n1 zfs destroy



# Options:

# poolname		restrict search to snapshots in pool poolname, multiple poolnames
#			can be specified as "pool1 pool2 ..."
# -F TTL		like the -F option in zfSnap, match any snapshot older than TTL

import getopt
from sys import argv, stderr
import re
from time import time, strptime, mktime
from locale import setlocale,LC_ALL

from pbutils.zfsutils import ttl_to_seconds, TTL_PROPERTY
from pbutils.zfsutils import zfs_list, zpool_list

# Functions
 
# Gets the full list of snapshots, parse needed attributes.
# Input: none
# Returns: list of snapshots as list of (name,creationdate,ttl) tuples (this may change to include more fields). 
# restrict dealing with 'zfs list' output to here, get everything out of output
# and store it so that all information needed is neatly packaged for further processing.
# The external representation of TTL should never be needed outside of this function,
# the TTL should be just a number when handled outside of this function. This should
# allow different ways of encoding the TTL value. The default is now the zfSnap way
# but other methods could be used some day.
def get_zfs_snapshots():
    allSnapShots = zfs_list(dataSetTypes=['snapshot'],
                            properties=['name', 'creation',
                            TTL_PROPERTY])

    #print allSnapShots
    # For each snapshot in output:
    # - Get creation date attribute as seconds from the epoch 
    # - Parse the TTL value from name (or attribute) as seconds
    # Construct a list of (name, creationdate, ttl) tuples, return the list to the caller.
    results = []

    for snapShot in allSnapShots:
        #print(snapShot.decode())
        snapShotName  = snapShot['name']
        creationString = snapShot['creation']
        ttlString = snapShot[TTL_PROPERTY]

        # TODO: check if the TTL_PROPERTY somehow got an errorneus value
        if ttlString == '-':
            ttlValue = -1 # means: no TTL value
        else:
            ttlValue = int(ttlString)

	    # TODO: This looks like a dirty hack but it's fine, just add little bit of error checking
        creationDate = int(mktime(strptime(creationString, "%a %b  %d  %H:%M %Y")))
	    #print snapShotName, '\t', creationString, '\t', creationDate, '\t', ttlValue, '\n'
        results.append({'dataset': snapShotName, 'creation': creationDate, 'ttl': ttlValue})
	
    return results


# "main" program

# Read command line switches
def main():
    # set locale so parsing of locale specific data can be done
    setlocale(LC_ALL, '')

    try:
        opts, args = getopt.getopt(argv[1:], "F:")
    except getopt.GetoptError as err:
	    print(str(err)) 
	    exit(2)

    # TODO: implement this
    for o, a in opts:
        if o == '-F':
            forcedCutOff = True



    # TODO: Start by making sure all needed utilities exist


    
    # If any dataset names were given on the command line, filter the output so that
    # only the snapshots from those datasets are included
    if len(args) > 0:
        dataSetsToMatch = set()
        for arg in args:
            dataSetPlusChildren = zfs_list(arg, recursion=True)
            for dataSet in dataSetPlusChildren:
                dataSetsToMatch.add(dataSet['name'])

    else:
        dataSetsToMatch = set()
        allDataSets = zfs_list()
        for dataSet in allDataSets:
            dataSetsToMatch.add(dataSet['name'])


    # Get all snapshots
    allSnapShots = get_zfs_snapshots()


    # What time is it now?
    timeNow = int(time())

    for snapShot in allSnapShots:
	    # Skip snapshots that did not have a TTL value
        if snapShot['ttl'] == -1:
            continue
        dataSetName, snapShotTag = snapShot['dataset'].split('@')
        if (snapShot['creation'] + snapShot['ttl']) < timeNow:
            if dataSetName in dataSetsToMatch:
                print(snapShot['dataset']) 


if __name__ == "__main__":
    main()

