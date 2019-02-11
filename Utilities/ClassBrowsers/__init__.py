# -*- coding: utf-8 -*-

# Copyright (c) 2005 - 2017 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Package implementing class browsers for various languages.

Currently it offers class browser support for the following
programming languages.

<ul>
<li>CORBA IDL</li>
<li>JavaScript</li>
<li>ProtoBuf</li>
<li>Python 2</li>
<li>Python 3</li>
<li>Ruby</li>
</ul>
"""

from __future__ import unicode_literals

import os
import imp
import sys

import Preferences

PY_SOURCE = imp.PY_SOURCE
PTL_SOURCE = 128
RB_SOURCE = 129
IDL_SOURCE = 130
JS_SOURCE = 131
PROTO_SOURCE = 132

SUPPORTED_TYPES = [PY_SOURCE, PTL_SOURCE, RB_SOURCE, IDL_SOURCE, JS_SOURCE,
                   PROTO_SOURCE]

__extensions = {
    "IDL": [".idl"],
    "Python": [".py", ".pyw", ".ptl"],  # currently not used
    "Ruby": [".rb"],
    "JavaScript": [".js"],
    "ProtoBuf": [".proto"],
}


def readmodule(module, path=None, isPyFile=False):
    """
    Read a source file and return a dictionary of classes, functions, modules,
    etc. .
    
    The real work of parsing the source file is delegated to the individual
    file parsers.

    @param module name of the source file
    @type str
    @param path list of paths the file should be searched in
    @type list of str
    @param isPyFile flag indicating a Python file
    @type bool
    @return the resulting dictionary
    @rtype dict
    """
    ext = os.path.splitext(module)[1].lower()
    path = [] if path is None else path[:]
    
    if ext in __extensions["IDL"]:
        from . import idlclbr
        dictionary = idlclbr.readmodule_ex(module, path)
        idlclbr._modules.clear()
    elif ext in __extensions["ProtoBuf"]:
        from . import protoclbr
        dictionary = protoclbr.readmodule_ex(module, path)
        protoclbr._modules.clear()
    elif ext in __extensions["Ruby"]:
        from . import rbclbr
        dictionary = rbclbr.readmodule_ex(module, path)
        rbclbr._modules.clear()
    elif ext in __extensions["JavaScript"] and sys.version_info[0] == 3:
        from . import jsclbr
        dictionary = jsclbr.readmodule_ex(module, path)
        jsclbr._modules.clear()
    elif ext in Preferences.getPython("PythonExtensions") or \
        ext in Preferences.getPython("Python3Extensions") or \
            isPyFile:
        from . import pyclbr
        dictionary = pyclbr.readmodule_ex(module, path, isPyFile=isPyFile)
        pyclbr._modules.clear()
    else:
        # try Python if it is without extension
        from . import pyclbr
        dictionary = pyclbr.readmodule_ex(module, path)
        pyclbr._modules.clear()
    
    return dictionary


def find_module(name, path, isPyFile=False):
    """
    Module function to extend the Python module finding mechanism.
    
    This function searches for files in the given list of paths. If the
    file name doesn't have an extension or an extension of .py, the normal
    Python search implemented in the imp module is used. For all other
    supported files only the paths list is searched.
    
    @param name file name or module name to search for
    @type str
    @param path search paths
    @type list of str
    @param isPyFile flag indicating a Python file
    @type bool
    @return tuple of the open file, pathname and description. Description
        is a tuple of file suffix, file mode and file type)
    @rtype tuple
    @exception ImportError The file or module wasn't found.
    """
    ext = os.path.splitext(name)[1].lower()
    
    if ext in __extensions["Ruby"]:
        for p in path:      # only search in path
            pathname = os.path.join(p, name)
            if os.path.exists(pathname):
                return (open(pathname), pathname, (ext, 'r', RB_SOURCE))
        raise ImportError
    
    elif ext in __extensions["IDL"]:
        for p in path:      # only search in path
            pathname = os.path.join(p, name)
            if os.path.exists(pathname):
                return (open(pathname), pathname, (ext, 'r', IDL_SOURCE))
        raise ImportError
    
    elif ext in __extensions["ProtoBuf"]:
        for p in path:      # only search in path
            pathname = os.path.join(p, name)
            if os.path.exists(pathname):
                return (open(pathname), pathname, (ext, 'r', PROTO_SOURCE))
        raise ImportError
    
    elif ext in __extensions["JavaScript"]:
        for p in path:      # only search in path
            pathname = os.path.join(p, name)
            if os.path.exists(pathname):
                return (open(pathname), pathname, (ext, 'r', JS_SOURCE))
        raise ImportError
    
    elif ext == '.ptl':
        for p in path:      # only search in path
            pathname = os.path.join(p, name)
            if os.path.exists(pathname):
                return (open(pathname), pathname, (ext, 'r', PTL_SOURCE))
        raise ImportError
    
    if name.lower().endswith('.py'):
        name = name[:-3]
    
    try:
        return imp.find_module(name, path)
    except ImportError:
        if name.lower().endswith(
                tuple(Preferences.getPython("PythonExtensions") +
                      Preferences.getPython("Python3Extensions"))) or \
                isPyFile:
            for p in path:      # search in path
                pathname = os.path.join(p, name)
                if os.path.exists(pathname):
                    return (open(pathname), pathname, (ext, 'r', PY_SOURCE))
        raise ImportError
    except SyntaxError:
        # re-raise as an import error
        raise ImportError
