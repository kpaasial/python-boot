PKGNG = '/usr/local/sbin/pkg'

from pbutils.pbutils import my_popen

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


