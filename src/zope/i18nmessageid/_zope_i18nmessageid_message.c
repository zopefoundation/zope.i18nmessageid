/*############################################################################
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
############################################################################*/

#include "Python.h"
#include "structmember.h"

static int is_message(PyTypeObject* type, PyObject* obj);  /* forward ref */

/*
 *  Message type subclasses str
 */

typedef struct
{
    PyUnicodeObject base;
    PyObject* domain;
    PyObject* default_;
    PyObject* mapping;
    PyObject* value_plural;
    PyObject* default_plural;
    PyObject* number;
} Message;

/*
 *  Message type slot handlers
 */

static int
Message_traverse(PyObject* pyobj_self, visitproc visit, void* arg)
{
    PyTypeObject* tp = Py_TYPE(pyobj_self);
    Py_VISIT(tp);
    Message* self = (Message*)pyobj_self;
    Py_VISIT(self->domain);
    Py_VISIT(self->default_);
    Py_VISIT(self->mapping);
    Py_VISIT(self->value_plural);
    Py_VISIT(self->default_plural);
    Py_VISIT(self->number);
    return 0;
}

static int
Message_clear(PyObject* pyobj_self)
{
    Message* self = (Message*)pyobj_self;
    Py_CLEAR(self->domain);
    Py_CLEAR(self->default_);
    Py_CLEAR(self->mapping);
    Py_CLEAR(self->value_plural);
    Py_CLEAR(self->default_plural);
    Py_CLEAR(self->number);
    return 0;
}

static void
Message_dealloc(PyObject* self)
{
    PyTypeObject* tp = Py_TYPE(self);
    PyObject_GC_UnTrack(self);
    Message_clear(self);
    PyUnicode_Type.tp_dealloc((PyObject*)self);
    Py_DECREF(tp);
}

static PyObject*
Message_new(PyTypeObject* type, PyObject* args, PyObject* kwds)
{
    PyObject *value;
    PyObject *domain = NULL;
    PyObject *default_ = NULL;
    PyObject *mapping = NULL;
    PyObject *value_plural = NULL;
    PyObject *default_plural = NULL;
    PyObject *number = NULL;

    static char* kwlist[] = {
        "value", "domain", "default", "mapping",
        "msgid_plural", "default_plural", "number", NULL
    };

    PyObject *new_args;
    PyObject *new_str;
    Message  *new_msg;
    Message  *other = NULL;

    if (!PyArg_ParseTupleAndKeywords(
        args, kwds, "O|OOOOOO", kwlist,
        &value, &domain, &default_, &mapping,
        &value_plural, &default_plural, &number)
    ) { return NULL; }

    if (number != NULL && Py_None != number) {
        if (!(PyLong_Check(number) || PyFloat_Check(number))) {
            PyErr_SetString(PyExc_TypeError,
                            "`number` should be an integer or a float");
            return NULL;
        }
    }

    new_args = Py_BuildValue("(O)", value);
    if (new_args == NULL) { return NULL; }

    new_str = PyUnicode_Type.tp_new(type, new_args, NULL);
    Py_DECREF(new_args);
    if (new_str == NULL) { return NULL; }

    if (!is_message(type, new_str)) {
        PyErr_SetString(PyExc_TypeError,
                        "unicode.__new__ didn't return a Message");
        Py_DECREF(new_str);
        return NULL;
    }

    new_msg = (Message*)new_str;

    if (is_message(type, value)) {
        /* value is a Message so we copy it and use it as base */
        other = (Message*)value;
        new_msg->domain = other->domain;
        new_msg->default_ = other->default_;
        new_msg->mapping = other->mapping;
        new_msg->value_plural = other->value_plural;
        new_msg->default_plural = other->default_plural;
        new_msg->number = other->number;
    } else {
        new_msg->domain = NULL;
        new_msg->default_ = NULL;
        new_msg->mapping = NULL;
        new_msg->value_plural = NULL;
        new_msg->default_plural = NULL;
        new_msg->number = NULL;
    }

    if (domain != NULL) {
        new_msg->domain = domain;
    }

    if (default_ != NULL) {
        new_msg->default_ = default_;
    }

    if (mapping == Py_None) {
        new_msg->mapping = Py_None;
        Py_INCREF(Py_None);
    } else if (mapping != NULL) {
        /* Ensure that our mapping is immutable */
        new_msg->mapping = PyDictProxy_New(mapping);
    } else if (other != NULL && new_msg->mapping == other->mapping) {
        /* borrowed? */
        Py_XINCREF(new_msg->mapping);
    }

    if (value_plural != NULL) {
        new_msg->value_plural = value_plural;
    }

    if (default_plural != NULL) {
        new_msg->default_plural = default_plural;
    }

    if (number != NULL) {
        new_msg->number = number;
    }

    /* Don't:  Py_XINCREF(new_msg->mapping); we handed it above */
    Py_XINCREF(new_msg->default_);
    Py_XINCREF(new_msg->domain);
    Py_XINCREF(new_msg->value_plural);
    Py_XINCREF(new_msg->default_plural);
    Py_XINCREF(new_msg->number);

    return (PyObject*)new_msg;
}

