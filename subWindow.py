# -*- coding: utf-8 -*-

"""
Module implementing subForm.
"""

"""
Created on $date$ <br>
description: $description$ <br>
author: 625781186@qq.com <br>
site: https://github.com/625781186 <br>
更多经典例子:https://github.com/892768447/PyQt <br>
课件: https://github.com/625781186/WoHowLearn_PyQt5 <br>
视频教程: https://space.bilibili.com/1863103/#/ <br>
"""
from collections import OrderedDict
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# from PyQt5.QtWidgets import QWidget

try:
    from Ui_subWindow import Ui_Form
except ImportError as e:
    print("--1 --", e)
    try:
        from .Ui_subWindow import Ui_Form
    except ImportError as e:
        print("--2 --", e)


class subForm(QWidget, Ui_Form):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(subForm, self).__init__(parent)
        self.setupUi(self)
        self.findParent().enableFindButton(self)

    def closeEvent(self, QCloseEvent):
        dia = self.findParent()
        dia.enableFindButton(self, close=True)

    @pyqtSlot(str)
    def on_findtextCombo_editTextChanged(self, text):
        """
        Private slot to handle the editTextChanged signal of the find
        text combo.

        @param text (ignored)
        """

        self.findParent().enableFindButton(self)

    @pyqtSlot(str)
    def on_replacetextCombo_editTextChanged(self, text):
        """
        Private slot to handle the editTextChanged signal of the replace
        text combo.

        @param text (ignored)
        """

        self.findParent().enableFindButton(self)

    @pyqtSlot(str)
    def on_filterEdit_textEdited(self, text):
        """
        Private slot to handle the textChanged signal of the file filter edit.

        @param text (ignored)
        """

        self.findParent().enableFindButton(self)


    def findParent(self):
        own = self
        while not isinstance(own.parent(), QDialog):
            own = own.parent()
        return own.parent()

    def serialize(self):
        return OrderedDict([
            ('findtextCombo', self.findtextCombo.currentText()),
            ('replacetextCombo', self.replacetextCombo.currentText()),
            ('caseCheckBox', self.caseCheckBox.isChecked()),
            ('regexpCheckBox', self.regexpCheckBox.isChecked()),
            ('wordCheckBox', self.wordCheckBox.isChecked()),
            ('feelLikeCheckBox', self.feelLikeCheckBox.isChecked()),
            ('filterEdit', self.filterEdit.text()),
        ])

    def deserialize(self, data):
        """·´ÐòÁÐ»¯"""

        self.findtextCombo.setCurrentText(data['findtextCombo'])
        self.replacetextCombo.setCurrentText(data['replacetextCombo'])
        self.caseCheckBox.setChecked(data['caseCheckBox'])
        self.regexpCheckBox.setChecked(data['regexpCheckBox'])
        self.wordCheckBox.setChecked(data['wordCheckBox'])
        self.feelLikeCheckBox.setChecked(data['feelLikeCheckBox'])
        self.filterEdit.setText(data['filterEdit'])

        return self


