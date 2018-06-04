# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created: Mon Jun 04 17:50:14 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from tank.platform.qt import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(723, 694)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.taskTabWidget = QtGui.QTabWidget(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.taskTabWidget.sizePolicy().hasHeightForWidth())
        self.taskTabWidget.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.taskTabWidget.setFont(font)
        self.taskTabWidget.setAcceptDrops(True)
        self.taskTabWidget.setObjectName("taskTabWidget")
        self.horizontalLayout.addWidget(self.taskTabWidget)
        self.timeTabWidget = QtGui.QTabWidget(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.timeTabWidget.setFont(font)
        self.timeTabWidget.setObjectName("timeTabWidget")
        self.horizontalLayout.addWidget(self.timeTabWidget)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 2)

        self.retranslateUi(Dialog)
        self.timeTabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "The Current Sgtk Environment", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
