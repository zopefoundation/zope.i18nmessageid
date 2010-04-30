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

$Id$
"""

import os

from setuptools import setup, find_packages, Extension, Feature

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

codeoptimization = Feature("Optional code optimizations",
    standard=True,
    ext_modules=[
        Extension("zope.i18nmessageid._zope_i18nmessageid_message", [
            os.path.join('src', 'zope', 'i18nmessageid',
                "_zope_i18nmessageid_message.c")
        ]),
    ],
)

setup(name='zope.i18nmessageid',
    version = '3.5.2dev',
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.org',
    description='Message Identifiers for internationalization',
    long_description=(
        read('README.txt')
        + '\n\n.. contents::\n\n' +
        read('src', 'zope', 'i18nmessageid', 'messages.txt')
        + '\n\n' +
        read('CHANGES.txt')
        ),
    keywords = "zope i18n message factory",
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
    features = {'codeoptimization': codeoptimization},
    namespace_packages=['zope',],
    install_requires=['setuptools'],
    include_package_data = True,
    zip_safe = False,
)
