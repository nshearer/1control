# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'N:\HR-ITS4-Documents\Projects\Active Projects\20 - Development\OneControl\src\onectl\ui\qt\ServerWindowQt.ui'
#
# Created: Tue Mar 03 18:36:00 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ServerWindow(object):
    def setupUi(self, ServerWindow):
        ServerWindow.setObjectName("ServerWindow")
        ServerWindow.resize(270, 318)
        self.centralwidget = QtGui.QWidget(ServerWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.browser = QtGui.QTextBrowser(self.centralwidget)
        self.browser.setObjectName("browser")
        self.gridLayout.addWidget(self.browser, 0, 0, 1, 1)
        self.lineedit = QtGui.QLineEdit(self.centralwidget)
        self.lineedit.setObjectName("lineedit")
        self.gridLayout.addWidget(self.lineedit, 1, 0, 1, 1)
        ServerWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(ServerWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 270, 21))
        self.menubar.setObjectName("menubar")
        ServerWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(ServerWindow)
        self.statusbar.setObjectName("statusbar")
        ServerWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ServerWindow)
        QtCore.QMetaObject.connectSlotsByName(ServerWindow)

    def retranslateUi(self, ServerWindow):
        ServerWindow.setWindowTitle(QtGui.QApplication.translate("ServerWindow", "1 Control", None, QtGui.QApplication.UnicodeUTF8))
        self.lineedit.setText(QtGui.QApplication.translate("ServerWindow", "Type something and hit enter", None, QtGui.QApplication.UnicodeUTF8))

