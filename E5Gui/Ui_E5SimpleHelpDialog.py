# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\E5Gui\E5SimpleHelpDialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_E5SimpleHelpDialog(object):
    def setupUi(self, E5SimpleHelpDialog):
        E5SimpleHelpDialog.setObjectName("E5SimpleHelpDialog")
        E5SimpleHelpDialog.resize(500, 600)
        E5SimpleHelpDialog.setWindowTitle("")
        E5SimpleHelpDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(E5SimpleHelpDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.helpLabel = QtWidgets.QLabel(E5SimpleHelpDialog)
        self.helpLabel.setObjectName("helpLabel")
        self.verticalLayout.addWidget(self.helpLabel)
        self.helpEdit = QtWidgets.QTextBrowser(E5SimpleHelpDialog)
        self.helpEdit.setTabChangesFocus(True)
        self.helpEdit.setReadOnly(True)
        self.helpEdit.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.helpEdit.setOpenExternalLinks(True)
        self.helpEdit.setObjectName("helpEdit")
        self.verticalLayout.addWidget(self.helpEdit)
        self.buttonBox = QtWidgets.QDialogButtonBox(E5SimpleHelpDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(E5SimpleHelpDialog)
        self.buttonBox.accepted.connect(E5SimpleHelpDialog.accept)
        self.buttonBox.rejected.connect(E5SimpleHelpDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(E5SimpleHelpDialog)

    def retranslateUi(self, E5SimpleHelpDialog):
        pass

