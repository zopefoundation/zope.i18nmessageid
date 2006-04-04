zope.i18nmessageid Package Readme
=================================

Overview
--------

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

This package provides facilities for *delaring* such messages within
program source text;  translation of the messages is the responsiblitiy
of the 'zope.i18n' package.

Changes
-------

See CHANGES.txt.

Installation
------------

See INSTALL.txt.


Developer Resources
-------------------

- Subversion browser:

  http://svn.zope.org/zope.i18nmessageid/

- Read-only Subversion checkout:

  $ svn co svn://svn.zope.org/repos/main/zope.i18nmessageid/trunk

- Writable Subversion checkout:

  $ svn co svn://svn.zope.org/repos/main/zope.i18nmessageid/trunk

- Note that the 'src/zope/i18nmessageid' package is acutally a
  'svn:externals' link to the corresponding package in the Zope3 trunk
  (or to a specific tag, for released versions of the package).
