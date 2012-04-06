##############################################################################
#
# Copyright (c) 2003 Zope Foundation and Contributors.
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
"""Message ID tests.
"""
import unittest

class PyMessageTests(unittest.TestCase):

    _TEST_REAOONLY = True

    def _getTargetClass(self):
        from zope.i18nmessageid.message import pyMessage
        return pyMessage

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_defaults(self):
        message = self._makeOne('testing')
        self.assertEqual(message, 'testing')
        self.assertEqual(message.domain, None)
        self.assertEqual(message.default, None)
        self.assertEqual(message.mapping, None)
        if self._TEST_REAOONLY:
            self.assertTrue(message._readonly)

    def test_ctor_explicit(self):
        mapping = {'key': 'value'}
        message = self._makeOne('testing', 'domain', 'default', mapping)
        self.assertEqual(message, 'testing')
        self.assertEqual(message.domain, 'domain')
        self.assertEqual(message.default, 'default')
        self.assertEqual(message.mapping, mapping)
        if self._TEST_REAOONLY:
            self.assertTrue(message._readonly)

    def test_ctor_copy(self):
        mapping = {'key': 'value'}
        source = self._makeOne('testing', 'domain', 'default', mapping)
        message = self._makeOne(source)
        self.assertEqual(message, 'testing')
        self.assertEqual(message.domain, 'domain')
        self.assertEqual(message.default, 'default')
        self.assertEqual(message.mapping, mapping)
        if self._TEST_REAOONLY:
            self.assertTrue(message._readonly)

    def test_ctor_copy_w_overrides(self):
        mapping = {'key': 'value'}
        source = self._makeOne('testing')
        message = self._makeOne(source, 'domain', 'default', mapping)
        self.assertEqual(message, 'testing')
        self.assertEqual(message.domain, 'domain')
        self.assertEqual(message.default, 'default')
        self.assertEqual(message.mapping, mapping)
        if self._TEST_REAOONLY:
            self.assertTrue(message._readonly)

    def test_domain_immutable(self):
        message = self._makeOne('testing')
        def _try():
            message.domain = 'domain'
        self.assertRaises(TypeError, _try)

    def test_default_immutable(self):
        message = self._makeOne('testing')
        def _try():
            message.default = 'default'
        self.assertRaises(TypeError, _try)

    def test_mapping_immutable(self):
        mapping = {'key': 'value'}
        message = self._makeOne('testing')
        def _try():
            message.mapping = mapping
        self.assertRaises(TypeError, _try)

    def test_unknown_immutable(self):
        message = self._makeOne('testing')
        def _try():
            message.unknown = 'unknown'
        self.assertRaises(TypeError, _try)

    def test___getstate__(self):
        mapping = {'key': 'value'}
        source = self._makeOne('testing')
        message = self._makeOne(source, 'domain', 'default', mapping)
        state = message.__getstate__()
        self.assertEqual(state, ('testing', 'domain', 'default', mapping))

    def test___reduce__(self):
        mapping = {'key': 'value'}
        source = self._makeOne('testing')
        message = self._makeOne(source, 'domain', 'default', mapping)
        klass, state = message.__reduce__()
        self.assertTrue(klass is self._getTargetClass())
        self.assertEqual(state, ('testing', 'domain', 'default', mapping))

class MessageTests(PyMessageTests):

    _TEST_REAOONLY = False

    def _getTargetClass(self):
        from zope.i18nmessageid.message import Message
        return Message


class Functional(unittest.TestCase):

    def test_message_pickling(self):
        from zope.i18nmessageid.message import pyMessage as Message
        robot = Message(u"robot-message", 'futurama', u"${name} is a robot.")

        self.assertEqual(robot, u'robot-message')
        self.assertTrue(isinstance(robot, unicode))
        self.assertEqual(robot.default, u'${name} is a robot.')
        self.assertEqual(robot.mapping, None)

        # Only the python implementation has a _readonly attribute
        self.assertEqual(robot._readonly, True)
        self.assertRaises(
            TypeError,
            robot.__setattr__, 'domain', "planetexpress")
        self.assertRaises(
            TypeError,
            robot.__setattr__, 'default', u"${name} is not a robot.")
        self.assertRaises(
            TypeError,
            robot.__setattr__, 'mapping', {u'name': u'Bender'})
        
        new_robot = Message(robot, mapping={u'name': u'Bender'})
        self.assertEqual(new_robot, u'robot-message')
        self.assertEqual(new_robot.domain, 'futurama')
        self.assertEqual(new_robot.default, u'${name} is a robot.')
        self.assertEqual(new_robot.mapping, {u'name': u'Bender'})

        callable, args = new_robot.__reduce__()
        self.assertTrue(callable is Message)
        self.assertEqual(
            args,
            (u'robot-message', 'futurama', u'${name} is a robot.',
             {u'name': u'Bender'}))

        fembot = Message(u'fembot')
        callable, args = fembot.__reduce__()
        self.assertTrue(callable is Message)
        self.assertEqual(args, (u'fembot', None, None, None))

        import zope.i18nmessageid.message
        zope.i18nmessageid.message.Message = Message

        # First check if pickling and unpickling from pyMessage to
        # pyMessage works
        from pickle import dumps, loads
        pystate = dumps(new_robot)
        pickle_bot = loads(pystate)
        self.assertEqual(pickle_bot, u'robot-message')
        self.assertEqual(pickle_bot.domain, 'futurama')
        self.assertEqual(pickle_bot.default, u'${name} is a robot.')
        self.assertEqual(pickle_bot.mapping, {u'name': u'Bender'})
        self.assertEqual(pickle_bot._readonly, True)

        from zope.i18nmessageid.message import pyMessage
        self.assertTrue(pickle_bot.__reduce__()[0] is pyMessage)
        del pickle_bot

        # Second check if cMessage is able to load the state of a pyMessage
        try:
            from zope.i18nmessageid._zope_i18nmessageid_message import Message
        except ImportError:
            return
        from zope.i18nmessageid._zope_i18nmessageid_message import (
                                                        Message as cMessage)
        zope.i18nmessageid.message.Message = Message
        c_bot = loads(pystate) 
        self.assertEqual(c_bot, u'robot-message')
        self.assertEqual(c_bot.domain, 'futurama')
        self.assertEqual(c_bot.default, u'${name} is a robot.')
        self.assertEqual(c_bot.mapping, {u'name': u'Bender'})
        self.assertFalse(hasattr(c_bot, '_readonly'))
        self.assertTrue(c_bot.__reduce__()[0] is cMessage)

        # Last check if pyMessage can load a state of cMessage
        cstate = dumps(c_bot)
        del c_bot
        from zope.i18nmessageid.message import pyMessage as Message
        zope.i18nmessageid.message.Message = Message
        py_bot = loads(cstate)
        self.assertEqual(py_bot, u'robot-message')
        self.assertEqual(py_bot.domain, 'futurama')
        self.assertEqual(py_bot.default, u'${name} is a robot.')
        self.assertEqual(py_bot.mapping, {u'name': u'Bender'})
        self.assertEqual(py_bot._readonly, True)
        self.assertTrue(py_bot.__reduce__()[0] is pyMessage)

        # Both pickle states should be equal
        self.assertEqual(pystate, cstate)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(PyMessageTests),
    ))
