# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FindFileDialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FindFileDialog(object):
    def setupUi(self, FindFileDialog):
        FindFileDialog.setObjectName("FindFileDialog")
        FindFileDialog.resize(600, 604)
        self.gridLayout_2 = QtWidgets.QGridLayout(FindFileDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.buttonBox = QtWidgets.QDialogButtonBox(FindFileDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 7, 0, 1, 1)
        self.replaceButton = QtWidgets.QPushButton(FindFileDialog)
        self.replaceButton.setObjectName("replaceButton")
        self.gridLayout_2.addWidget(self.replaceButton, 6, 0, 1, 1)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.add_btn = QtWidgets.QPushButton(FindFileDialog)
        self.add_btn.setObjectName("add_btn")
        self.horizontalLayout_12.addWidget(self.add_btn)
        self.dirButton = QtWidgets.QRadioButton(FindFileDialog)
        self.dirButton.setChecked(True)
        self.dirButton.setObjectName("dirButton")
        self.horizontalLayout_12.addWidget(self.dirButton)
        self.dirPicker = E5ComboPathPicker(FindFileDialog)
        self.dirPicker.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dirPicker.sizePolicy().hasHeightForWidth())
        self.dirPicker.setSizePolicy(sizePolicy)
        self.dirPicker.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.dirPicker.setObjectName("dirPicker")
        self.horizontalLayout_12.addWidget(self.dirPicker)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem)
        self.clear_btn = QtWidgets.QPushButton(FindFileDialog)
        self.clear_btn.setObjectName("clear_btn")
        self.horizontalLayout_12.addWidget(self.clear_btn)
        self.gridLayout_2.addLayout(self.horizontalLayout_12, 0, 0, 1, 1)
        self.mdiArea = QtWidgets.QMdiArea(FindFileDialog)
        self.mdiArea.setObjectName("mdiArea")
        self.gridLayout_2.addWidget(self.mdiArea, 1, 0, 1, 1)
        self.findList = QtWidgets.QTreeWidget(FindFileDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.findList.sizePolicy().hasHeightForWidth())
        self.findList.setSizePolicy(sizePolicy)
        self.findList.setMinimumSize(QtCore.QSize(0, 150))
        self.findList.setAlternatingRowColors(True)
        self.findList.setColumnCount(2)
        self.findList.setObjectName("findList")
        self.gridLayout_2.addWidget(self.findList, 5, 0, 1, 1)
        self.findProgress = QtWidgets.QProgressBar(FindFileDialog)
        self.findProgress.setProperty("value", 0)
        self.findProgress.setOrientation(QtCore.Qt.Horizontal)
        self.findProgress.setObjectName("findProgress")
        self.gridLayout_2.addWidget(self.findProgress, 4, 0, 1, 1)
        self.findProgressLabel = E5SqueezeLabelPath(FindFileDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.findProgressLabel.sizePolicy().hasHeightForWidth())
        self.findProgressLabel.setSizePolicy(sizePolicy)
        self.findProgressLabel.setText("")
        self.findProgressLabel.setObjectName("findProgressLabel")
        self.gridLayout_2.addWidget(self.findProgressLabel, 3, 0, 1, 1)

        self.retranslateUi(FindFileDialog)
        self.buttonBox.rejected.connect(FindFileDialog.close)
        self.dirButton.toggled['bool'].connect(self.dirPicker.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(FindFileDialog)
        FindFileDialog.setTabOrder(self.findList, self.replaceButton)

    def retranslateUi(self, FindFileDialog):
        _translate = QtCore.QCoreApplication.translate
        FindFileDialog.setWindowTitle(_translate("FindFileDialog", "Find in Files"))
        self.replaceButton.setToolTip(_translate("FindFileDialog", "Press to apply the selected replacements"))
        self.replaceButton.setText(_translate("FindFileDialog", "Replace"))
        self.add_btn.setText(_translate("FindFileDialog", "Add"))
        self.dirButton.setToolTip(_translate("FindFileDialog", "Search in files of a directory tree to be entered below"))
        self.dirButton.setText(_translate("FindFileDialog", "Find in \n"
"Directory tree"))
        self.dirPicker.setToolTip(_translate("FindFileDialog", "Enter the directory to search in"))
        self.clear_btn.setText(_translate("FindFileDialog", "Clear"))
        self.findList.setSortingEnabled(True)
        self.findList.headerItem().setText(0, _translate("FindFileDialog", "File/Line"))
        self.findList.headerItem().setText(1, _translate("FindFileDialog", "Text"))
        self.findProgress.setToolTip(_translate("FindFileDialog", "Shows the progress of the search action"))
        self.findProgress.setFormat(_translate("FindFileDialog", "%v/%m Files"))

from E5Gui.E5PathPicker import E5ComboPathPicker
from E5Gui.E5SqueezeLabels import E5SqueezeLabelPath
