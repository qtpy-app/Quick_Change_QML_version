# -*- coding: utf-8 -*-

# Copyright (c) 2012 - 2017 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a horizontal search widget for QTextEdit.
"""

from __future__ import unicode_literals

from PyQt5.QtCore import pyqtSlot, Qt, QMetaObject, QSize
from PyQt5.QtGui import QPalette, QBrush, QColor, QTextDocument, QTextCursor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, \
    QComboBox, QCheckBox, QToolButton, QSizePolicy

from E5Gui.E5ComboBox import E5ClearableComboBox

import UI.PixmapCache


class E5TextEditSearchWidget(QWidget):
    """
    Class implementing a horizontal search widget for QTextEdit.
    """
    def __init__(self, parent=None, widthForHeight=True):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        @param widthForHeight flag indicating to prefer width for height.
            If this parameter is False, some widgets are shown in a third
            line.
        @type bool
        """
        super(E5TextEditSearchWidget, self).__init__(parent)
        self.__setupUi(widthForHeight)
        
        self.__textedit = None
        self.__texteditType = ""
        self.__findBackwards = True
        
        self.__defaultBaseColor = \
            self.findtextCombo.lineEdit().palette().color(QPalette.Base)
        self.__defaultTextColor = \
            self.findtextCombo.lineEdit().palette().color(QPalette.Text)
        
        self.findHistory = []
        
        self.findtextCombo.setCompleter(None)
        self.findtextCombo.lineEdit().returnPressed.connect(
            self.__findByReturnPressed)
        
        self.__setSearchButtons(False)
        self.infoLabel.hide()
        
        self.setFocusProxy(self.findtextCombo)
    
    def __setupUi(self, widthForHeight):
        """
        Private method to generate the UI.
        
        @param widthForHeight flag indicating to prefer width for height
        @type bool
        """
        self.setObjectName("E5TextEditSearchWidget")
        
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        
        # row 1 of widgets
        self.horizontalLayout1 = QHBoxLayout()
        self.horizontalLayout1.setObjectName("horizontalLayout1")
        
        self.label = QLabel(self)
        self.label.setObjectName("label")
        self.label.setText(self.tr("Find:"))
        self.horizontalLayout1.addWidget(self.label)
        
        self.findtextCombo = E5ClearableComboBox(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.findtextCombo.sizePolicy().hasHeightForWidth())
        self.findtextCombo.setSizePolicy(sizePolicy)
        self.findtextCombo.setMinimumSize(QSize(200, 0))
        self.findtextCombo.setEditable(True)
        self.findtextCombo.setInsertPolicy(QComboBox.InsertAtTop)
        self.findtextCombo.setDuplicatesEnabled(False)
        self.findtextCombo.setObjectName("findtextCombo")
        self.horizontalLayout1.addWidget(self.findtextCombo)
        
        # row 2 (maybe) of widgets
        self.horizontalLayout2 = QHBoxLayout()
        self.horizontalLayout2.setObjectName("horizontalLayout2")
        
        self.caseCheckBox = QCheckBox(self)
        self.caseCheckBox.setObjectName("caseCheckBox")
        self.caseCheckBox.setText(self.tr("Match case"))
        self.horizontalLayout2.addWidget(self.caseCheckBox)
        
        self.wordCheckBox = QCheckBox(self)
        self.wordCheckBox.setObjectName("wordCheckBox")
        self.wordCheckBox.setText(self.tr("Whole word"))
        self.horizontalLayout2.addWidget(self.wordCheckBox)
        
        # layout for the navigation buttons
        self.horizontalLayout3 = QHBoxLayout()
        self.horizontalLayout3.setSpacing(0)
        self.horizontalLayout3.setObjectName("horizontalLayout3")
        
        self.findPrevButton = QToolButton(self)
        self.findPrevButton.setObjectName("findPrevButton")
        self.findPrevButton.setToolTip(self.tr(
            "Press to find the previous occurrence"))
        self.findPrevButton.setIcon(UI.PixmapCache.getIcon("1leftarrow.png"))
        self.horizontalLayout3.addWidget(self.findPrevButton)
        
        self.findNextButton = QToolButton(self)
        self.findNextButton.setObjectName("findNextButton")
        self.findNextButton.setToolTip(self.tr(
            "Press to find the next occurrence"))
        self.findNextButton.setIcon(UI.PixmapCache.getIcon("1rightarrow.png"))
        self.horizontalLayout3.addWidget(self.findNextButton)
        
        self.horizontalLayout2.addLayout(self.horizontalLayout3)
        
        # info label (in row 2 or 3)
        self.infoLabel = QLabel(self)
        self.infoLabel.setText("")
        self.infoLabel.setObjectName("infoLabel")
        
        # place everything together
        self.verticalLayout.addLayout(self.horizontalLayout1)
        if widthForHeight:
            self.horizontalLayout1.addLayout(self.horizontalLayout2)
        else:
            self.verticalLayout.addLayout(self.horizontalLayout2)
        self.verticalLayout.addWidget(self.infoLabel)
        
        QMetaObject.connectSlotsByName(self)
        
        self.setTabOrder(self.findtextCombo, self.caseCheckBox)
        self.setTabOrder(self.caseCheckBox, self.wordCheckBox)
        self.setTabOrder(self.wordCheckBox, self.findPrevButton)
        self.setTabOrder(self.findPrevButton, self.findNextButton)
    
    def attachTextEdit(self, textedit, editType="QTextEdit"):
        """
        Public method to attach a QTextEdit widget.
        
        @param textedit reference to the edit widget to be attached
        @type QTextEdit, QWebEngineView or QWebView
        @param editType type of the attached edit widget
        @type str (one of "QTextEdit", "QWebEngineView" or "QWebView")
        """
        assert editType in ["QTextEdit", "QWebEngineView", "QWebView"]
        
        self.__textedit = textedit
        self.__texteditType = editType
        
        self.wordCheckBox.setVisible(editType == "QTextEdit")
    
    def keyPressEvent(self, event):
        """
        Protected slot to handle key press events.
        
        @param event reference to the key press event (QKeyEvent)
        """
        if self.__textedit and event.key() == Qt.Key_Escape:
            self.__textedit.setFocus(Qt.ActiveWindowFocusReason)
            event.accept()
    
    @pyqtSlot(str)
    def on_findtextCombo_editTextChanged(self, txt):
        """
        Private slot to enable/disable the find buttons.
        
        @param txt text of the combobox (string)
        """
        self.__setSearchButtons(txt != "")
        
        self.infoLabel.hide()
        self.__setFindtextComboBackground(False)
    
    def __setSearchButtons(self, enabled):
        """
        Private slot to set the state of the search buttons.
        
        @param enabled flag indicating the state (boolean)
        """
        self.findPrevButton.setEnabled(enabled)
        self.findNextButton.setEnabled(enabled)
    
    def __findByReturnPressed(self):
        """
        Private slot to handle the returnPressed signal of the findtext
        combobox.
        """
        self.__find(self.__findBackwards)
    
    @pyqtSlot()
    def on_findPrevButton_clicked(self):
        """
        Private slot to find the previous occurrence.
        """
        self.__find(True)
    
    @pyqtSlot()
    def on_findNextButton_clicked(self):
        """
        Private slot to find the next occurrence.
        """
        self.__find(False)
    
    def __find(self, backwards):
        """
        Private method to search the associated text edit.
        
        @param backwards flag indicating a backwards search (boolean)
        """
        if not self.__textedit:
            return
        
        self.infoLabel.clear()
        self.infoLabel.hide()
        self.__setFindtextComboBackground(False)
        
        txt = self.findtextCombo.currentText()
        if not txt:
            return
        self.__findBackwards = backwards
        
        # This moves any previous occurrence of this statement to the head
        # of the list and updates the combobox
        if txt in self.findHistory:
            self.findHistory.remove(txt)
        self.findHistory.insert(0, txt)
        self.findtextCombo.clear()
        self.findtextCombo.addItems(self.findHistory)
        
        if self.__texteditType == "QTextEdit":
            ok = self.__findPrevNextQTextEdit(backwards)
            self.__findNextPrevCallback(ok)
        elif self.__texteditType == "QWebEngineView":
            self.__findPrevNextQWebEngineView(backwards)
        elif self.__texteditType == "QWebView":
            ok = self.__findPrevNextQWebView(backwards)
            self.__findNextPrevCallback(ok)
    
    def __findPrevNextQTextEdit(self, backwards):
        """
        Private method to to search the associated edit widget of
        type QTextEdit.
        
        @param backwards flag indicating a backwards search
        @type bool
        @return flag indicating the search result
        @rtype bool
        """
        if backwards:
            flags = QTextDocument.FindFlags(QTextDocument.FindBackward)
        else:
            flags = QTextDocument.FindFlags()
        if self.caseCheckBox.isChecked():
            flags |= QTextDocument.FindCaseSensitively
        if self.wordCheckBox.isChecked():
            flags |= QTextDocument.FindWholeWords
        
        ok = self.__textedit.find(self.findtextCombo.currentText(), flags)
        if not ok:
            # wrap around once
            cursor = self.__textedit.textCursor()
            if backwards:
                moveOp = QTextCursor.End        # move to end of document
            else:
                moveOp = QTextCursor.Start      # move to start of document
            cursor.movePosition(moveOp)
            self.__textedit.setTextCursor(cursor)
            ok = self.__textedit.find(self.findtextCombo.currentText(), flags)
        
        return ok
    
    def __findPrevNextQWebView(self, backwards):
        """
        Private method to to search the associated edit widget of
        type QWebView.
        
        @param backwards flag indicating a backwards search
        @type bool
        @return flag indicating the search result
        @rtype bool
        """
        from PyQt5.QtWebKitWidgets import QWebPage
        
        findFlags = QWebPage.FindFlags(QWebPage.FindWrapsAroundDocument)
        if self.caseCheckBox.isChecked():
            findFlags |= QWebPage.FindCaseSensitively
        if backwards:
            findFlags |= QWebPage.FindBackward
        
        return self.__textedit.findText(self.findtextCombo.currentText(),
                                        findFlags)
    
    def __findPrevNextQWebEngineView(self, backwards):
        """
        Private method to to search the associated edit widget of
        type QWebEngineView.
        
        @param backwards flag indicating a backwards search
        @type bool
        """
        from PyQt5.QtWebEngineWidgets import QWebEnginePage
        
        findFlags = QWebEnginePage.FindFlags()
        if self.caseCheckBox.isChecked():
            findFlags |= QWebEnginePage.FindCaseSensitively
        if backwards:
            findFlags |= QWebEnginePage.FindBackward
        self.__textedit.findText(self.findtextCombo.currentText(),
                                 findFlags, self.__findNextPrevCallback)
    
    def __findNextPrevCallback(self, found):
        """
        Private method to process the result of the last search.
        
        @param found flag indicating if the last search succeeded
        @type bool
        """
        if not found:
            txt = self.findtextCombo.currentText()
            self.infoLabel.setText(
                self.tr("'{0}' was not found.").format(txt))
            self.infoLabel.show()
            self.__setFindtextComboBackground(True)
    
    def __setFindtextComboBackground(self, error):
        """
        Private slot to change the findtext combo background to indicate
        errors.
        
        @param error flag indicating an error condition (boolean)
        """
        le = self.findtextCombo.lineEdit()
        p = le.palette()
        if error:
            p.setBrush(QPalette.Base, QBrush(QColor("#FF6666")))
            p.setBrush(QPalette.Text, QBrush(QColor("#000000")))
        else:
            p.setBrush(QPalette.Base, self.__defaultBaseColor)
            p.setBrush(QPalette.Text, self.__defaultTextColor)
        le.setPalette(p)
        le.update()
