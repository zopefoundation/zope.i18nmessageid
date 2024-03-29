``zope.i18nmessageid``
======================

.. image:: https://img.shields.io/pypi/v/zope.i18nmessageid.svg
    :target: https://pypi.python.org/pypi/zope.i18nmessageid/
    :alt: Latest Version

.. image:: https://github.com/zopefoundation/zope.i18nmessageid/actions/workflows/tests.yml/badge.svg
        :target: https://github.com/zopefoundation/zope.i18nmessageid/actions/workflows/tests.yml
        
.. image:: https://readthedocs.org/projects/zopei18nmessageid/badge/?version=latest
        :target: http://zopei18nmessageid.readthedocs.org/en/latest/
        :alt: Documentation Status

To translate any text, we must be able to discover the source domain
of the text.  A source domain is an identifier that identifies a
project that produces program source strings.  Source strings occur as
literals in python programs, text in templates, and some text in XML
data.  The project implies a source language and an application
context.

We can think of a source domain as a collection of messages and
associated translation strings.

We often need to create unicode strings that will be displayed by
separate views.  The view cannot translate the string without knowing
its source domain.  A string or unicode literal carries no domain
information, therefore we use messages.  Messages are unicode strings
which carry a translation source domain and possibly a default
translation.  They are created by a message factory. The message
factory is created by calling ``MessageFactory`` with the source
domain.

This package provides facilities for *declaring* such messages within
program source text;  translation of the messages is the responsiblitiy
of the 'zope.i18n' package.

Please see http://zopei18nmessageid.readthedocs.org/en/latest/ for the documentation.
