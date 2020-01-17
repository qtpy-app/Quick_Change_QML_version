# -*- coding: utf-8 -*-

# Copyright (c) 2002 - 2017 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to search for text in files.
"""

from __future__ import unicode_literals

# -*- mode: python -*-

import sys

from PyQt5.QtWidgets import QStyleFactory

from E5Gui.E5Application import e5App, E5Application
from FindFileDialog import FindFileDialog


if __name__ == "__main__":
    app = E5Application(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    ui = FindFileDialog()
    ui.show()
    sys.exit(app.exec_())
