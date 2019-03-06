# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from sgtk.platform.qt import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(750, 900)
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
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.time_sum_label = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.time_sum_label.setFont(font)
        self.time_sum_label.setObjectName("time_sum_label")
        self.horizontalLayout_2.addWidget(self.time_sum_label)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.time_sum_today_label = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.time_sum_today_label.setFont(font)
        self.time_sum_today_label.setObjectName("time_sum_today_label")
        self.horizontalLayout_3.addWidget(self.time_sum_today_label)
        self.time_sum_week_label = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.time_sum_week_label.setFont(font)
        self.time_sum_week_label.setObjectName("time_sum_week_label")
        self.horizontalLayout_3.addWidget(self.time_sum_week_label)
        self.horizontalLayout_2.addLayout(self.horizontalLayout_3)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.tableLayout = QtGui.QVBoxLayout()
        self.tableLayout.setObjectName("tableLayout")
        self.gridLayout.addLayout(self.tableLayout, 3, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.timeTabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "The Current Sgtk Environment", None, QtGui.QApplication.UnicodeUTF8))
        self.time_sum_label.setText(QtGui.QApplication.translate("Dialog", "You have logged in", None, QtGui.QApplication.UnicodeUTF8))
        self.time_sum_today_label.setText(QtGui.QApplication.translate("Dialog", "0 hour today", None, QtGui.QApplication.UnicodeUTF8))
        self.time_sum_week_label.setText(QtGui.QApplication.translate("Dialog", "0 hour this week", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
