# -*- coding: utf-8 -*-

# Copyright (c) 2005 - 2017 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Parse a CORBA IDL file and retrieve modules, interfaces, methods and
attributes.

Parse enough of a CORBA IDL file to recognize module, interface and method
definitions and to find out the superclasses of an interface as well as its
attributes.

It is based on the Python class browser found in this package.
"""

from __future__ import unicode_literals

import re

import Utilities
import Utilities.ClassBrowsers as ClassBrowsers
from . import ClbrBaseClasses

SUPPORTED_TYPES = [ClassBrowsers.IDL_SOURCE]
    
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

|   (?P<Method>
        ^
        (?P<MethodIndent> [ \t]* )
        (?: oneway [ \t]+ )?
        (?: [a-zA-Z0-9_:]+ | void ) [ \t]*
        (?P<MethodName> [a-zA-Z_] [a-zA-Z0-9_]* )
        [ \t]*
        \(
        (?P<MethodSignature> [^)]*? )
        \);
        [ \t]*
    )

|   (?P<Interface>
        ^
        (?P<InterfaceIndent> [ \t]* )
        (?: abstract [ \t]+ )?
        interface [ \t]+
        (?P<InterfaceName> [a-zA-Z_] [a-zA-Z0-9_]* )
        [ \t]*
        (?P<InterfaceSupers> : [^{]+? )?
        [ \t]* {
    )

|   (?P<Module>
        ^
        (?P<ModuleIndent> [ \t]* )
        module [ \t]+
        (?P<ModuleName> [a-zA-Z_] [a-zA-Z0-9_]* )
        [ \t]* {
    )

|   (?P<Attribute>
        ^
        (?P<AttributeIndent> [ \t]* )
        (?P<AttributeReadonly> readonly [ \t]+ )?
        attribute [ \t]+
        (?P<AttributeType>  (?: [a-zA-Z0-9_:]+ [ \t]+ )+ )
        (?P<AttributeNames> [^;]* )
        ;
    )

|   (?P<Begin>
        [ \t]* {
    )

|   (?P<End>
        [ \t]* } [ \t]* ;
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


class Module(ClbrBaseClasses.Module, VisibilityMixin):
    """
    Class to represent a CORBA IDL module.
    """
    def __init__(self, module, name, file, lineno):
        """
        Constructor
        
        @param module name of the module containing this module
        @type str
        @param name name of this module
        @type str
        @param file filename containing this module
        @type str
        @param lineno line number of the module definition
        @type int
        """
        ClbrBaseClasses.Module.__init__(self, module, name, file, lineno)
        VisibilityMixin.__init__(self)


class Interface(ClbrBaseClasses.Class, VisibilityMixin):
    """
    Class to represent a CORBA IDL interface.
    """
    def __init__(self, module, name, superClasses, file, lineno):
        """
        Constructor
        
        @param module name of the module containing this interface
        @type str
        @param name name of this interface
        @type str
        @param superClasses list of interface names this interface is
            inherited from
        @type list of str
        @param file filename containing this interface
        @type str
        @param lineno line number of the interface definition
        @type int
        """
        ClbrBaseClasses.Class.__init__(self, module, name, superClasses, file,
                                       lineno)
        VisibilityMixin.__init__(self)


class Function(ClbrBaseClasses.Function, VisibilityMixin):
    """
    Class to represent a CORBA IDL function.
    """
    def __init__(self, module, name, file, lineno, signature='',
                 separator=','):
        """
        Constructor
        
        @param module name of the module containing this function
        @type str
        @param name name of this function
        @type str
        @param file filename containing this function
        @type str
        @param lineno line number of the function definition
        @type int
        @param signature parameter list of the function
        @type str
        @param separator string separating the parameters
        @type str
        """
        ClbrBaseClasses.Function.__init__(self, module, name, file, lineno,
                                          signature, separator)
        VisibilityMixin.__init__(self)


class Attribute(ClbrBaseClasses.Attribute, VisibilityMixin):
    """
    Class to represent a CORBA IDL attribute.
    """
    def __init__(self, module, name, file, lineno):
        """
        Constructor
        
        @param module name of the module containing this attribute
        @type str
        @param name name of this attribute
        @type str
        @param file filename containing this attribute
        @type str
        @param lineno line number of the attribute definition
        @type int
        """
        ClbrBaseClasses.Attribute.__init__(self, module, name, file, lineno)
        VisibilityMixin.__init__(self)


def readmodule_ex(module, path=None):
    """
    Read a CORBA IDL file and return a dictionary of classes, functions and
    modules.

    @param module name of the CORBA IDL file
    @type str
    @param path path the file should be searched in
    @type list of str
    @return the resulting dictionary
    @rtype dict
    """
    global _modules
    
    dictionary = {}
    dict_counts = {}

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
        # not CORBA IDL source, can't do anything with this module
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
                if isinstance(cur_class, Interface) or \
                        isinstance(cur_class, Module):
                    # it's a method
                    f = Function(None, meth_name,
                                 file, lineno, meth_sig)
                    cur_class._addmethod(meth_name, f)
                # else it's a nested def
                else:
                    f = None
            else:
                # it's a function
                f = Function(module, meth_name,
                             file, lineno, meth_sig)
                if meth_name in dict_counts:
                    dict_counts[meth_name] += 1
                    meth_name = "{0}_{1:d}".format(
                        meth_name, dict_counts[meth_name])
                else:
                    dict_counts[meth_name] = 0
                dictionary[meth_name] = f
            if not classstack:
                if lastGlobalEntry:
                    lastGlobalEntry.setEndLine(lineno - 1)
                lastGlobalEntry = f
            if cur_obj and isinstance(cur_obj, Function):
                cur_obj.setEndLine(lineno - 1)
            cur_obj = f
            classstack.append((f, thisindent))  # Marker for nested fns

        elif m.start("String") >= 0:
            pass

        elif m.start("Comment") >= 0:
            pass

        elif m.start("Interface") >= 0:
            # we found an interface definition
            thisindent = indent
            indent += 1
            # close all interfaces/modules indented at least as much
            while classstack and \
                    classstack[-1][1] >= thisindent:
                if classstack[-1][0] is not None:
                    # record the end line
                    classstack[-1][0].setEndLine(lineno - 1)
                del classstack[-1]
            lineno = lineno + src.count('\n', last_lineno_pos, start)
            last_lineno_pos = start
            class_name = m.group("InterfaceName")
            inherit = m.group("InterfaceSupers")
            if inherit:
                # the interface inherits from other interfaces
                inherit = inherit[1:].strip()
                inherit = [_commentsub('', inherit)]
            # remember this interface
            cur_class = Interface(module, class_name, inherit,
                                  file, lineno)
            if not classstack:
                dictionary[class_name] = cur_class
            else:
                cls = classstack[-1][0]
                cls._addclass(class_name, cur_class)
            if not classstack:
                if lastGlobalEntry:
                    lastGlobalEntry.setEndLine(lineno - 1)
                lastGlobalEntry = cur_class
            if cur_obj and isinstance(cur_obj, Function):
                cur_obj.setEndLine(lineno - 1)
            cur_obj = cur_class
            classstack.append((cur_class, thisindent))

        elif m.start("Module") >= 0:
            # we found a module definition
            thisindent = indent
            indent += 1
            # close all interfaces/modules indented at least as much
            while classstack and \
                    classstack[-1][1] >= thisindent:
                if classstack[-1][0] is not None:
                    # record the end line
                    classstack[-1][0].setEndLine(lineno - 1)
                del classstack[-1]
            lineno = lineno + src.count('\n', last_lineno_pos, start)
            last_lineno_pos = start
            module_name = m.group("ModuleName")
            # remember this module
            cur_class = Module(module, module_name, file, lineno)
            if not classstack:
                dictionary[module_name] = cur_class
                if lastGlobalEntry:
                    lastGlobalEntry.setEndLine(lineno - 1)
                lastGlobalEntry = cur_class
            if cur_obj and isinstance(cur_obj, Function):
                cur_obj.setEndLine(lineno - 1)
            cur_obj = cur_class
            classstack.append((cur_class, thisindent))

        elif m.start("Attribute") >= 0:
            lineno = lineno + src.count('\n', last_lineno_pos, start)
            last_lineno_pos = start
            index = -1
            while index >= -len(classstack):
                if classstack[index][0] is not None and \
                   not isinstance(classstack[index][0], Function) and \
                   not classstack[index][1] >= indent:
                    attributes = m.group("AttributeNames").split(',')
                    ro = m.group("AttributeReadonly")
                    for attribute in attributes:
                        attr = Attribute(module, attribute, file, lineno)
                        if ro:
                            attr.setPrivate()
                        classstack[index][0]._addattribute(attr)
                    break
                else:
                    index -= 1
                    if lastGlobalEntry:
                        lastGlobalEntry.setEndLine(lineno - 1)
                    lastGlobalEntry = None

        elif m.start("Begin") >= 0:
            # a begin of a block we are not interested in
            indent += 1

        elif m.start("End") >= 0:
            # an end of a block
            indent -= 1

        else:
            assert 0, "regexp _getnext found something unexpected"

    return dictionary
