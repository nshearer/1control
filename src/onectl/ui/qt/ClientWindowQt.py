# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'N:\HR-ITS4-Documents\Projects\Active Projects\20 - Development\OneControl\src\onectl\ui\qt\ClientWindowQt.ui'
#
# Created: Wed Mar 04 12:27:09 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ServerWindow(object):
    def setupUi(self, ServerWindow):
        ServerWindow.setObjectName("ServerWindow")
        ServerWindow.resize(293, 142)
        self.centralwidget = QtGui.QWidget(ServerWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 5, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 1, 1, 1)
        self.ip_address = QtGui.QLineEdit(self.centralwidget)
        self.ip_address.setEnabled(False)
        self.ip_address.setObjectName("ip_address")
        self.gridLayout.addWidget(self.ip_address, 2, 2, 1, 1)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 1, 1, 1)
        self.vmix_client_status = QtGui.QLabel(self.centralwidget)
        self.vmix_client_status.setObjectName("vmix_client_status")
        self.gridLayout.addWidget(self.vmix_client_status, 5, 2, 1, 1)
        self.pp_client_status = QtGui.QLabel(self.centralwidget)
        self.pp_client_status.setObjectName("pp_client_status")
        self.gridLayout.addWidget(self.pp_client_status, 4, 2, 1, 1)
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 1, 1, 1)
        ServerWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(ServerWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 293, 21))
        self.menubar.setObjectName("menubar")
        ServerWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(ServerWindow)
        self.statusbar.setObjectName("statusbar")
        ServerWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ServerWindow)
        QtCore.QMetaObject.connectSlotsByName(ServerWindow)

    def retranslateUi(self, ServerWindow):
        ServerWindow.setWindowTitle(QtGui.QApplication.translate("ServerWindow", "1 Control", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("ServerWindow", "vMix PC", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ServerWindow", "PowerPoint PC", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ServerWindow", "IP Address", None, QtGui.QApplication.UnicodeUTF8))
        self.vmix_client_status.setText(QtGui.QApplication.translate("ServerWindow", "<font color=red>Not Connected</font>", None, QtGui.QApplication.UnicodeUTF8))
        self.pp_client_status.setText(QtGui.QApplication.translate("ServerWindow", "<font color=green>Connected</font>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("ServerWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">Client</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

