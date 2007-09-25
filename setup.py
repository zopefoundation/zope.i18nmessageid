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

from setuptools import setup, find_packages, Extension

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(name='zope.i18nmessageid',
    version = '3.4.2',
    author='Zope Corporation and Contributors',
    author_email='zope3-dev@zope.org',
    description='Zope 3 i18n Message Identifier',
    long_description=(
        read('README.txt')
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
    url='http://svn.zope.org/zope.i18nmessageid',
    packages=find_packages('src'),
    package_dir = {'': 'src'},

    ext_modules=[Extension("zope.i18nmessageid._zope_i18nmessageid_message",
                           [os.path.join('src', 'zope', 'i18nmessageid',
                                         "_zope_i18nmessageid_message.c")
                            ]),
                 ],
    namespace_packages=['zope',],
    tests_require = ['zope.testing'],
    install_requires=['setuptools'],
    include_package_data = True,
    zip_safe = False,
    )
