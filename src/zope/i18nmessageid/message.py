##############################################################################
#
# Copyright (c) 2004 Zope Foundation and Contributors.
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
"""I18n Messages and factories.
"""
__docformat__ = "reStructuredText"
_marker = object()

import six


class Message(six.text_type):
    """Message (Python implementation)

    This is a string used as a message.  It has a domain attribute that is
    its source domain, and a default attribute that is its default text to
    display when there is no translation.  domain may be None meaning there is
    no translation domain.  default may also be None, in which case the
    message id itself implicitly serves as the default text.
    """

    __slots__ = (
        'domain', 'default', 'mapping', '_readonly',
        'msgid_plural', 'default_plural', 'number')

    def __new__(cls, ustr, domain=_marker, default=_marker, mapping=_marker,
                msgid_plural=_marker, default_plural=_marker, number=_marker):
        self = six.text_type.__new__(cls, ustr)
        if isinstance(ustr, self.__class__):
            domain = ustr.domain[:] if domain is _marker else domain
            default = ustr.default[:] if default is _marker else default
            mapping = ustr.mapping.copy() if mapping is _marker else mapping
            msgid_plural = (
                ustr.msgid_plural[:] if msgid_plural is _marker else
                msgid_plural)
            default_plural = (
                ustr.default_plural[:] if default_plural is _marker else
                default_plural)
            number = ustr.number if number is _marker else number
            ustr = six.text_type(ustr)
        else:
            domain = None if domain is _marker else domain
            default = None if default is _marker else default
            mapping = None if mapping is _marker else mapping
            msgid_plural = None if msgid_plural is _marker else msgid_plural
            default_plural = (None if default_plural is _marker else
                              default_plural)
            number = None if number is _marker else number

        self.domain = domain
        self.default = default
        self.mapping = mapping
        self.msgid_plural = msgid_plural
        self.default_plural = default_plural

        if number is not None and not isinstance(
                number, six.integer_types + (float,)):
            raise TypeError('`number` should be an integer or a float')

        self.number = number
        self._readonly = True
        return self

    def __setattr__(self, key, value):
        """Message is immutable

        It cannot be changed once the message id is created.
        """
        if getattr(self, '_readonly', False):
            raise TypeError('readonly attribute')
        else:
            return six.text_type.__setattr__(self, key, value)

    def __getstate__(self):
        return (
            six.text_type(self), self.domain, self.default, self.mapping,
            self.msgid_plural, self.default_plural, self.number)

    def __reduce__(self):
        return self.__class__, self.__getstate__()


# Name the fallback Python implementation to make it easier to test.
pyMessage = Message


try:
    from ._zope_i18nmessageid_message import Message
except ImportError:  # pragma: no cover
    pass


class MessageFactory(object):
    """Factory for creating i18n messages."""

    def __init__(self, domain):
        self._domain = domain

    def __call__(self, ustr, default=None, mapping=None,
                 msgid_plural=None, default_plural=None, number=None):
        return Message(ustr, self._domain, default, mapping,
                       msgid_plural, default_plural, number)
