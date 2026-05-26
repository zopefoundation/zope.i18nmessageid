##############################################################################
#
# Copyright (c) 2006 Zope Foundation and Contributors.
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
# This package is developed by the Zope Toolkit project, documented here:
# http://docs.zope.org/zopetoolkit
# When developing and releasing this package, please follow the documented
# Zope Toolkit policies as described by this documentation.
##############################################################################
"""Setup for zope.i18nmessageid package
"""

import os
import platform
import sys

from setuptools import Extension
from setuptools import setup


# isort: off
# See https://github.com/zopefoundation/zope.i18nmessageid/issues/61

from distutils.command.build_ext import build_ext
from distutils.errors import CCompilerError
from distutils.errors import DistutilsExecError
from distutils.errors import DistutilsPlatformError

# isort: on

py_impl = getattr(platform, 'python_implementation', lambda: None)
is_pypy = py_impl() == 'PyPy'
is_jython = 'java' in sys.platform

codeoptimization_c = os.path.join('src', 'zope', 'i18nmessageid',
                                  "_zope_i18nmessageid_message.c")
codeoptimization = [
    Extension(
        "zope.i18nmessageid._zope_i18nmessageid_message",
        [os.path.normcase(codeoptimization_c)]
    ),
]

ext_modules = []
if not is_pypy and not is_jython:
    # Jython cannot build the C optimizations, while on PyPy they are
    # anti-optimizations (the C extension compatibility layer is known-slow,
    # and defeats JIT opportunities).
    ext_modules = codeoptimization


class optional_build_ext(build_ext):
    """This class subclasses build_ext and allows
       the building of C extensions to fail.
    """

    def run(self):
        try:
            build_ext.run(self)
        except DistutilsPlatformError as e:
            self._unavailable(e)

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except (CCompilerError, DistutilsExecError) as e:
            self._unavailable(e)

    def _unavailable(self, e):
        print('*' * 80, file=sys.stderr)
        print("""WARNING:

        An optional code optimization (C extension) could not be compiled.

        Optimizations for this package will not be available!

        """, file=sys.stderr)
        print(str(e), file=sys.stderr)
        print('*' * 80, file=sys.stderr)


setup(cmdclass={'build_ext': optional_build_ext},
      ext_modules=ext_modules)
