# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\E5Gui\E5ErrorMessageFilterDialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_E5ErrorMessageFilterDialog(object):
    def setupUi(self, E5ErrorMessageFilterDialog):
        E5ErrorMessageFilterDialog.setObjectName("E5ErrorMessageFilterDialog")
        E5ErrorMessageFilterDialog.resize(500, 350)
        E5ErrorMessageFilterDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(E5ErrorMessageFilterDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.filtersEditWidget = E5StringListEditWidget(E5ErrorMessageFilterDialog)
        self.filtersEditWidget.setObjectName("filtersEditWidget")
        self.verticalLayout.addWidget(self.filtersEditWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(E5ErrorMessageFilterDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(E5ErrorMessageFilterDialog)
        self.buttonBox.accepted.connect(E5ErrorMessageFilterDialog.accept)
        self.buttonBox.rejected.connect(E5ErrorMessageFilterDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(E5ErrorMessageFilterDialog)

    def retranslateUi(self, E5ErrorMessageFilterDialog):
        _translate = QtCore.QCoreApplication.translate
        E5ErrorMessageFilterDialog.setWindowTitle(_translate("E5ErrorMessageFilterDialog", "Error Messages Filter"))

from E5Gui.E5StringListEditWidget import E5StringListEditWidget
