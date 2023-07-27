# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from  . import resources_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName("Dialog")
        Dialog.resize(750, 900)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.taskTabWidget = QTabWidget(Dialog)
        self.taskTabWidget.setObjectName("taskTabWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.taskTabWidget.sizePolicy().hasHeightForWidth())
        self.taskTabWidget.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.taskTabWidget.setFont(font)
        self.taskTabWidget.setAcceptDrops(True)

        self.horizontalLayout.addWidget(self.taskTabWidget)

        self.timeTabWidget = QTabWidget(Dialog)
        self.timeTabWidget.setObjectName("timeTabWidget")
        self.timeTabWidget.setFont(font)

        self.horizontalLayout.addWidget(self.timeTabWidget)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.time_sum_label = QLabel(Dialog)
        self.time_sum_label.setObjectName("time_sum_label")
        font1 = QFont()
        font1.setPointSize(16)
        self.time_sum_label.setFont(font1)

        self.horizontalLayout_2.addWidget(self.time_sum_label)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.time_sum_today_label = QLabel(Dialog)
        self.time_sum_today_label.setObjectName("time_sum_today_label")
        self.time_sum_today_label.setFont(font1)

        self.horizontalLayout_3.addWidget(self.time_sum_today_label)

        self.time_sum_week_label = QLabel(Dialog)
        self.time_sum_week_label.setObjectName("time_sum_week_label")
        self.time_sum_week_label.setFont(font1)

        self.horizontalLayout_3.addWidget(self.time_sum_week_label)


        self.horizontalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)

        self.tableLayout = QVBoxLayout()
        self.tableLayout.setObjectName("tableLayout")

        self.gridLayout.addLayout(self.tableLayout, 3, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.timeTabWidget.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", "The Current Sgtk Environment", None))
        self.time_sum_label.setText(QCoreApplication.translate("Dialog", "You have logged in", None))
        self.time_sum_today_label.setText(QCoreApplication.translate("Dialog", "0 hour today", None))
        self.time_sum_week_label.setText(QCoreApplication.translate("Dialog", "0 hour this week", None))
    # retranslateUi

