# -*- coding: utf-8 -*-

# Copyright (c) 2005 - 2017 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing base classes used by the various class browsers.
"""


from __future__ import unicode_literals


class _ClbrBase(object):
    """
    Class implementing the base of all class browser objects.
    """
    def __init__(self, module, name, file, lineno):
        """
        Constructor
        
        @param module name of the module containing this object
        @type str
        @param name name of this object
        @type str
        @param file filename containing this object
        @type str
        @param lineno linenumber of the object definition
        @type int
        """
        self.module = module
        self.name = name
        self.file = file
        self.lineno = lineno
        self.endlineno = -1     # marker for "not set"
        
    def setEndLine(self, endLineNo):
        """
        Public method to set the ending line number.
        
        @param endLineNo number of the last line
        @type int
        """
        self.endlineno = endLineNo


class ClbrBase(_ClbrBase):
    """
    Class implementing the base of all complex class browser objects.
    """
    def __init__(self, module, name, file, lineno):
        """
        Constructor
        
        @param module name of the module containing this object
        @type str
        @param name name of this object
        @type str
        @param file filename containing this object
        @type str
        @param lineno linenumber of the object definition
        @type int
        """
        _ClbrBase.__init__(self, module, name, file, lineno)
        self.methods = {}
        self.attributes = {}
        self.classes = {}
        self.globals = {}
        
    def _addmethod(self, name, function):
        """
        Protected method to add information about a method.
        
        @param name name of method to be added
        @type str
        @param function Function object to be added
        @type Function
        """
        self.methods[name] = function
        
    def _getmethod(self, name):
        """
        Protected method to retrieve a method by name.
        
        @param name name of the method (string)
        @type str
        @return the named method
        @rtype Function or None
        """
        try:
            return self.methods[name]
        except KeyError:
            return None
        
    def _addglobal(self, attr):
        """
        Protected method to add information about global variables.
        
        @param attr Attribute object to be added
        @type Attribute
        """
        if attr.name not in self.globals:
            self.globals[attr.name] = attr
        else:
            self.globals[attr.name].addAssignment(attr.lineno)
        
    def _getglobal(self, name):
        """
        Protected method to retrieve a global variable by name.
        
        @param name name of the global variable
        @type str
        @return the named global variable
        @rtype Attribute or None
        """
        try:
            return self.globals[name]
        except KeyError:
            return None
        
    def _addattribute(self, attr):
        """
        Protected method to add information about attributes.
        
        @param attr Attribute object to be added
        @type Attribute
        """
        if attr.name not in self.attributes:
            self.attributes[attr.name] = attr
        else:
            self.attributes[attr.name].addAssignment(attr.lineno)
        
    def _getattribute(self, name):
        """
        Protected method to retrieve an attribute by name.
        
        @param name name of the attribute
        @type str
        @return the named attribute
        @rtype Attribute or None
        """
        try:
            return self.attributes[name]
        except KeyError:
            return None
        
    def _addclass(self, name, _class):
        """
        Protected method method to add a nested class to this class.
        
        @param name name of the class
        @type str
        @param _class Class object to be added
        @type Class
        """
        self.classes[name] = _class


class ClbrVisibilityMixinBase(object):
    """
    Class implementing the base class of all visibility mixins.
    """
    def isPrivate(self):
        """
        Public method to check, if the visibility is Private.
        
        @return flag indicating Private visibility
        @rtype bool
        """
        return self.visibility == 0
        
    def isProtected(self):
        """
        Public method to check, if the visibility is Protected.
        
        @return flag indicating Protected visibility
        @rtype bool
        """
        return self.visibility == 1
        
    def isPublic(self):
        """
        Public method to check, if the visibility is Public.
        
        @return flag indicating Public visibility
        @rtype bool
        """
        return self.visibility == 2
        
    def setPrivate(self):
        """
        Public method to set the visibility to Private.
        """
        self.visibility = 0
        
    def setProtected(self):
        """
        Public method to set the visibility to Protected.
        """
        self.visibility = 1
        
    def setPublic(self):
        """
        Public method to set the visibility to Public.
        """
        self.visibility = 2


class Attribute(_ClbrBase):
    """
    Class to represent an attribute.
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
        _ClbrBase.__init__(self, module, name, file, lineno)
        
        self.linenos = [lineno]
    
    def addAssignment(self, lineno):
        """
        Public method to add another assignment line number.
        
        @param lineno line number of the additional attribute assignment
        @type int
        """
        if lineno not in self.linenos:
            self.linenos.append(lineno)


class Class(ClbrBase):
    """
    Class to represent a class.
    """
    def __init__(self, module, name, superClasses, file, lineno):
        """
        Constructor
        
        @param module name of the module containing this class
        @type str
        @param name name of this class
        @type str
        @param superClasses list of class names this class is inherited from
        @type list of str
        @param file filename containing this class
        @type str
        @param lineno line number of the class definition
        @type int
        """
        ClbrBase.__init__(self, module, name, file, lineno)
        if superClasses is None:
            superClasses = []
        self.super = superClasses


class Module(ClbrBase):
    """
    Class to represent a module.
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
        ClbrBase.__init__(self, module, name, file, lineno)


class Function(ClbrBase):
    """
    Class to represent a function or method.
    """
    General = 0
    Static = 1
    Class = 2
    
    def __init__(self, module, name, file, lineno, signature='', separator=',',
                 modifierType=General, annotation=""):
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
        @param separator string separating the parameters of the function
        @type str
        @param modifierType type of the function
        @type int
        @param annotation function return annotation
        @type str
        """
        ClbrBase.__init__(self, module, name, file, lineno)
        self.parameters = [e.strip() for e in signature.split(separator)]
        self.modifier = modifierType
        self.annotation = annotation


class Coding(ClbrBase):
    """
    Class to represent a source coding.
    """
    def __init__(self, module, file, lineno, coding):
        """
        Constructor
        
        @param module name of the module containing this coding statement
        @type str
        @param file filename containing this coding statement
        @type str
        @param lineno line number of the coding definition
        @type int
        @param coding character coding of the source file
        @type str
        """
        ClbrBase.__init__(self, module, "Coding", file, lineno)
        self.coding = coding


class Enum(ClbrBase):
    """
    Class to represent an enum definition.
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
        @param lineno line number of the enum definition
        @type int
        """
        ClbrBase.__init__(self, module, name, file, lineno)
