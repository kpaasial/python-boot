#!/usr/local/bin/python3.2

# Tool to clean up /var/db/ports, much like portmaster --check-port-dbdir

# - First find out list of installed packages like in distfilecleaner.
# - Find out UNIQUENAME for each installed package
# - Create a list of PORT_DBDIR/uniquename/options files
# - Check which of the files are found in the list of UNIQUENAMEs
#   created from installed packages.
# - Print out names of orphaned options -files.

from os import walk
from os.path import split
from pb_utils import my_popen, get_make_variable, get_installed_packages

portsdir = '/usr/ports'
port_dbdir = '/var/db/ports'

# Main
def main():

    uniquenames = set()

    for origin in get_installed_packages():
        uniquename = get_make_variable('UNIQUENAME', '/'.join([portsdir, origin]))
        uniquenames.add(uniquename)

    # os.walk the PORT_DBDIR, check each file named 'options' if the last part
    # of the directory name matches an entry in uniquenames
    for root, dirs, files in walk(port_dbdir):
        if len(files) == 0 and len(dirs) == 0:
            # empty directory
            print(root)
        for name in files:
            if name == 'options':
                root_lastdir = split(root)[1]
                if not root_lastdir in uniquenames:
                    print('/'.join([root, name]))
                    if len(files) == 1 and len(dirs) == 0:
                        print(root)
             

if __name__ == "__main__":
	main()
