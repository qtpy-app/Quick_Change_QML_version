# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\E5Gui\E5ZoomWidget.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_E5ZoomWidget(object):
    def setupUi(self, E5ZoomWidget):
        E5ZoomWidget.setObjectName("E5ZoomWidget")
        E5ZoomWidget.resize(242, 21)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(E5ZoomWidget.sizePolicy().hasHeightForWidth())
        E5ZoomWidget.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtWidgets.QHBoxLayout(E5ZoomWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.valueLabel = QtWidgets.QLabel(E5ZoomWidget)
        self.valueLabel.setMinimumSize(QtCore.QSize(0, 16))
        self.valueLabel.setMaximumSize(QtCore.QSize(16777215, 16))
        self.valueLabel.setText("0")
        self.valueLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.valueLabel.setObjectName("valueLabel")
        self.horizontalLayout.addWidget(self.valueLabel)
        self.zoomOutLabel = E5ClickableLabel(E5ZoomWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zoomOutLabel.sizePolicy().hasHeightForWidth())
        self.zoomOutLabel.setSizePolicy(sizePolicy)
        self.zoomOutLabel.setMinimumSize(QtCore.QSize(16, 16))
        self.zoomOutLabel.setMaximumSize(QtCore.QSize(16, 16))
        self.zoomOutLabel.setObjectName("zoomOutLabel")
        self.horizontalLayout.addWidget(self.zoomOutLabel)
        self.slider = QtWidgets.QSlider(E5ZoomWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.slider.sizePolicy().hasHeightForWidth())
        self.slider.setSizePolicy(sizePolicy)
        self.slider.setMinimumSize(QtCore.QSize(160, 16))
        self.slider.setMaximumSize(QtCore.QSize(160, 16))
        self.slider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.slider.setMinimum(-10)
        self.slider.setMaximum(20)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.slider.setObjectName("slider")
        self.horizontalLayout.addWidget(self.slider)
        self.zoomInLabel = E5ClickableLabel(E5ZoomWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zoomInLabel.sizePolicy().hasHeightForWidth())
        self.zoomInLabel.setSizePolicy(sizePolicy)
        self.zoomInLabel.setMinimumSize(QtCore.QSize(16, 16))
        self.zoomInLabel.setMaximumSize(QtCore.QSize(16, 16))
        self.zoomInLabel.setObjectName("zoomInLabel")
        self.horizontalLayout.addWidget(self.zoomInLabel)
        self.zoomResetLabel = E5ClickableLabel(E5ZoomWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zoomResetLabel.sizePolicy().hasHeightForWidth())
        self.zoomResetLabel.setSizePolicy(sizePolicy)
        self.zoomResetLabel.setMinimumSize(QtCore.QSize(16, 16))
        self.zoomResetLabel.setMaximumSize(QtCore.QSize(16, 16))
        self.zoomResetLabel.setObjectName("zoomResetLabel")
        self.horizontalLayout.addWidget(self.zoomResetLabel)

        self.retranslateUi(E5ZoomWidget)
        QtCore.QMetaObject.connectSlotsByName(E5ZoomWidget)

    def retranslateUi(self, E5ZoomWidget):
        _translate = QtCore.QCoreApplication.translate
        self.zoomOutLabel.setToolTip(_translate("E5ZoomWidget", "Zoom out"))
        self.slider.setToolTip(_translate("E5ZoomWidget", "Drag to zoom"))
        self.zoomInLabel.setToolTip(_translate("E5ZoomWidget", "Zoom in"))
        self.zoomResetLabel.setToolTip(_translate("E5ZoomWidget", "Zoom reset"))

from E5Gui.E5ClickableLabel import E5ClickableLabel
