# -*- coding: utf-8 -*-

# Copyright (c) 2015 - 2017 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to show some help text.
"""

from __future__ import unicode_literals

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog

from .Ui_E5SimpleHelpDialog import Ui_E5SimpleHelpDialog


class E5SimpleHelpDialog(QDialog, Ui_E5SimpleHelpDialog):
    """
    Class implementing a dialog to show some help text.
    """
    def __init__(self, title="", label="", helpStr="", parent=None):
        """
        Constructor
        
        @param title title of the window
        @type str
        @param label label for the help
        @type str
        @param helpStr HTML help text
        @type str
        @param parent reference to the parent widget
        @type QWidget
        """
        super(E5SimpleHelpDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.Window)
        
        self.setWindowTitle(title)
        if label:
            self.helpLabel.setText(label)
        else:
            self.helpLabel.hide()
        self.helpEdit.setHtml(helpStr)
