from re import match
from pb_utils import my_popen

TTL_PROPERTY = 'zfs_snapshot:time_to_live'
SECONDS_MINUTE = 60
SECONDS_HOUR = 60 * SECONDS_MINUTE
SECONDS_DAY = 24 * SECONDS_HOUR
SECONDS_WEEK = 7 * SECONDS_DAY
SECONDS_MONTH = 30 * SECONDS_DAY
SECONDS_YEAR = 365 * SECONDS_DAY 

ZPOOL_LOC = '/sbin/zpool'
ZFS_LOC = '/sbin/zfs'

# Functions for dealing with timestamps
# Human readable ttl -> seconds
# Input: ttl as string representation, type: string
# Returns: ttl as seconds, type: integer
# Possible representations for TTL value:
#   number -  seconds
#   numbers - seconds
#   numberM - minutes
#   numberh - hours
#   numberd - days
#   numberw - week
#   numberm - months
#   numbery - years

def ttl_to_seconds(ttl):
    m = match(r"(\d+)([sMhdwmy]?)", ttl)
    #  Check for errors here, unrecognized string should equal -1
    if m is False:
        return -1    
    
    number = int(m.group(1))
    qualifier = m.group(2)

    if qualifier == '':
        return number
    elif qualifier == 'M':
        return SECONDS_MINUTE * number
    elif qualifier == 'h':
        return SECONDS_HOUR * number
    elif qualifier == 'd':
        return SECONDS_DAY * number
    elif qualifier == 'w':
        return SECONDS_WEEK * number
    elif qualifier == 'm':
        return SECONDS_MONTH * number
    elif qualifier == 'y':
        return SECONDS_YEAR * number

# Encapsulates Popen into a single method that does error checking and returns
# the data as a proper python string.
#def my_popen(*cmdLine, returnOutput=True):
#    if returnOutput is True:
#        stdOutFile = PIPE
#    else:
#        stdOutFile = None
#
#    try:
#        p = Popen(*cmdLine, stdout=stdOutFile)
#    except OSError as err:
#        print (err, file=sys.stderr)
#        return
#    
#    if returnOutput is True:
#        output = p.communicate()[0]
        # TODO: Check for errors, check that different locale does
        # not affect what we get as output
#        decodedOutput = output.decode()
#        return decodedOutput



# Interface to 'zpool list' 
#
def zpool_list(*pools, properties=['name']):
    # TODO: handle errors
    cmdLine = [ZPOOL_LOC, 'list']
    cmdLine.append('-H')
    cmdLine.extend(['-o', ','.join(properties)])
    cmdLine.extend(pools)

    output = my_popen(cmdLine).splitlines() 
    resultList = []
    for line in output:
        result = {}
        fields = line.split('\t')
        # TODO: Check that fields has the same number of
        # items as properties
        for i, prop in enumerate(properties):                         
            result[prop] = fields[i]
        resultList.append(result)

    return resultList

# The generic interface to 'zfs list'
# Inputs:
#	        - Types of datasets to include, filesystem|volume|snapshot|all or any 
#             combination of first three, default is ['filesystem']  
#	        - Recurse into child datasets of the given datasets 
#             (-r option of 'zfs list'), Boolean, default off.
#	        - Recursion depth (-d option of 'zfs list'), Number, default -1 
#	        - List of properties to get for each dataset, default ['name']
#           - Filter for datasets to include in output, list of datasets,
#             the *dataSets -parameter gathers these.

#	    
# Returns:  - List of dictionary objects with keys in the dictionary objects as
#             they are in the 'zfs list' output without the -H option
#             (for example 'name', 'type', 'mountpoint', 'creation' etc.)
#             and values from the matching columns in the output.
#	        - Values are returned as strings with no attempt to validate,
#	          sanitize or convert them (other than converting raw byte sequences
#	          to python strings).

def zfs_list(*dataSets, recursion=False, recursionDepth=-1,
             dataSetTypes=['filesystem'],
             properties=['name']):


    # TODO: validate dataSetTypes against allowed values

    cmdLine = [ZFS_LOC, 'list']
    if recursion is True:
        cmdLine.append('-r')
    elif recursionDepth >= 0:
        cmdLine.extend(['-d', str(recursionDepth)]) 
    cmdLine.append('-H')
    cmdLine.extend(['-o', ','.join(properties)])
    cmdLine.extend(['-t', ','.join(dataSetTypes)])
    cmdLine.extend(dataSets)

    #print(cmdLine)
    #p = Popen(cmdLine, stdout=PIPE)
    output = my_popen(cmdLine).splitlines()
    # print(output)

    resultList = []
    for line in output:
        result = {}
        fields = line.split('\t')
        # TODO: Check that fields has the same number of items as properties
        for i, prop in enumerate(properties):
            result[prop] = fields[i]
            
        resultList.append(result)

    return resultList

# Reads a zfs property
# Inputs: dataset(filesystem) name, property name
# TODO: provide generic interface to 'zfs get'
def zfs_get(dataset, zfs_property):
    return my_popen(['zfs', 'get', '-H', '-p', '-o', 'value', zfs_property,
                    dataset]).rstrip()

# Sets a zfs property
# Can not unset a property, use zfs_inherit() for that
def zfs_set():
    pass

# Unsets a property, recursion supported
def zfs_inherit():
    pass



# Create a zfs dataset
def zfs_create():
    pass


# Create a zfs snapshot
def zfs_snapshot():
    pass

# Destroy a zfs dataset, volume or snapshot
def zfs_destroy():
    pass



