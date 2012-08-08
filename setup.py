#!/usr/bin/env python

from distutils.core import setup


setup(name='Python Boot',
        version='1.0',
        description='Random python utilities',
        author='Kimmo Paasiala',
        author_email='kpaasial@gmail.com',
        url='https://github.com/kpaasial/python-boot',
        packages=['pb_utils'],
        package_dir = {'pb_utils': 'pb_utils'},
        scripts = ['ports/distfilecleaner.py', 'ports/portoptionscleaner.py']
)
    
