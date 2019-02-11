# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\E5Gui\E5StringListEditWidget.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_E5StringListEditWidget(object):
    def setupUi(self, E5StringListEditWidget):
        E5StringListEditWidget.setObjectName("E5StringListEditWidget")
        E5StringListEditWidget.resize(500, 300)
        E5StringListEditWidget.setWindowTitle("")
        self.verticalLayout = QtWidgets.QVBoxLayout(E5StringListEditWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setHorizontalSpacing(0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.searchEdit = E5ClearableLineEdit(E5StringListEditWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchEdit.sizePolicy().hasHeightForWidth())
        self.searchEdit.setSizePolicy(sizePolicy)
        self.searchEdit.setMinimumSize(QtCore.QSize(300, 0))
        self.searchEdit.setObjectName("searchEdit")
        self.gridLayout_4.addWidget(self.searchEdit, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_4)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.stringList = E5ListView(E5StringListEditWidget)
        self.stringList.setAlternatingRowColors(True)
        self.stringList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.stringList.setObjectName("stringList")
        self.gridLayout.addWidget(self.stringList, 0, 0, 6, 1)
        self.addButton = QtWidgets.QPushButton(E5StringListEditWidget)
        self.addButton.setAutoDefault(False)
        self.addButton.setObjectName("addButton")
        self.gridLayout.addWidget(self.addButton, 0, 1, 1, 1)
        self.line_3 = QtWidgets.QFrame(E5StringListEditWidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 1, 1, 1, 1)
        self.removeButton = QtWidgets.QPushButton(E5StringListEditWidget)
        self.removeButton.setAutoDefault(False)
        self.removeButton.setObjectName("removeButton")
        self.gridLayout.addWidget(self.removeButton, 2, 1, 1, 1)
        self.removeAllButton = QtWidgets.QPushButton(E5StringListEditWidget)
        self.removeAllButton.setAutoDefault(False)
        self.removeAllButton.setObjectName("removeAllButton")
        self.gridLayout.addWidget(self.removeAllButton, 3, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 4, 1, 1, 1)
        self.defaultButton = QtWidgets.QPushButton(E5StringListEditWidget)
        self.defaultButton.setObjectName("defaultButton")
        self.gridLayout.addWidget(self.defaultButton, 5, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(E5StringListEditWidget)
        QtCore.QMetaObject.connectSlotsByName(E5StringListEditWidget)
        E5StringListEditWidget.setTabOrder(self.stringList, self.searchEdit)
        E5StringListEditWidget.setTabOrder(self.searchEdit, self.addButton)
        E5StringListEditWidget.setTabOrder(self.addButton, self.removeButton)
        E5StringListEditWidget.setTabOrder(self.removeButton, self.removeAllButton)
        E5StringListEditWidget.setTabOrder(self.removeAllButton, self.defaultButton)

    def retranslateUi(self, E5StringListEditWidget):
        _translate = QtCore.QCoreApplication.translate
        self.searchEdit.setToolTip(_translate("E5StringListEditWidget", "Enter search term for strings"))
        self.addButton.setToolTip(_translate("E5StringListEditWidget", "Press to add an entry"))
        self.addButton.setText(_translate("E5StringListEditWidget", "&Add..."))
        self.removeButton.setToolTip(_translate("E5StringListEditWidget", "Press to remove the selected entries"))
        self.removeButton.setText(_translate("E5StringListEditWidget", "&Remove"))
        self.removeAllButton.setToolTip(_translate("E5StringListEditWidget", "Press to remove all entries"))
        self.removeAllButton.setText(_translate("E5StringListEditWidget", "R&emove All"))
        self.defaultButton.setToolTip(_translate("E5StringListEditWidget", "Press to set the default list of values"))
        self.defaultButton.setText(_translate("E5StringListEditWidget", "&Default"))

from E5Gui.E5LineEdit import E5ClearableLineEdit
from E5Gui.E5ListView import E5ListView