/*
 * Message type methods
 */

static char Message_reduce__doc__[] = (
    "Reduce messages to a serializable form\n\n"
    "Notably, for use in pickling."
);

static PyObject*
Message_reduce(Message* self)
{
    PyObject *value;
    PyObject *mapping;
    PyObject *result;

    value = PyObject_CallFunctionObjArgs(
        (PyObject*)&PyUnicode_Type, self, NULL);
    if (value == NULL) { return NULL;}

    if (self->mapping == NULL) {
        mapping = Py_None; /* borrowed: Py_BuildValue will incref */
    } else if (self->mapping == Py_None) {
        mapping = Py_None; /* borrowed: Py_BuildValue will incref */
    } else {
        mapping = PyObject_CallFunctionObjArgs(
          (PyObject*)&PyDict_Type, self->mapping, NULL);
        if (mapping == NULL) { return NULL; }
    }

    result = Py_BuildValue(
        "(O(OOOOOOO))",
        Py_TYPE(&(self->base)),
        value,
        self->domain ? self->domain : Py_None,
        self->default_ ? self->default_ : Py_None,
        mapping,
        self->value_plural ? self->value_plural : Py_None,
        self->default_plural ? self->default_plural : Py_None,
        self->number ? self->number : Py_None
    );

    if (mapping != Py_None) {
        Py_DECREF(mapping);
    }
    Py_DECREF(value);

    return result;
}

/*
 *  Message type declaration structures
 */

static PyMemberDef Message_members[] = {
    { "domain", T_OBJECT, offsetof(Message, domain), READONLY },
    { "default", T_OBJECT, offsetof(Message, default_), READONLY },
    { "mapping", T_OBJECT, offsetof(Message, mapping), READONLY },
    { "msgid_plural", T_OBJECT, offsetof(Message, value_plural), READONLY },
    { "default_plural", T_OBJECT, offsetof(Message, default_plural), READONLY },
    { "number", T_OBJECT, offsetof(Message, number), READONLY },
    { NULL } /* Sentinel */
};

static PyMethodDef Message_methods[] = {
    { "__reduce__",
        (PyCFunction)Message_reduce, METH_NOARGS, Message_reduce__doc__ },
    { NULL } /* Sentinel */
};

static char Message__name__[] = "zope.i18nmessageid.message.Message";
static char Message__doc__[] =
  "Message\n"
  "\n"
  "This is a string used as a message.  It has a domain attribute that is\n"
  "its source domain, and a default attribute that is its default text to\n"
  "display when there is no translation.  domain may be None meaning there is\n"
  "no translation domain.  default may also be None, in which case the\n"
  "message id itself implicitly serves as the default text.\n";

/*
 *  Heap type: MessageType
 */
