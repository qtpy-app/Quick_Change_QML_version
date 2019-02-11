# -*- coding: utf-8 -*-

# Copyright (c) 2015 - 2017 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a path picker widget.
"""

from __future__ import unicode_literals

import os

try:
    from enum import Enum
except ImportError:
    from ThirdParty.enum import Enum

from PyQt5.QtCore import pyqtSignal, Qt, QFileInfo, QCoreApplication
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QToolButton, QSizePolicy

from . import E5FileDialog
from .E5LineEdit import E5ClearableLineEdit
from .E5Completers import E5FileCompleter, E5DirCompleter
from .E5ComboBox import E5ClearableComboBox

import UI.PixmapCache
import Utilities


class E5PathPickerModes(Enum):
    """
    Class implementing the path picker modes.
    """
    OpenFileMode = 0
    OpenFilesMode = 1
    SaveFileMode = 2
    SaveFileEnsureExtensionMode = 3
    SaveFileOverwriteMode = 4
    DirectoryMode = 5
    DirectoryShowFilesMode = 6
    CustomMode = 99
    NoMode = 100


class E5PathPickerBase(QWidget):
    """
    Class implementing the base of a path picker widget consisting of a
    line edit or combo box and a tool button to open a file dialog.
    
    @signal textChanged(path) emitted when the entered path has changed
        (line edit based widget)
    @signal editTextChanged(path) emitted when the entered path has changed
        (combo box based widget)
    @signal pathSelected(path) emitted after a path has been selected via the
        file dialog
    @signal aboutToShowPathPickerDialog emitted before the file dialog is shown
    @signal pickerButtonClicked emitted when the picker button was pressed and
        the widget mode is custom
    """
    DefaultMode = E5PathPickerModes.NoMode
    
    textChanged = pyqtSignal(str)
    editTextChanged = pyqtSignal(str)
    pathSelected = pyqtSignal(str)
    aboutToShowPathPickerDialog = pyqtSignal()
    pickerButtonClicked = pyqtSignal()
    
    def __init__(self, parent=None, useLineEdit=True):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        @param useLineEdit flag indicating the use of a line edit
        @type bool
        """
        super(E5PathPickerBase, self).__init__(parent)
        
        self.__lineEditKind = useLineEdit
        
        self.__mode = E5PathPicker.DefaultMode
        self.__editorEnabled = True
        
        self._completer = None
        self.__filters = ""
        self.__defaultDirectory = ""
        self.__windowTitle = ""
        
        self.__layout = QHBoxLayout()
        self.__layout.setSpacing(0)
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.__layout)
        
        if useLineEdit:
            self._editor = E5ClearableLineEdit(
                self, QCoreApplication.translate(
                    "E5PathPickerBase", "Enter Path Name"))
        else:
            self._editor = E5ClearableComboBox(
                self, QCoreApplication.translate(
                    "E5PathPickerBase", "Enter Path Name"))
        
        self.__button = QToolButton(self)
        self.__button.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.__button.setIcon(UI.PixmapCache.getIcon("open.png"))
        
        self.__layout.addWidget(self._editor)
        self.__layout.addWidget(self.__button)
        
        self.__button.clicked.connect(self.__showPathPickerDialog)
        if useLineEdit:
            self._editor.textEdited.connect(self.__pathEdited)
            self._editor.textChanged.connect(self.textChanged)
        else:
            self._editor.editTextChanged.connect(self.editTextChanged)
        
        self.setFocusProxy(self._editor)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        self.__button.setEnabled(self.__mode != E5PathPickerModes.NoMode)
    
    def __pathEdited(self, path):
        """
        Private slot handling editing of the path.
        
        @param path current text of the path line edit
        @type str
        """
        if self._completer and not self._completer.popup().isVisible():
            self._completer.setRootPath(Utilities.toNativeSeparators(path))
    
    def setMode(self, mode):
        """
        Public method to set the path picker mode.
        
        @param mode picker mode
        @type E5PathPickerModes
        """
        assert mode in E5PathPickerModes
        
        oldMode = self.__mode
        self.__mode = mode
        
        if mode != oldMode or (self.__lineEditKind and not self._completer):
            if self.__lineEditKind and self._completer:
                # Remove current completer
                self._editor.setCompleter(None)
                self._completer = None
            
            if mode != E5PathPickerModes.NoMode:
                if self.__lineEditKind:
                    # Set a new completer
                    if mode == E5PathPickerModes.DirectoryMode:
                        self._completer = E5DirCompleter(self._editor)
                    else:
                        self._completer = E5FileCompleter(self._editor)
                
                # set inactive text
                if mode == E5PathPickerModes.OpenFilesMode:
                    self._editor.setInactiveText(
                        self.tr("Enter Path Names separated by ';'"))
                else:
                    self._editor.setInactiveText(
                        self.tr("Enter Path Name"))
        self.__button.setEnabled(self.__mode != E5PathPickerModes.NoMode)
    
    def mode(self):
        """
        Public method to get the path picker mode.
        
        @return path picker mode
        @rtype E5PathPickerModes
        """
        return self.__mode
    
    def setPickerEnabled(self, enable):
        """
        Public method to set the enabled state of the file dialog button.
        
        @param enable flag indicating the enabled state
        @type bool
        """
        self.__button.setEnabled(enable)
    
    def isPickerEnabled(self):
        """
        Public method to get the file dialog button enabled state.
        
        @return flag indicating the enabled state
        @rtype bool
        """
        return self.__button.isEnabled()
    
    def clear(self):
        """
        Public method to clear the current path or list of paths.
        """
        self._editor.clear()
    
    def clearEditText(self):
        """
        Public method to clear the current path.
        """
        if not self.__lineEditKind:
            self._editor.clearEditText()
    
    def _setEditorText(self, text):
        """
        Protected method to set the text of the editor.
        
        @param text text to set
        @type str
        """
        if self.__lineEditKind:
            self._editor.setText(text)
        else:
            self._editor.setEditText(text)
            if text and self._editor.findText(text) == -1:
                self._editor.insertItem(0, text)
    
    def _editorText(self):
        """
        Protected method to get the text of the editor.
        
        @return text of the editor
        @rtype str
        """
        if self.__lineEditKind:
            return self._editor.text()
        else:
            return self._editor.currentText()
    
    def setText(self, path, toNative=True):
        """
        Public method to set the current path.
        
        @param path path to be set
        @type str
        @param toNative flag indicating to convert the path into
            a native format
        @type bool
        """
        if self.__mode == E5PathPickerModes.OpenFilesMode:
            self._setEditorText(path)
        else:
            if toNative:
                path = Utilities.toNativeSeparators(path)
            self._setEditorText(path)
            if self._completer:
                self._completer.setRootPath(path)
    
    def text(self, toNative=True):
        """
        Public method to get the current path.
        
        @param toNative flag indicating to convert the path into
            a native format
        @type bool
        @return current path
        @rtype str
        """
        if self.__mode == E5PathPickerModes.OpenFilesMode:
            if toNative:
                return ";".join(
                    [Utilities.toNativeSeparators(path)
                     for path in self._editorText().split(";")])
            else:
                return self._editorText()
        else:
            if toNative:
                return os.path.expanduser(
                    Utilities.toNativeSeparators(self._editorText()))
            else:
                return os.path.expanduser(self._editorText())
    
    def setEditText(self, path, toNative=True):
        """
        Public method to set the current path.
        
        @param path path to be set
        @type str
        @param toNative flag indicating to convert the path into
            a native format
        @type bool
        """
        self.setText(path, toNative=toNative)
    
    def currentText(self, toNative=True):
        """
        Public method to get the current path.
        
        @param toNative flag indicating to convert the path into
            a native format
        @type bool
        @return current path
        @rtype str
        """
        return self.text(toNative=toNative)
    
    def setPath(self, path, toNative=True):
        """
        Public method to set the current path.
        
        @param path path to be set
        @type str
        @param toNative flag indicating to convert the path into
            a native format
        @type bool
        """
        self.setText(path, toNative=toNative)
    
    def path(self, toNative=True):
        """
        Public method to get the current path.
        
        @param toNative flag indicating to convert the path into
            a native format
        @type bool
        @return current path
        @rtype str
        """
        return self.text(toNative=toNative)
    
    def paths(self, toNative=True):
        """
        Public method to get the list of entered paths.
        
        @param toNative flag indicating to convert the path into
            a native format
        @type bool
        @return entered paths
        @rtype list of str
        """
        if self.__mode == E5PathPickerModes.OpenFilesMode:
            return self.path(toNative=toNative).split(";")
        else:
            return [self.path(toNative=toNative)]
    
    def firstPath(self, toNative=True):
        """
        Public method to get the first path of a list of entered paths.
        
        @param toNative flag indicating to convert the path into
            a native format
        @type bool
        @return first path
        @rtype str
        """
        return self.paths(toNative=toNative)[0]
    
    def lastPath(self, toNative=True):
        """
        Public method to get the last path of a list of entered paths.
        
        @param toNative flag indicating to convert the path into
            a native format
        @type bool
        @return last path
        @rtype str
        """
        return self.paths(toNative=toNative)[-1]
    
    def setEditorEnabled(self, enable):
        """
        Public method to set the path editor's enabled state.
        
        @param enable flag indicating the enable state
        @type bool
        """
        if enable != self._editorEnabled:
            self._editorEnabled = enable
            self._editor.setEnabled(enable)
    
    def editorEnabled(self):
        """
        Public method to get the path editor's enabled state.
        
        @return flag indicating the enabled state
        @rtype bool
        """
        return self._editorEnabled
    
    def setDefaultDirectory(self, directory):
        """
        Public method to set the default directory.
        
        @param directory default directory
        @type str
        """
        self.__defaultDirectory = directory
    
    def defaultDirectory(self):
        """
        Public method to get the default directory.
        
        @return default directory
        @rtype str
        """
        return self.__defaultDirectory
    
    def setWindowTitle(self, title):
        """
        Public method to set the path picker dialog window title.
        
        @param title window title
        @type str
        """
        self.__windowTitle = title
    
    def windowTitle(self):
        """
        Public method to get the path picker dialog's window title.
        
        @return window title
        @rtype str
        """
        return self.__windowTitle
    
    def setFilters(self, filters):
        """
        Public method to set the filters for the path picker dialog.
        
        Note: Multiple filters must be separated by ';;'.
        
        @param filters string containing the file filters
        @type str
        """
        self.__filters = filters
    
    def filters(self):
        """
        Public methods to get the filter string.
        
        @return filter string
        @rtype str
        """
        return self.__filters
    
    def setNameFilters(self, filters):
        """
        Public method to set the name filters for the completer.
        
        @param filters list of file name filters
        @type list of str
        """
        if self._completer:
            self._completer.model().setNameFilters(filters)
    
    def setButtonToolTip(self, tooltip):
        """
        Public method to set the tool button tool tip.
        
        @param tooltip text to be set as a tool tip
        @type str
        """
        self.__button.setToolTip(tooltip)
    
    def buttonToolTip(self):
        """
        Public method to get the tool button tool tip.
        
        @return tool tip text
        @rtype str
        """
        return self.__button.toolTip()
    
    def setEditorToolTip(self, tooltip):
        """
        Public method to set the editor tool tip.
        
        @param tooltip text to be set as a tool tip
        @type str
        """
        self._editor.setToolTip(tooltip)
    
    def editorToolTip(self):
        """
        Public method to get the editor tool tip.
        
        @return tool tip text
        @rtype str
        """
        return self._editor.toolTip()
    
    def __showPathPickerDialog(self):
        """
        Private slot to show the path picker dialog.
        """
        if self.__mode == E5PathPickerModes.NoMode:
            return
        
        if self.__mode == E5PathPickerModes.CustomMode:
            self.pickerButtonClicked.emit()
            return
        
        self.aboutToShowPathPickerDialog.emit()
        
        windowTitle = self.__windowTitle
        if not windowTitle:
            if self.__mode == E5PathPickerModes.OpenFileMode:
                windowTitle = self.tr("Choose a file to open")
            elif self.__mode == E5PathPickerModes.OpenFilesMode:
                windowTitle = self.tr("Choose files to open")
            elif self.__mode in [
                E5PathPickerModes.SaveFileMode,
                    E5PathPickerModes.SaveFileEnsureExtensionMode,
                    E5PathPickerModes.SaveFileOverwriteMode]:
                windowTitle = self.tr("Choose a file to save")
            elif self.__mode == E5PathPickerModes.DirectoryMode:
                windowTitle = self.tr("Choose a directory")
        
        directory = self._editorText()
        if not directory and self.__defaultDirectory:
            directory = self.__defaultDirectory
        if self.__mode == E5PathPickerModes.OpenFilesMode:
            directory = os.path.expanduser(directory.split(";")[0])
        else:
            directory = os.path.expanduser(directory)
        if not os.path.isabs(directory) and self.__defaultDirectory:
            directory = os.path.join(self.__defaultDirectory, directory)
        directory = Utilities.fromNativeSeparators(directory)
        
        if self.__mode == E5PathPickerModes.OpenFileMode:
            path = E5FileDialog.getOpenFileName(
                self,
                windowTitle,
                directory,
                self.__filters)
            path = Utilities.toNativeSeparators(path)
        elif self.__mode == E5PathPickerModes.OpenFilesMode:
            paths = E5FileDialog.getOpenFileNames(
                self,
                windowTitle,
                directory,
                self.__filters)
            path = ";".join([Utilities.toNativeSeparators(path)
                             for path in paths])
        elif self.__mode == E5PathPickerModes.SaveFileMode:
            path = E5FileDialog.getSaveFileName(
                self,
                windowTitle,
                directory,
                self.__filters,
                E5FileDialog.Options(E5FileDialog.DontConfirmOverwrite))
            path = Utilities.toNativeSeparators(path)
        elif self.__mode == E5PathPickerModes.SaveFileEnsureExtensionMode:
            path, selectedFilter = E5FileDialog.getSaveFileNameAndFilter(
                self,
                windowTitle,
                directory,
                self.__filters,
                None,
                E5FileDialog.Options(E5FileDialog.DontConfirmOverwrite))
            path = Utilities.toNativeSeparators(path)
            if path:
                ext = QFileInfo(path).suffix()
                if not ext:
                    ex = selectedFilter.split("(*")[1].split(")")[0]
                    if ex:
                        path += ex
        elif self.__mode == E5PathPickerModes.SaveFileOverwriteMode:
            path = E5FileDialog.getSaveFileName(
                self,
                windowTitle,
                directory,
                self.__filters)
            path = Utilities.toNativeSeparators(path)
        elif self.__mode == E5PathPickerModes.DirectoryMode:
            path = E5FileDialog.getExistingDirectory(
                self,
                windowTitle,
                directory,
                E5FileDialog.Options(E5FileDialog.ShowDirsOnly))
            path = Utilities.toNativeSeparators(path)
            while path.endswith(os.sep):
                path = path[:-1]
        elif self.__mode == E5PathPickerModes.DirectoryShowFilesMode:
            path = E5FileDialog.getExistingDirectory(
                self,
                windowTitle,
                directory,
                E5FileDialog.Options(E5FileDialog.DontUseNativeDialog))
            path = Utilities.toNativeSeparators(path)
            while path.endswith(os.sep):
                path = path[:-1]
        
        if path:
            self._setEditorText(path)
            self.pathSelected.emit(path)
    
    def setReadOnly(self, readOnly):
        """
        Public method to set the path picker to read only mode.
        
        @param readOnly flag indicating read only mode
        @type bool
        """
        try:
            self._editor.setReadOnly(readOnly)
        except AttributeError:
            self._editor.setEditable(not readOnly)
        self.setPickerEnabled(not readOnly)
    
    def isReadOnly(self):
        """
        Public method to check the path picker for read only mode.
        
        @return flg indicating read only mode
        @rtype bool
        """
        try:
            return self._editor.isReadOnly()
        except AttributeError:
            return not self._editor.isEditable()
    
    ##################################################################
    ## Methods below emulate some of the QComboBox API
    ##################################################################
    
    def addItems(self, pathsList):
        """
        Public method to add paths to the current list.
        
        @param pathsList list of paths to add
        @type list of str
        """
        self._editor.addItems(pathsList)
    
    def addItem(self, path):
        """
        Public method to add a paths to the current list.
        
        @param path path to add
        @type str
        """
        self._editor.addItem(path)
    
    def setPathsList(self, pathsList):
        """
        Public method to set the paths list.
        
        @param pathsList list of paths
        @type list of str
        """
        self.clear()
        self.addItems(pathsList)
    
    def setCurrentIndex(self, index):
        """
        Public slot to set the current index.
        
        @param index index of the item to set current
        @type int
        """
        self._editor.setCurrentIndex(index)
    
    def setInsertPolicy(self, policy):
        """
        Public method to set the insertion policy of the combo box.
        
        @param policy insertion policy
        @type QComboBox.InsertPolicy
        """
        self._editor.setInsertPolicy(policy)
    
    def setSizeAdjustPolicy(self, policy):
        """
        Public method to set the size adjust policy of the combo box.
        
        @param policy size adjust policy
        @type QComboBox.SizeAdjustPolicy
        """
        self._editor.setSizeAdjustPolicy(policy)


class E5PathPicker(E5PathPickerBase):
    """
    Class implementing a path picker widget consisting of a line edit and a
    tool button to open a file dialog.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(E5PathPicker, self).__init__(parent, useLineEdit=True)


class E5ComboPathPicker(E5PathPickerBase):
    """
    Class implementing a path picker widget consisting of a combobox and a
    tool button to open a file dialog.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(E5ComboPathPicker, self).__init__(parent, useLineEdit=False)
    
    def getPathItems(self):
        """
        Public method to get the list of remembered paths.
        
        @return list od remembered paths
        @rtype list of str
        """
        paths = []
        for index in range(self._editor.count()):
            paths.append(self._editor.itemText(index))
        return paths
