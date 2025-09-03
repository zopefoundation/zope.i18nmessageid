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


tests_require = [
    'zope.testrunner >= 6.4',
    'coverage',
]


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as stream:
        return stream.read()


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


setup(
    name='zope.i18nmessageid',
    version='8.0.dev0',
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.dev',
    description='Message Identifiers for internationalization',
    long_description=(
        read('README.rst')
        + '\n\n' +
        read('CHANGES.rst')
    ),
    keywords="zope i18n message factory",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope :: 3',
    ],
    license='ZPL-2.1',
    url='https://github.com/zopefoundation/zope.i18nmessageid',
    # we need the following two parameters because we compile C code,
    # otherwise only the shared library is installed:
    package_dir={'': 'src'},
    packages=['zope.i18nmessageid'],
    install_requires=['setuptools'],
    python_requires='>=3.9',
    include_package_data=True,
    zip_safe=False,
    cmdclass={'build_ext': optional_build_ext},
    ext_modules=ext_modules,
    extras_require={
        'testing': tests_require,
        'test': tests_require,
        'docs': ['Sphinx', 'sphinx_rtd_theme'],
    },
)
