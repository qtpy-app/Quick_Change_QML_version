# -*- coding: utf-8 -*-

# Copyright (c) 2016 - 2017 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to select from a list of strings.
"""

from __future__ import unicode_literals

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QAbstractItemView

from .Ui_E5ListSelectionDialog import Ui_E5ListSelectionDialog


class E5ListSelectionDialog(QDialog, Ui_E5ListSelectionDialog):
    """
    Class implementing a dialog to select from a list of strings.
    """
    def __init__(self, entries,
                 selectionMode=QAbstractItemView.ExtendedSelection,
                 title="", message="", parent=None):
        """
        Constructor
        
        @param entries list of entries to select from
        @type list of str
        @param selectionMode selection mode for the list
        @type QAbstractItemView.SelectionMode
        @param title tirle of the dialog
        @type str
        @param message message to be show in the dialog
        @type str
        @param parent reference to the parent widget
        @type QWidget
        """
        super(E5ListSelectionDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.selectionList.setSelectionMode(selectionMode)
        if title:
            self.setWindowTitle(title)
        if message:
            self.messageLabel.setText(message)
        
        self.selectionList.addItems(entries)
        
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
    
    @pyqtSlot()
    def on_selectionList_itemSelectionChanged(self):
        """
        Private slot handling a change of the selection.
        """
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(
            len(self.selectionList.selectedItems()) > 0)
    
    def getSelection(self):
        """
        Public method to retrieve the selected items.
        
        @return selected entries
        @rtype list of str
        """
        entries = []
        for item in self.selectionList.selectedItems():
            entries.append(item.text())
        return entries
