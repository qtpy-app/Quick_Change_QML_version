# -*- coding: utf-8 -*-

# Copyright (c) 2017 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Parse a ProtoBuf protocol file and retrieve messages, enums, services and
rpc methods.

It is based on the Python class browser found in this package.
"""

from __future__ import unicode_literals

import re

import Utilities
import Utilities.ClassBrowsers as ClassBrowsers
from . import ClbrBaseClasses

SUPPORTED_TYPES = [ClassBrowsers.PROTO_SOURCE]
    
_getnext = re.compile(
    r"""
    (?P<String>
        " [^"\\\n]* (?: \\. [^"\\\n]*)* "
    )

|   (?P<Comment>
        ^ [ \t]* // .*? $
    |
        ^ [ \t]* /\* .*? \*/
    )

|   (?P<Message>
        ^
        (?P<MessageIndent> [ \t]* )
        message [ \t]+
        (?P<MessageName> [a-zA-Z_] [a-zA-Z0-9_]* )
        [ \t]* {
    )

|   (?P<Enum>
        ^
        (?P<EnumIndent> [ \t]* )
        enum [ \t]+
        (?P<EnumName> [a-zA-Z_] [a-zA-Z0-9_]* )
        [ \t]* {
    )

|   (?P<Service>
        ^
        (?P<ServiceIndent> [ \t]* )
        service [ \t]+
        (?P<ServiceName> [a-zA-Z_] [a-zA-Z0-9_]* )
        [ \t]* {
    )

|   (?P<Method>
        ^
        (?P<MethodIndent> [ \t]* )
        rpc [ \t]+
        (?P<MethodName> [a-zA-Z_] [a-zA-Z0-9_]* )
        [ \t]*
        \(
        (?P<MethodSignature> [^)]+? )
        \)
        [ \t]+
        returns
        [ \t]*
        \(
        (?P<MethodReturn> [^)]+? )
        \)
        [ \t]*
    )

|   (?P<Begin>
        [ \t]* {
    )

|   (?P<End>
        [ \t]* } [ \t]* ;?
    )""",
    re.VERBOSE | re.DOTALL | re.MULTILINE).search

# function to replace comments
_commentsub = re.compile(r"""//[^\n]*\n|//[^\n]*$""").sub
# function to normalize whitespace
_normalize = re.compile(r"""[ \t]{2,}""").sub

_modules = {}                           # cache of modules we've seen


class VisibilityMixin(ClbrBaseClasses.ClbrVisibilityMixinBase):
    """
    Mixin class implementing the notion of visibility.
    """
    def __init__(self):
        """
        Constructor
        """
        self.setPublic()


class Message(ClbrBaseClasses.Module, VisibilityMixin):
    """
    Class to represent a ProtoBuf Message.
    """
    def __init__(self, module, name, file, lineno):
        """
        Constructor
        
        @param module name of the module containing this message
        @type str
        @param name name of this message
        @type str
        @param file filename containing this message
        @type str
        @param lineno linenumber of the message definition
        @type int
        """
        ClbrBaseClasses.Module.__init__(self, module, name, file, lineno)
        VisibilityMixin.__init__(self)


class Enum(ClbrBaseClasses.Enum, VisibilityMixin):
    """
    Class to represent a ProtoBuf Enum.
    """
    def __init__(self, module, name, file, lineno):
        """
        Constructor
        
        @param module name of the module containing this enum
        @type str
        @param name name of this enum
        @type str
        @param file filename containing this enum
        @type str
        @param lineno linenumber of the message enum
        @type int
        """
        ClbrBaseClasses.Enum.__init__(self, module, name, file, lineno)
        VisibilityMixin.__init__(self)


class Service(ClbrBaseClasses.Class, VisibilityMixin):
    """
    Class to represent a ProtoBuf Service.
    """
    def __init__(self, module, name, file, lineno):
        """
        Constructor
        
        @param module name of the module containing this service
        @type str
        @param name name of this service
        @type str
        @param file filename containing this service
        @type str
        @param lineno linenumber of the service definition
        @type int
        """
        ClbrBaseClasses.Class.__init__(self, module, name, None, file,
                                       lineno)
        VisibilityMixin.__init__(self)


class ServiceMethod(ClbrBaseClasses.Function, VisibilityMixin):
    """
    Class to represent a ProtoBuf Service Method.
    """
    def __init__(self, name, file, lineno, signature, returns):
        """
        Constructor
        
        @param name name of this service method
        @type str
        @param file filename containing this service method
        @type str
        @param lineno linenumber of the service method definition
        @type int
        @param signature parameter list of the service method
        @type str
        @param returns return type of the service method
        @type str
        """
        ClbrBaseClasses.Function.__init__(self, None, name, file, lineno,
                                          signature,
                                          annotation="-> {0}".format(returns))
        VisibilityMixin.__init__(self)


def readmodule_ex(module, path=None):
    """
    Read a ProtoBuf protocol file and return a dictionary of messages, enums,
    services and rpc methods.

    @param module name of the ProtoBuf protocol file
    @type str
    @param path path the file should be searched in
    @type list of str
    @return the resulting dictionary
    @rtype dict
    """
    global _modules
    
    dictionary = {}

    if module in _modules:
        # we've seen this file before...
        return _modules[module]

    # search the path for the file
    f = None
    fullpath = [] if path is None else path[:]
    f, file, (suff, mode, type) = ClassBrowsers.find_module(module, fullpath)
    if f:
        f.close()
    if type not in SUPPORTED_TYPES:
        # not ProtoBuf protocol source, can't do anything with this module
        _modules[module] = dictionary
        return dictionary

    _modules[module] = dictionary
    classstack = []  # stack of (class, indent) pairs
    indent = 0
    try:
        src = Utilities.readEncodedFile(file)[0]
    except (UnicodeError, IOError):
        # can't do anything with this module
        _modules[module] = dictionary
        return dictionary

    lineno, last_lineno_pos = 1, 0
    lastGlobalEntry = None
    cur_obj = None
    i = 0
    while True:
        m = _getnext(src, i)
        if not m:
            break
        start, i = m.span()

        if m.start("Method") >= 0:
            # found a method definition or function
            thisindent = indent
            meth_name = m.group("MethodName")
            meth_sig = m.group("MethodSignature")
            meth_sig = meth_sig and meth_sig.replace('\\\n', '') or ''
            meth_sig = _commentsub('', meth_sig)
            meth_sig = _normalize(' ', meth_sig)
            meth_return = m.group("MethodReturn")
            meth_return = meth_return and meth_return.replace('\\\n', '') or ''
            meth_return = _commentsub('', meth_return)
            meth_return = _normalize(' ', meth_return)
            lineno = lineno + src.count('\n', last_lineno_pos, start)
            last_lineno_pos = start
            # close all interfaces/modules indented at least as much
            while classstack and \
                    classstack[-1][1] >= thisindent:
                if classstack[-1][0] is not None:
                    # record the end line
                    classstack[-1][0].setEndLine(lineno - 1)
                del classstack[-1]
            if classstack:
                # it's an interface/module method
                cur_class = classstack[-1][0]
                if isinstance(cur_class, Service):
                    # it's a method
                    f = ServiceMethod(meth_name, file, lineno, meth_sig,
                                      meth_return)
                    cur_class._addmethod(meth_name, f)
                # else it's a nested def
                else:
                    f = None
            else:
                # the file is incorrect, ignore the entry
                continue
            if not classstack:
                if lastGlobalEntry:
                    lastGlobalEntry.setEndLine(lineno - 1)
                lastGlobalEntry = f
            if cur_obj and isinstance(cur_obj, ServiceMethod):
                cur_obj.setEndLine(lineno - 1)
            cur_obj = f
            classstack.append((f, thisindent))  # Marker for nested fns

        elif m.start("String") >= 0:
            pass

        elif m.start("Comment") >= 0:
            pass

        elif m.start("Message") >= 0:
            # we found a message definition
            thisindent = indent
            indent += 1
            # close all messages/services indented at least as much
            while classstack and \
                    classstack[-1][1] >= thisindent:
                if classstack[-1][0] is not None:
                    # record the end line
                    classstack[-1][0].setEndLine(lineno - 1)
                del classstack[-1]
            lineno = lineno + src.count('\n', last_lineno_pos, start)
            last_lineno_pos = start
            message_name = m.group("MessageName")
            # remember this message
            cur_class = Message(module, message_name, file, lineno)
            if not classstack:
                dictionary[message_name] = cur_class
            else:
                msg = classstack[-1][0]
                msg._addclass(message_name, cur_class)
            if not classstack:
                if lastGlobalEntry:
                    lastGlobalEntry.setEndLine(lineno - 1)
                lastGlobalEntry = cur_class
            cur_obj = cur_class
            classstack.append((cur_class, thisindent))

        elif m.start("Enum") >= 0:
            # we found a message definition
            thisindent = indent
            indent += 1
            # close all messages/services indented at least as much
            while classstack and \
                    classstack[-1][1] >= thisindent:
                if classstack[-1][0] is not None:
                    # record the end line
                    classstack[-1][0].setEndLine(lineno - 1)
                del classstack[-1]
            lineno = lineno + src.count('\n', last_lineno_pos, start)
            last_lineno_pos = start
            enum_name = m.group("EnumName")
            # remember this Enum
            cur_class = Enum(module, enum_name, file, lineno)
            if not classstack:
                dictionary[enum_name] = cur_class
            else:
                enum = classstack[-1][0]
                enum._addclass(enum_name, cur_class)
            if not classstack:
                if lastGlobalEntry:
                    lastGlobalEntry.setEndLine(lineno - 1)
                lastGlobalEntry = cur_class
            cur_obj = cur_class
            classstack.append((cur_class, thisindent))

        elif m.start("Service") >= 0:
            # we found a message definition
            thisindent = indent
            indent += 1
            # close all messages/services indented at least as much
            while classstack and \
                    classstack[-1][1] >= thisindent:
                if classstack[-1][0] is not None:
                    # record the end line
                    classstack[-1][0].setEndLine(lineno - 1)
                del classstack[-1]
            lineno = lineno + src.count('\n', last_lineno_pos, start)
            last_lineno_pos = start
            service_name = m.group("ServiceName")
            # remember this Service
            cur_class = Service(module, service_name, file, lineno)
            if not classstack:
                dictionary[service_name] = cur_class
            else:
                service = classstack[-1][0]
                service._addclass(service_name, cur_class)
            if not classstack:
                if lastGlobalEntry:
                    lastGlobalEntry.setEndLine(lineno - 1)
                lastGlobalEntry = cur_class
            cur_obj = cur_class
            classstack.append((cur_class, thisindent))

        elif m.start("Begin") >= 0:
            # a begin of a block we are not interested in
            indent += 1

        elif m.start("End") >= 0:
            # an end of a block
            indent -= 1

        else:
            assert 0, "regexp _getnext found something unexpected"

    return dictionary
