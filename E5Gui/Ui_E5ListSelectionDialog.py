# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\E5Gui\E5ListSelectionDialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_E5ListSelectionDialog(object):
    def setupUi(self, E5ListSelectionDialog):
        E5ListSelectionDialog.setObjectName("E5ListSelectionDialog")
        E5ListSelectionDialog.resize(400, 500)
        E5ListSelectionDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(E5ListSelectionDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.messageLabel = QtWidgets.QLabel(E5ListSelectionDialog)
        self.messageLabel.setWordWrap(True)
        self.messageLabel.setObjectName("messageLabel")
        self.verticalLayout.addWidget(self.messageLabel)
        self.selectionList = QtWidgets.QListWidget(E5ListSelectionDialog)
        self.selectionList.setAlternatingRowColors(True)
        self.selectionList.setObjectName("selectionList")
        self.verticalLayout.addWidget(self.selectionList)
        self.buttonBox = QtWidgets.QDialogButtonBox(E5ListSelectionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(E5ListSelectionDialog)
        self.buttonBox.accepted.connect(E5ListSelectionDialog.accept)
        self.buttonBox.rejected.connect(E5ListSelectionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(E5ListSelectionDialog)

    def retranslateUi(self, E5ListSelectionDialog):
        _translate = QtCore.QCoreApplication.translate
        E5ListSelectionDialog.setWindowTitle(_translate("E5ListSelectionDialog", "Select from List"))
        self.messageLabel.setText(_translate("E5ListSelectionDialog", "Select from the list below:"))

