#!/usr/bin/env python3.2

from distutils.core import setup


setup(name='Python Boot',
        version='1.0',
        description='Random python utilities',
        author='Kimmo Paasiala',
        author_email='kpaasial@gmail.com',
        url='https://github.com/kpaasial/python-boot',
        py_modules=['pbutils.portutils', 'pbutils.zfsutils'],
        scripts = ['scripts/distfilecleaner.py', 'scripts/portoptionscleaner.py']
)
    
