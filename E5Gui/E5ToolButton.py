# -*- coding: utf-8 -*-

# Copyright (c) 2017 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a specialized tool button subclass.
"""

from __future__ import unicode_literals

from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt, QTimer, QSize
from PyQt5.QtWidgets import QToolButton, QStyle, QStyleOptionToolButton, \
    QStyleOption, QApplication


class E5ToolButton(QToolButton):
    """
    Class implementing a specialized tool button subclass.
    
    @signal aboutToShowMenu() emitted before the tool button menu is shown
    @signal aboutToHideMenu() emitted before the tool button menu is hidden
    @signal middleClicked() emitted when the middle mouse button was clicked
    @signal controlClicked() emitted when the left mouse button was
        clicked while pressing the Ctrl key
    @signal doubleClicked() emitted when the left mouse button was
        double clicked
    """
    NoOptions = 0
    ShowMenuInsideOption = 1
    ToolBarLookOption = 2
    
    aboutToShowMenu = pyqtSignal()
    aboutToHideMenu = pyqtSignal()
    middleClicked = pyqtSignal()
    controlClicked = pyqtSignal()
    doubleClicked = pyqtSignal()
    
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(E5ToolButton, self).__init__(parent)
        
        self.setMinimumWidth(16)
        
        self.__menu = None
        self.__options = E5ToolButton.NoOptions
        
        opt = QStyleOptionToolButton()
        self.initStyleOption(opt)
        
        self.__pressTimer = QTimer()
        self.__pressTimer.setSingleShot(True)
        self.__pressTimer.setInterval(
            QApplication.style().styleHint(
                QStyle.SH_ToolButton_PopupDelay, opt, self))
        self.__pressTimer.timeout.connect(self.__showMenu)
    
    ##################################################################
    ## Menu handling methods below.
    ##
    ## The menu is handled in E5ToolButton and is not passed to
    ## QToolButton. No menu indicator will be shown in the button.
    ##################################################################
    
    def menu(self):
        """
        Public method to get a reference to the tool button menu.
        
        @return reference to the tool button menu
        @rtype QMenu
        """
        return self.__menu
    
    def setMenu(self, menu):
        """
        Public method to set the tool button menu.
        
        @param menu reference to the tool button menu
        @type QMenu
        """
        assert menu is not None
        
        if self.__menu:
            self.__menu.aboutToHide.disconnect(self.__menuAboutToHide)
        
        self.__menu = menu
        self.__menu.aboutToHide.connect(self.__menuAboutToHide)
    
    def showMenuInside(self):
        """
        Public method to check, if the menu edge shall be aligned with
        the button.
        
        @return flag indicating that the menu edge shall be aligned
        @rtype bool
        """
        return bool(self.__options & E5ToolButton.ShowMenuInsideOption)
    
    def setShowMenuInside(self, enable):
        """
        Public method to set a flag to show the menu edge aligned with
        the button.
        
        @param enable flag indicating to align the menu edge to the button
        @type bool
        """
        if enable:
            self.__options |= E5ToolButton.ShowMenuInsideOption
        else:
            self.__options &= ~E5ToolButton.ShowMenuInsideOption
    
    @pyqtSlot()
    def __showMenu(self):
        """
        Private slot to show the tool button menu.
        """
        if self.__menu is None or self.__menu.isVisible():
            return
        
        self.aboutToShowMenu.emit()
        
        if self.__options & E5ToolButton.ShowMenuInsideOption:
            pos = self.mapToGlobal(self.rect().bottomRight())
            if QApplication.layoutDirection() == Qt.RightToLeft:
                pos.setX(pos.x() - self.rect().width())
            else:
                pos.setX(pos.x() - self.__menu.sizeHint().width())
        else:
            pos = self.mapToGlobal(self.rect().bottomLeft())
        
        self.__menu.popup(pos)
    
    @pyqtSlot()
    def __menuAboutToHide(self):
        """
        Private slot to handle the tool button menu about to be hidden.
        """
        self.setDown(False)
        self.aboutToHideMenu.emit()
    
    ##################################################################
    ## Methods to handle the tool button look
    ##################################################################
    
    def toolbarButtonLook(self):
        """
        Public method to check, if the button has the toolbar look.
        
        @return flag indicating toolbar look
        @rtype bool
        """
        return bool(self.__options & E5ToolButton.ToolBarLookOption)
    
    def setToolbarButtonLook(self, enable):
        """
        Public method to set the toolbar look state.
        
        @param enable flag indicating toolbar look
        @type bool
        """
        if enable:
            self.__options |= E5ToolButton.ToolBarLookOption
            
            opt = QStyleOption()
            opt.initFrom(self)
            size = self.style().pixelMetric(
                QStyle.PM_ToolBarIconSize, opt, self)
            self.setIconSize(QSize(size, size))
        else:
            self.__options &= ~E5ToolButton.ToolBarLookOption
        
        self.setProperty("toolbar-look", enable)
        self.style().unpolish(self)
        self.style().polish(self)
    
    ##################################################################
    ## Methods to handle some event types
    ##################################################################
    
    def mousePressEvent(self, evt):
        """
        Protected method to handle mouse press events.
        
        @param evt reference to the mouse event
        @type QMouseEvent
        """
        if self.popupMode() == QToolButton.DelayedPopup:
            self.__pressTimer.start()
        
        if evt.buttons() == Qt.LeftButton and \
           self.__menu is not None and \
           self.popupMode() == QToolButton.InstantPopup:
            self.setDown(True)
            self.__showMenu()
        elif evt.buttons() == Qt.RightButton and \
                self.__menu is not None:
            self.setDown(True)
            self.__showMenu()
        else:
            super(E5ToolButton, self).mousePressEvent(evt)
    
    def mouseReleaseEvent(self, evt):
        """
        Protected method to handle mouse release events.
        
        @param evt reference to the mouse event
        @type QMouseEvent
        """
        self.__pressTimer.stop()
        
        if evt.button() == Qt.MiddleButton and \
           self.rect().contains(evt.pos()):
            self.middleClicked.emit()
            self.setDown(False)
        elif evt.button() == Qt.LeftButton and \
            self.rect().contains(evt.pos()) and \
                evt.modifiers() == Qt.ControlModifier:
            self.controlClicked.emit()
            self.setDown(False)
        else:
            super(E5ToolButton, self).mouseReleaseEvent(evt)
    
    def mouseDoubleClickEvent(self, evt):
        """
        Protected method to handle mouse double click events.
        
        @param evt reference to the mouse event
        @type QMouseEvent
        """
        super(E5ToolButton, self).mouseDoubleClickEvent(evt)
        
        self.__pressTimer.stop()
        
        if evt.buttons() == Qt.LeftButton:
            self.doubleClicked.emit()
    
    def contextMenuEvent(self, evt):
        """
        Protected method to handle context menu events.
        
        @param evt reference to the context menu event
        @type QContextMenuEvent
        """
        # block to prevent showing the context menu and the tool button menu
        if self.__menu is not None:
            return
        
        super(E5ToolButton, self).contextMenuEvent(evt)
