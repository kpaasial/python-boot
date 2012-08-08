PKGNG = '/usr/local/sbin/pkg'


def my_popen(*cmdLine, returnOutput=True):
    if returnOutput is True:
        stdOutFile = os.PIPE
    else:
        stdOutFile = None

    try:
        p = os.Popen(*cmdLine, stdout=stdOutFile)
    except OSError as err:
        print (err, file=sys.stderr)
        return

    if returnOutput is True:
        output = p.communicate()[0]
        # TODO: Check for errors, check that different locale does
        #         # not affect what we get as output             
        decodedOutput = output.decode()
        return decodedOutput



def get_make_variable(variable, directory=''):
    cmdLine = ['/usr/bin/make']
    if directory != '':
        cmdLine.append('-C')
        cmdLine.append(directory)
    cmdLine.append('-V')
    cmdLine.append(variable)

    return my_popen(cmdLine).rstrip('\n')


# Returns a list of installed packages, for each package
# the origin (port directory relative to PORTSDIR) of the
# package is returned.
# TODO Add options for origin etc.
def get_installed_packages():
	cmdLine = [PKGNG]
	cmdLine.append('info')
	cmdLine.append('-qao')

	installedPackages = my_popen(cmdLine)

	return installedPackages.splitlines()


# Get the SHA256 secure hash for a file
def get_file_sha256(file):

    chunk_size = 1048576
    file_sha256_checksum = hashlib.sha256()


    with open(file, "rb") as f:
        byte = f.read(chunk_size)
        while byte:
            file_sha256_checksum.update(byte)
            byte = f.read(chunk_size)

    return file_sha256_checksum.hexdigest()



# Return the size of a file in bytes
def get_file_size(file):
    # use os.stat() to figure out the size
    statinfo = os.stat(file)

    return str(statinfo.st_size)

