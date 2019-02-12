# -*- coding: utf-8 -*-

# Copyright (c) 2002 - 2017 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to search for text in files.
"""

from __future__ import unicode_literals

import os
import re
import sys
import json
from collections import OrderedDict

from PyQt5.QtCore import pyqtSignal, Qt, pyqtSlot
from PyQt5.QtGui import QCursor, QFont
from PyQt5.QtWidgets import QDialog, QApplication, QMenu, QDialogButtonBox, \
    QTreeWidgetItem, QComboBox, QStyleFactory, QMdiSubWindow, QFileDialog, QMessageBox

from E5Gui.E5Application import e5App, E5Application
from E5Gui import E5MessageBox
from E5Gui.E5PathPicker import E5PathPickerModes

from subWindow import subForm

try:
    from Ui_FindFileDialog import Ui_FindFileDialog
except:
    from .Ui_FindFileDialog import Ui_FindFileDialog

import Utilities


# import Preferences


class FindFileDialog(QDialog, Ui_FindFileDialog):
    """
    Class implementing a dialog to search for text in files.
    
    The occurrences found are displayed in a QTreeWidget showing the filename,
    the linenumber and the found text. The file will be opened upon a double
    click onto the respective entry of the list.
    
    @signal sourceFile(str, int, str, int, int) emitted to open a source file
        at a line
    @signal designerFile(str) emitted to open a Qt-Designer file
    """
    sourceFile = pyqtSignal(str, int, str, int, int)
    designerFile = pyqtSignal(str)

    lineRole = Qt.UserRole + 1
    startRole = Qt.UserRole + 2
    endRole = Qt.UserRole + 3
    replaceRole = Qt.UserRole + 4
    md5Role = Qt.UserRole + 5

    def __init__(self, parent=None, replaceMode=True, ):
        """
        Constructor
        
        @param project reference to the project object
        @param replaceMode flag indicating the replace dialog mode (boolean)
        @param parent parent widget of this dialog (QWidget)
        """
        super(FindFileDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.Window)

        self.dirPicker.setMode(E5PathPickerModes.DirectoryMode)
        self.dirPicker.setInsertPolicy(QComboBox.InsertAtTop)
        self.dirPicker.setSizeAdjustPolicy(
            QComboBox.AdjustToMinimumContentsLength)

        self.__replaceMode = replaceMode

        self.importButton = \
            self.buttonBox.addButton(self.tr("&Import"),
                                     QDialogButtonBox.ActionRole)

        self.exportButton = \
            self.buttonBox.addButton(self.tr("&Export"),
                                     QDialogButtonBox.ActionRole)

        self.stopButton = \
            self.buttonBox.addButton(self.tr("Stop"),
                                     QDialogButtonBox.ActionRole)
        self.stopButton.setEnabled(False)

        self.transButton = \
            self.buttonBox.addButton(self.tr("TransForm"),
                                     QDialogButtonBox.ActionRole)
        self.findButton = \
            self.buttonBox.addButton(self.tr("Find"),
                                     QDialogButtonBox.ActionRole)
        self.findButton.setEnabled(False)
        self.findButton.setDefault(True)

        if self.__replaceMode:
            self.replaceButton.setEnabled(False)
            self.setWindowTitle(self.tr("Replace in Files"))
        else:
            self.replaceLabel.hide()
            self.replacetextCombo.hide()
            self.replaceButton.hide()

        self.findProgressLabel.setMaximumWidth(550)

        self.findList.headerItem().setText(self.findList.columnCount(), "")
        self.findList.header().setSortIndicator(0, Qt.AscendingOrder)
        self.__section0Size = self.findList.header().sectionSize(0)
        self.findList.setExpandsOnDoubleClick(False)

        if self.__replaceMode:
            font = QFont()
            # font = Preferences.getEditorOtherFonts("MonospacedFont")
            self.findList.setFont(font)

        self.__cancelSearch = False
        self.__lastFileItem = None
        self.__populating = False

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.__contextMenuRequested)

    def __createItem(self, file, line, text, start, end, replTxt="", md5=""):
        """
        Private method to create an entry in the file list.
        创建 Item
        @param file filename of file (string)
        @param line line number (integer)
        @param text text found (string)
        @param start start position of match (integer)
        @param end end position of match (integer)
        @param replTxt text with replacements applied (string)
        @keyparam md5 MD5 hash of the file (string)
        """
        if self.__lastFileItem is None:
            # It's a new file
            self.__lastFileItem = QTreeWidgetItem(self.findList, [file])
            self.__lastFileItem.setFirstColumnSpanned(True)
            self.__lastFileItem.setExpanded(True)
            if self.__replaceMode:
                self.__lastFileItem.setFlags(
                    self.__lastFileItem.flags() |
                    Qt.ItemFlags(Qt.ItemIsUserCheckable | Qt.ItemIsTristate))
                # Qt bug:
                # item is not user checkable if setFirstColumnSpanned
                # is True (< 4.5.0)
            self.__lastFileItem.setData(0, self.md5Role, md5)

        itm = QTreeWidgetItem(self.__lastFileItem)
        itm.setTextAlignment(0, Qt.AlignRight)
        itm.setData(0, Qt.DisplayRole, line)
        itm.setData(1, Qt.DisplayRole, text)
        itm.setData(0, self.lineRole, line)
        itm.setData(0, self.startRole, start)
        itm.setData(0, self.endRole, end)
        itm.setData(0, self.replaceRole, replTxt)
        if self.__replaceMode:
            itm.setFlags(itm.flags() | Qt.ItemFlags(Qt.ItemIsUserCheckable))
            itm.setCheckState(0, Qt.Checked)
            self.replaceButton.setEnabled(True)

    def show(self, txt=""):
        """
        Public method to enable/disable the project button.
        
        @param txt text to be shown in the searchtext combo (string)
        """

        if self.__replaceMode:
            self.findList.clear()

        super(FindFileDialog, self).show()

    def resizeEvent(self, e):
        self.mdiArea.tileSubWindows()
        return super().resizeEvent(e)

    def on_dirPicker_editTextChanged(self, text):
        """
        Private slot to handle the textChanged signal of the directory
        picker.
        
        @param text (ignored)
        """
        self.enableFindButton(False, False)

    def enableFindButton(self, sub=None, close=None):
        """
        Private slot called to enable the find button.
        """

        def closeBtn():
            self.findButton.setEnabled(False)
            self.buttonBox.button(QDialogButtonBox.Close).setDefault(True)

        def openBtn():
            self.findButton.setEnabled(True)
            self.findButton.setDefault(True)

        if self.dirPicker.currentText() == "":
            closeBtn()
        elif os.path.exists(os.path.abspath(self.dirPicker.currentText())) is False:
            closeBtn()
        elif sub is not None:
            if close is None:
                if sub.findtextCombo.currentText() == "" or (sub.filterEdit.text() == "") \
                        or (self.__replaceMode is False and sub.replacetextCombo.currentText() == ""):
                    closeBtn()
                else:
                    openBtn()
            elif close is True:
                subList = self.mdiArea.subWindowList()
                for sub_ in subList:
                    sub__ = sub_.widget()

                    if sub__ != sub:
                        if sub__.findtextCombo.currentText() == "" or (sub__.filterEdit.text() == ""):
                            closeBtn()
                            break
                        else:
                            openBtn()
                    else:
                        if len(subList) == 1:
                            closeBtn()
            elif close is False:

                for sub_ in self.mdiArea.subWindowList():
                    sub__ = sub_.widget()

                    if sub__.findtextCombo.currentText() == "" or (sub__.filterEdit.text() == ""):
                        closeBtn()
                        break
                    else:
                        openBtn()
        else:
            openBtn()

    def on_buttonBox_clicked(self, button):
        """
        Private slot called by a button of the button box clicked.
        
        @param button button that was clicked (QAbstractButton)
        """
        if button == self.findButton:
            self.findList.clear()
            self.__doSearch()
        elif button == self.stopButton:
            self.__stopSearch()
        elif button == self.importButton:
            self.clear_btn.click()
            fileName, ok = QFileDialog.getOpenFileName(self, "Open", "history.json", "Json (*.json)")
            if fileName == '':
                return
            else:
                self.loadFromFile(fileName)
        elif button == self.exportButton:
            fileName, ok = QFileDialog.getSaveFileName(self, "Save", "history.json", "Json (*.json)")
            if fileName == '':
                return
            else:
                self.saveToFile(fileName)
        elif button == self.transButton:
            for sub in self.mdiArea.subWindowList():
                sub = sub.widget()
                a, b = sub.findtextCombo.currentText(), sub.replacetextCombo.currentText()
                sub.findtextCombo.setCurrentText(b), sub.replacetextCombo.setCurrentText(a)

    def __stripEol(self, txt):
        """
        Private method to strip the eol part.
        
        @param txt line of text that should be treated (string)
        @return text with eol stripped (string)
        """
        return txt.replace("\r", "").replace("\n", "")

    def __stopSearch(self):
        """
        Private slot to handle the stop button being pressed.
        """

        self.__cancelSearch = True

    def __doSearch(self):
        """
        Private slot to handle the find button being pressed.
        搜索逻辑
        """
        # if self.__replaceMode and \
        #    not e5App().getObject("ViewManager").checkAllDirty():
        #     return

        self.__cancelSearch = False

        for sub in self.mdiArea.subWindowList():
            sub = sub.widget()
            fileFilter = sub.filterEdit.text()
            fileFilterList = \
                ["^{0}$".format(filter.replace(".", "\.").replace("*", ".*"))
                 for filter in fileFilter.split(";")]
            # *.qml -> .*\.qml
            filterRe = re.compile("|".join(fileFilterList))

            # 开始查找
            files = self.__getFileList(
                os.path.abspath(self.dirPicker.currentText()),
                filterRe)

            QApplication.processEvents()
            QApplication.processEvents()
            self.findProgress.setMaximum(len(files))

            # retrieve the values
            reg = sub.regexpCheckBox.isChecked()
            wo = sub.wordCheckBox.isChecked()
            cs = sub.caseCheckBox.isChecked()
            ct = sub.findtextCombo.currentText()
            if reg:
                txt = ct
            else:
                txt = re.escape(ct)
            if wo:
                txt = "\\b{0}\\b".format(txt)
            if sys.version_info[0] == 2:
                flags = re.UNICODE | re.LOCALE
            else:
                flags = re.UNICODE
            if not cs:
                flags |= re.IGNORECASE
            try:
                search = re.compile(txt, flags)
            except re.error as why:
                E5MessageBox.critical(
                    self,
                    self.tr("Invalid search expression"),
                    self.tr("""<p>The search expression is not valid.</p>"""
                            """<p>Error: {0}</p>""").format(str(why)))
                self.stopButton.setEnabled(False)
                self.findButton.setEnabled(True)
                self.findButton.setDefault(True)
                return

            if self.__replaceMode:
                replTxt = sub.replacetextCombo.currentText()

        # ======================================================
            # set the button states
            self.stopButton.setEnabled(True)
            self.stopButton.setDefault(True)
            self.findButton.setEnabled(False)

            # now go through all the files
            self.__populating = True
            self.findList.setUpdatesEnabled(False)
            progress = 0
            breakSearch = False
            occurrences = 0
            fileOccurrences = 0

            for file in files:
                self.__lastFileItem = None
                found = False
                if self.__cancelSearch or breakSearch:
                    break

                self.findProgressLabel.setPath(file)

                fn = file

                # read the file and split it into textlines
                try:
                    text, encoding, hashStr = Utilities.readEncodedFileWithHash(fn)
                    lines = text.splitlines(True)
                except (UnicodeError, IOError):
                    progress += 1
                    self.findProgress.setValue(progress)
                    continue

                # now perform the search and display the lines found
                count = 0
                for line in lines:
                    if self.__cancelSearch:
                        break

                    count += 1
                    contains = search.search(line)
                    if contains:
                        occurrences += 1
                        found = True
                        start = contains.start()
                        end = contains.end()
                        if self.__replaceMode:
                            rline = search.sub(replTxt, line)
                        else:
                            rline = ""
                        line = self.__stripEol(line)
                        if len(line) > 1024:
                            line = "{0} ...".format(line[:1024])
                        if self.__replaceMode:
                            if len(rline) > 1024:
                                rline = "{0} ...".format(line[:1024])
                            line = "- {0}\n+ {1}".format(
                                line, self.__stripEol(rline))
                        self.__createItem(file, count, line, start, end,
                                          rline, hashStr)

                    QApplication.processEvents()

                if found:
                    fileOccurrences += 1
                progress += 1
                self.findProgress.setValue(progress)

            if not files:
                self.findProgress.setMaximum(1)
                self.findProgress.setValue(1)

            resultFormat = self.tr("{0} / {1}", "occurrences / files")
            self.findProgressLabel.setPath(resultFormat.format(
                self.tr("%n occurrence(s)", "", occurrences),
                self.tr("%n file(s)", "", fileOccurrences)))

            self.findList.setUpdatesEnabled(True)
            self.findList.sortItems(self.findList.sortColumn(),
                                    self.findList.header().sortIndicatorOrder())
            self.findList.resizeColumnToContents(1)
            if self.__replaceMode:
                self.findList.header().resizeSection(0, self.__section0Size + 30)
            self.findList.header().setStretchLastSection(True)
            self.__populating = False

            self.stopButton.setEnabled(False)
            self.findButton.setEnabled(True)
            self.findButton.setDefault(True)

            if breakSearch:
                self.close()

    def __getFileList(self, path, filterRe):
        """
        Private method to get a list of files to search.
        
        @param path the root directory to search in (string)
        @param filterRe regular expression defining the filter
            criteria (regexp object)
        @return list of files to be processed (list of strings)
        """
        path = os.path.abspath(path)
        files = []
        for dirname, _, names in os.walk(path):
            files.extend([os.path.join(dirname, f)
                          for f in names
                          if re.match(filterRe, f)]
                         )
        return files

    def setOpenFiles(self):
        """
        Public slot to set the mode to search in open files.
        """
        self.openFilesButton.setChecked(True)

    @pyqtSlot()
    def on_replaceButton_clicked(self):
        """
        Private slot to perform the requested replace actions.
        替换开始
        """
        self.findProgress.setMaximum(self.findList.topLevelItemCount())
        self.findProgress.setValue(0)

        progress = 0
        for index in range(self.findList.topLevelItemCount()):
            itm = self.findList.topLevelItem(index)
            if itm.checkState(0) in [Qt.PartiallyChecked, Qt.Checked]:
                file = itm.text(0)
                origHash = itm.data(0, self.md5Role)

                self.findProgressLabel.setPath(file)

                fn = file

                # read the file and split it into textlines
                try:
                    text, encoding, hashStr = \
                        Utilities.readEncodedFileWithHash(fn)
                    lines = text.splitlines(True)
                except (UnicodeError, IOError) as err:
                    E5MessageBox.critical(
                        self,
                        self.tr("Replace in Files"),
                        self.tr(
                            """<p>Could not read the file <b>{0}</b>."""
                            """ Skipping it.</p><p>Reason: {1}</p>""")
                            .format(fn, str(err))
                    )
                    progress += 1
                    self.findProgress.setValue(progress)
                    continue

                # Check the original and the current hash. Skip the file,
                # if hashes are different.
                if origHash != hashStr:
                    E5MessageBox.critical(
                        self,
                        self.tr("Replace in Files"),
                        self.tr(
                            """<p>The current and the original hash of the"""
                            """ file <b>{0}</b> are different. Skipping it."""
                            """</p><p>Hash 1: {1}</p><p>Hash 2: {2}</p>""")
                            .format(fn, origHash, hashStr)
                    )
                    progress += 1
                    self.findProgress.setValue(progress)
                    continue

                # replace the lines authorized by the user
                for cindex in range(itm.childCount()):
                    citm = itm.child(cindex)
                    if citm.checkState(0) == Qt.Checked:
                        line = citm.data(0, self.lineRole)
                        rline = citm.data(0, self.replaceRole)
                        lines[line - 1] = rline

                # write the file
                # 写入
                txt = "".join(lines)
                try:
                    Utilities.writeEncodedFile(fn, txt, encoding)
                except (IOError, Utilities.CodingError, UnicodeError) as err:
                    E5MessageBox.critical(
                        self,
                        self.tr("Replace in Files"),
                        self.tr(
                            """<p>Could not save the file <b>{0}</b>."""
                            """ Skipping it.</p><p>Reason: {1}</p>""")
                            .format(fn, str(err))
                    )

            progress += 1
            self.findProgress.setValue(progress)

        self.findProgressLabel.setPath("")

        # 替换完成
        self.findList.clear()
        self.replaceButton.setEnabled(False)
        self.findButton.setEnabled(True)
        self.findButton.setDefault(True)

    def __contextMenuRequested(self, pos):
        """
        Private slot to handle the context menu request.
        
        @param pos position the context menu shall be shown (QPoint)
        """
        menu = QMenu(self)

        menu.addAction(self.tr("Copy Path to Clipboard"),
                       self.__copyToClipboard)

        menu.exec_(QCursor.pos())

    def __copyToClipboard(self):
        """
        Private method to copy the path of an entry to the clipboard.
        """
        itm = self.findList.selectedItems()[0]
        if itm.parent():
            fn = itm.parent().text(0)
        else:
            fn = itm.text(0)

        cb = QApplication.clipboard()
        cb.setText(fn)

    # =================================
    @pyqtSlot()
    def on_add_btn_clicked(self):
        """
        add form.
        """

        sub = subForm(self)
        self.mdiArea.addSubWindow(sub)
        sub.show()
        self.mdiArea.tileSubWindows()

    @pyqtSlot()
    def on_clear_btn_clicked(self):
        """
        Slot documentation goes here.
        """
        for i in self.mdiArea.subWindowList():
            self.mdiArea.removeSubWindow(i)

    # =================================
    def saveToFile(self, filename):
        try:
            with open(filename, "w") as file:
                file.write(json.dumps(self.serialize(), indent=4))
                print("saving to", filename, "was successfull.")

                self.has_been_modified = False
        except:

            QMessageBox.warning(self, "error", "save json fail", QMessageBox.Ok)

    def loadFromFile(self, filename):
        try:
            with open(filename, "r") as file:
                raw_data = file.read()
                data = json.loads(raw_data, encoding='utf-8')
                self.deserialize(data)
        except:
            QMessageBox.warning(self, "error", "open json fail", QMessageBox.Ok)

    def serialize(self):
        """ÐòÁÐ»¯"""
        subs = []
        for sub in self.mdiArea.subWindowList():
            subs.append(sub.widget().serialize())

        return OrderedDict([
            ('subs', subs),
            ('path', self.dirPicker.path()),
        ])

    def deserialize(self, data, hashmap={}, restore_id=True):
        """·´ÐòÁÐ»¯"""

        self.clear_btn.click()

        for sub_info in data['subs']:
            sub = subForm(self).deserialize(sub_info)
            self.mdiArea.addSubWindow(sub)
            sub.show()
        self.mdiArea.tileSubWindows()

        self.dirPicker.setPath(data['path'])

        self.enableFindButton(False, False)
        return True


if __name__ == "__main__":
    app = E5Application(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    ui = FindFileDialog()
    ui.show()
    sys.exit(app.exec_())
