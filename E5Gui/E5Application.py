# -*- coding: utf-8 -*-

# Copyright (c) 2009 - 2017 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Class implementing a specialized application class.
"""

from __future__ import unicode_literals

from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QApplication


class E5Application(QApplication):
    """
    Eric application class with an object registry.
    """
    def __init__(self, argv):
        """
        Constructor
        
        @param argv command line arguments
        """
        try:
            QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
            # __IGNORE_EXCEPTION__
        except AttributeError:
            pass
        
        super(E5Application, self).__init__(argv)
        
        QCoreApplication.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
        try:
            QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
            # __IGNORE_EXCEPTION__
        except AttributeError:
            pass
        
        self.__objectRegistry = {}
        self.__pluginObjectRegistry = {}
        
    def registerObject(self, name, objectRef):
        """
        Public method to register an object in the object registry.
        
        @param name name of the object (string)
        @param objectRef reference to the object
        @exception KeyError raised when the given name is already in use
        """
        if name in self.__objectRegistry:
            raise KeyError('Object "{0}" already registered.'.format(name))
        else:
            self.__objectRegistry[name] = objectRef
        
    def getObject(self, name):
        """
        Public method to get a reference to a registered object.
        
        @param name name of the object (string)
        @return reference to the registered object
        @exception KeyError raised when the given name is not known
        """
        if name in self.__objectRegistry:
            return self.__objectRegistry[name]
        else:
            raise KeyError('Object "{0}" is not registered.'.format(name))
        
    def registerPluginObject(self, name, objectRef, pluginType=None):
        """
        Public method to register a plugin object in the object registry.
        
        @param name name of the plugin object (string)
        @param objectRef reference to the plugin object
        @keyparam pluginType type of the plugin object (string)
        @exception KeyError raised when the given name is already in use
        """
        if name in self.__pluginObjectRegistry:
            raise KeyError(
                'Pluginobject "{0}" already registered.'.format(name))
        else:
            self.__pluginObjectRegistry[name] = (objectRef, pluginType)
        
    def unregisterPluginObject(self, name):
        """
        Public method to unregister a plugin object in the object registry.
        
        @param name name of the plugin object (string)
        """
        if name in self.__pluginObjectRegistry:
            del self.__pluginObjectRegistry[name]
        
    def getPluginObject(self, name):
        """
        Public method to get a reference to a registered plugin object.
        
        @param name name of the plugin object (string)
        @return reference to the registered plugin object
        @exception KeyError raised when the given name is not known
        """
        if name in self.__pluginObjectRegistry:
            return self.__pluginObjectRegistry[name][0]
        else:
            raise KeyError(
                'Pluginobject "{0}" is not registered.'.format(name))
        
    def getPluginObjects(self):
        """
        Public method to get a list of (name, reference) pairs of all
        registered plugin objects.
        
        @return list of (name, reference) pairs
        """
        objects = []
        for name in self.__pluginObjectRegistry:
            objects.append((name, self.__pluginObjectRegistry[name][0]))
        return objects
        
    def getPluginObjectType(self, name):
        """
        Public method to get the type of a registered plugin object.
        
        @param name name of the plugin object (string)
        @return type of the plugin object (string)
        @exception KeyError raised when the given name is not known
        """
        if name in self.__pluginObjectRegistry:
            return self.__pluginObjectRegistry[name][1]
        else:
            raise KeyError(
                'Pluginobject "{0}" is not registered.'.format(name))

e5App = QCoreApplication.instance
