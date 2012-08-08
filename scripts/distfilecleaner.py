#!/usr/local/bin/python3.2


# distviper from sysutils/bsdadminscripts implemented in python


# Only the fast mode is implemented

# Only pkgng supported (old tools should work with few modifications to this
# script)

# For each installed package:
# - find out distinfo file for the port using origin of the package, look up
#   DISTINFO_FILE make variable if no file is found in the origin directory. 
# - Extract distfiles from the distinfo files, store name (relative to 
#   DISTDIR), size and SHA256 sum in a hash, file name as the
#   key.
# 

from pb_utils.portutils import my_popen, get_make_variable, get_installed_packages
from pb_utils.portutils import get_file_sha256
import getopt
from sys import argv, stderr
import re
from os import path, walk
from os.path import exists, getsize
import fileinput

            


# Main
def main():

    # The hash that contains the distinfo information.
    # Key in the hash is the path of the file relative to DISTDIR
    # For example "xorg/lib/libX11-1.4.4.tar.bz2"
    # Value in the hash is a another hash with size and SHA256 fingerprint as extracted
    # from the distinfo files of ports.
    distinfo = {}

    # All distinfo files for installed packages
    distinfofiles = []

    checksum_mode = False
    size_mode = False
    verbose_mode = False

    # Parse command line options
    try:
        opts, arg = getopt.getopt(argv[1:], "csv")
    except getopt.GetoptError as err:
        print(argv[0], ':', str(err))
        exit(2)

    for o, a in opts:
        if o == '-c':
            checksum_mode= True
        if o == '-s':
            size_mode = True
        if o == '-v':
            verbose_mode = True

    portsdir = get_make_variable('PORTSDIR')
    if portsdir == '':
        portsdir = '/usr/ports'
    portsdir_len = len(portsdir)

    distdir = get_make_variable('DISTDIR')
    if distdir == '':
        distdir = '/usr/ports/distfiles'
    distdir_len = len(distdir)


    # Start with getting a list of installed packages and
    # make a list of all distinfo files for installed packages.
    for origin in get_installed_packages():
        distinfo_file = '/'.join([portsdir, origin, 'distinfo']) 
        if not exists(distinfo_file):
            # Try with make(1)
            distinfo_file = get_make_variable('DISTINFO_FILE', '/'.join([portsdir, origin]))
        if exists(distinfo_file):
            distinfofiles.append(distinfo_file)
            
    # Prepare the regexp for parsing the lines
    p = re.compile('^(SHA256|SIZE) \(([^)]+)\) = ([a-z0-9]+|IGNORE)$')        
    
    # Read all the distinfo files in one loop
    for line in fileinput.input(distinfofiles):
        m = p.match(line)

        if m:
            filename = m.group(2)
            if not filename in distinfo:
                distinfo[filename] = {}
            if m.group(1) == 'SHA256':
                if verbose_mode:
                    print('SHA256 (' + filename + ') = ' + m.group(3))
                distinfo[filename]['sha256'] = m.group(3)
            else:
                if verbose_mode:
                    print('SIZE (' + filename + ') = ' + m.group(3))
                distinfo[filename]['size'] = m.group(3)
        else:
            print ('Unrecognized line in file ' + filename.filename(), file=stderr)
            print (line, file=stderr)

    # os.walk() the DISTDIR
    for root, dirs, files in walk(distdir):
        for name in files:
            distfile_fullpath = '/'.join([root, name])
            distdirfile = distfile_fullpath[distdir_len+1:]
            # Test if the file is listed in distinfo files
            if not distdirfile in distinfo:
                print(distfile_fullpath)
                continue
        
            # Test if the sha256 sum is 'IGNORE'
            if distinfo[distdirfile]['sha256'] == 'IGNORE':
                continue

            # Compare sizes if requested.
            if size_mode:
                distdirfile_size = str(getsize(distfile_fullpath))
                if distdirfile_size != distinfo[distdirfile]['size']:
                    print('SIZE\t' + distfile_fullpath)
            
            # Compare sha256 hashes if requested
            if checksum_mode:
                distdirfile_sha256 = get_file_sha256(distfile_fullpath)
                if distdirfile_sha256 != distinfo[distdirfile]['sha256']:
                    print('SHA256\t' + distfile_fullpath)

if __name__ == "__main__":
	main()
