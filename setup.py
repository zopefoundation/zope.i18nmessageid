##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Setup for zope.i18nmessageid package

$Id$
"""

import os
import sys

from setuptools import setup, find_packages, Extension
from distutils.command.build_ext import build_ext
from distutils.errors import CCompilerError
from distutils.errors import DistutilsExecError
from distutils.errors import DistutilsPlatformError

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

class optional_build_ext(build_ext):
    """This class subclasses build_ext and allows
       the building of C extensions to fail.
    """
    def run(self):
        try:
            build_ext.run(self)
        
        except DistutilsPlatformError, e:
            self._unavailable(e)

    def build_extension(self, ext):
       try:
           build_ext.build_extension(self, ext)
        
       except (CCompilerError, DistutilsExecError), e:
           self._unavailable(e)

    def _unavailable(self, e):
        print >> sys.stderr, '*' * 80
        print >> sys.stderr, """WARNING:

        An optional code optimization (C extension) could not be compiled.

        Optimizations for this package will not be available!"""
        print >> sys.stderr
        print >> sys.stderr, e
        print >> sys.stderr, '*' * 80


setup(name='zope.i18nmessageid',
    version = '3.5.1dev',
    author='Zope Corporation and Contributors',
    author_email='zope-dev@zope.org',
    description='Message Identifiers for internationalization',
    long_description=(
        read('README.txt')
        + '\n\n.. contents::\n\n' +
        read('src', 'zope', 'i18nmessageid', 'messages.txt')
        + '\n\n' +
        read('CHANGES.txt')
        ),
    keywords = "zope3 i18n message factory",
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope3'],
    license='ZPL 2.1',
    url='http://pypi.python.org/pypi/zope.i18nmessageid',
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    ext_modules=[
        Extension("zope.i18nmessageid._zope_i18nmessageid_message",
                  [os.path.join('src', 'zope', 'i18nmessageid',
                                "_zope_i18nmessageid_message.c") ]),
        ],
    namespace_packages=['zope',],
    tests_require = ['zope.testing'],
    install_requires=['setuptools'],
    include_package_data = True,
    zip_safe = False,
    cmdclass = {'build_ext':optional_build_ext},
    )