static PyType_Slot Message_type_slots[] = {
    {Py_tp_doc,         Message__doc__},
    {Py_tp_new,         Message_new},
    {Py_tp_dealloc,     Message_dealloc},
    {Py_tp_traverse,    Message_traverse},
    {Py_tp_clear,       Message_clear},
    {Py_tp_methods,     Message_methods},
    {Py_tp_members,     Message_members},
    {0,                 NULL}
};

static PyType_Spec Message_type_spec = {
    .name             = Message__name__,
    .basicsize        = sizeof(Message),
    .flags            = Py_TPFLAGS_DEFAULT |
                        Py_TPFLAGS_BASETYPE |
#if PY_VERSION_HEX >= 0x030a0000
                        Py_TPFLAGS_IMMUTABLETYPE |
#endif
                        Py_TPFLAGS_HAVE_GC,
    .slots            = Message_type_slots
};


/*
 *  Module initialization structures
 */

static char _zim__name__[]  = "_zope_i18nmessageid_message";
static char _zim__doc__[]   = "I18n Messages";

typedef struct {
    PyTypeObject*  message_type;
} _zim_module_state;

/*
 *  Macro to speed lookup of state members
 */
#define _zim_state(o) ((_zim_module_state*)PyModule_GetState(o))

/*
 * Utility: returns True if 'obj' is an instance of 'MessageType'.
 */
static int is_message(PyTypeObject* type, PyObject* obj)
{
    PyTypeObject* message_type;
    _zim_module_state* rec = (_zim_module_state*)PyType_GetModuleState(type);
    /* PT_GMS will already have set the exception */
    if (rec == NULL) { return 0; }

    message_type = rec->message_type;
    return PyObject_TypeCheck(obj, message_type);
}

static _zim_module_state*
_zim_state_init(PyObject* module)
{
    _zim_module_state* rec = _zim_state(module);
    rec->message_type = NULL;
    return rec;
}

static int
_zim_state_traverse(PyObject* module, visitproc visit, void* arg)
{
    _zim_module_state* rec = _zim_state(module);
    Py_VISIT(rec->message_type);
    return 0;
}

static int
_zim_state_clear(PyObject* module)
{
    _zim_module_state* rec = _zim_state(module);
    Py_CLEAR(rec->message_type);
    return 0;
}

static int
_zim_module_exec(PyObject* module)
{
    _zim_module_state* rec = _zim_state_init(module);

    /* Initialize / add types: */

    PyObject* message_bases;
    PyObject* message_type;

    message_bases = Py_BuildValue("(O)", (PyObject*)&PyUnicode_Type);
    if (message_bases == NULL) { return -1; }

    message_type = PyType_FromModuleAndSpec(
        module, &Message_type_spec, message_bases
    );
    Py_DECREF(message_bases);
    if (message_type == NULL) { return -1; }

    rec->message_type = (PyTypeObject*)message_type;

    if (PyModule_AddObject(module, "Message", message_type) < 0) {
        return -1;
    }

    Py_INCREF(message_type);  /* Recover stolen ref */

    return 0;
}

/*
 * Slot definitions for multi-phase initialization
 *
 * See: https://docs.python.org/3/c-api/module.html#multi-phase-initialization
 * and: https://peps.python.org/pep-0489
 */
static PyModuleDef_Slot _zim_module_slots[] = {
    {Py_mod_exec,       _zim_module_exec},
    {0,                 NULL}
};

static struct PyModuleDef _zim_module = {
    PyModuleDef_HEAD_INIT,
    .m_name     =_zim__name__,
    .m_doc      =_zim__doc__,
    .m_size     = sizeof(_zim_module_state),
    .m_traverse = _zim_state_traverse,
    .m_clear    = _zim_state_clear,
    .m_slots    = _zim_module_slots,
};

static PyObject*
init(void)
{
    return PyModuleDef_Init(&_zim_module);
}

PyMODINIT_FUNC
PyInit__zope_i18nmessageid_message(void)
{
    return init();
}
