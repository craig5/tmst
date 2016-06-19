#!/usr/bin/env python
"""Setup script for sample package (python3)."""


import distutils.core
import glob
import os
import setuptools
import sys


_NAME = 'tmst'
_PYTHON_PKG_NAME = 'tmst'
_PKG_VERSION = '0.0.1'
_PKG_DESCRIPTION = 'Coming soon...'
_PKG_AUTHOR_NAME = 'Craig Sebenik'
_PKG_AUTHOR_EMAIL = 'craig5@users.noreply.github.com'
_PKG_URL = 'http://www.friedserver.com/'
_PKG_KEYWORDS = ['todo']
#
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_LIB_DIR = 'lib'
_DATA_DIR = 'data'
_DATA_LIST = ['{0}/*'.format(_DATA_DIR)]
_ENTRY_POINTS = {
    'console_scripts': [
        'tmst = tmst.scripts:cli'
    ]
}


setuptools.setup(
    name=_NAME,
    version=_PKG_VERSION,
    description=_PKG_DESCRIPTION,
    author=_PKG_AUTHOR_NAME,
    author_email=_PKG_AUTHOR_EMAIL,
    package_dir={'': _LIB_DIR},
    packages=[_PYTHON_PKG_NAME],
    package_data={'': _DATA_LIST},
    entry_points=_ENTRY_POINTS,
    url=_PKG_URL,
    keywords=_PKG_KEYWORDS,
)

# End of file.
