# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'task_widget.ui'
#
# Created: Wed Jun 06 12:12:21 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from tank.platform.qt import QtCore, QtGui

class Ui_TaskWidget(object):
    def setupUi(self, TaskWidget):
        TaskWidget.setObjectName("TaskWidget")
        TaskWidget.resize(383, 107)
        self.horizontalLayout = QtGui.QHBoxLayout(TaskWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.background = QtGui.QFrame(TaskWidget)
        self.background.setAcceptDrops(True)
        self.background.setStyleSheet("#background {\n"
"    border-bottom-style: solid;\n"
"    border-bottom-width: 1px;\n"
"    border-bottom-color: rgb(64,64,64);\n"
"}\n"
"\n"
"#background[selected=false] {\n"
"    background-color: rgb(0, 0, 0,0);\n"
"}\n"
"\n"
"#background[selected=true] {\n"
"    background-color: rgb(0, 178, 236);\n"
"}\n"
"\n"
"/*Font colour for all QLabels in form*/\n"
"#background[selected=false] QLabel {\n"
"}\n"
"\n"
"#background[selected=true] QLabel {\n"
"    color: rgb(255,255,255);\n"
"}")
        self.background.setFrameShape(QtGui.QFrame.NoFrame)
        self.background.setFrameShadow(QtGui.QFrame.Plain)
        self.background.setLineWidth(0)
        self.background.setProperty("selected", True)
        self.background.setObjectName("background")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.background)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.thumbnail = QtGui.QLabel(self.background)
        self.thumbnail.setMinimumSize(QtCore.QSize(100, 60))
        self.thumbnail.setMaximumSize(QtCore.QSize(100, 60))
        self.thumbnail.setStyleSheet("#thumbnail {\n"
"background-color: rgb(32,32, 32);\n"
"}")
        self.thumbnail.setText("")
        self.thumbnail.setObjectName("thumbnail")
        self.horizontalLayout_2.addWidget(self.thumbnail)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtGui.QSpacerItem(3, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_1 = QtGui.QHBoxLayout()
        self.horizontalLayout_1.setSpacing(6)
        self.horizontalLayout_1.setObjectName("horizontalLayout_1")
        self.project_icon = QtGui.QLabel(self.background)
        self.project_icon.setText("")
        self.project_icon.setObjectName("project_icon")
        self.horizontalLayout_1.addWidget(self.project_icon)
        self.project_label = QtGui.QLabel(self.background)
        self.project_label.setObjectName("project_label")
        self.horizontalLayout_1.addWidget(self.project_label)
        self.horizontalLayout_1.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.entity_icon = QtGui.QLabel(self.background)
        self.entity_icon.setText("")
        self.entity_icon.setObjectName("entity_icon")
        self.horizontalLayout_3.addWidget(self.entity_icon)
        self.entity_label = QtGui.QLabel(self.background)
        self.entity_label.setObjectName("entity_label")
        self.horizontalLayout_3.addWidget(self.entity_label)
        self.horizontalLayout_3.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.task_icon = QtGui.QLabel(self.background)
        self.task_icon.setText("")
        self.task_icon.setObjectName("task_icon")
        self.horizontalLayout_4.addWidget(self.task_icon)
        self.task_label = QtGui.QLabel(self.background)
        self.task_label.setObjectName("task_label")
        self.horizontalLayout_4.addWidget(self.task_label)
        self.horizontalLayout_4.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.timelog_icon = QtGui.QLabel(self.background)
        self.timelog_icon.setText("")
        self.timelog_icon.setObjectName("timelog_icon")
        self.horizontalLayout_5.addWidget(self.timelog_icon)
        self.timelog_label = QtGui.QLabel(self.background)
        self.timelog_label.setObjectName("timelog_label")
        self.horizontalLayout_5.addWidget(self.timelog_label)
        self.horizontalLayout_5.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.other_label = QtGui.QLabel(self.background)
        self.other_label.setObjectName("other_label")
        self.verticalLayout.addWidget(self.other_label)
        spacerItem1 = QtGui.QSpacerItem(3, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(6, 1)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout.addWidget(self.background)

        self.retranslateUi(TaskWidget)
        QtCore.QMetaObject.connectSlotsByName(TaskWidget)

    def retranslateUi(self, TaskWidget):
        TaskWidget.setWindowTitle(QtGui.QApplication.translate("TaskWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.project_label.setText(QtGui.QApplication.translate("TaskWidget", "Project", None, QtGui.QApplication.UnicodeUTF8))
        self.entity_label.setText(QtGui.QApplication.translate("TaskWidget", "Entity", None, QtGui.QApplication.UnicodeUTF8))
        self.task_label.setText(QtGui.QApplication.translate("TaskWidget", "Task", None, QtGui.QApplication.UnicodeUTF8))
        self.timelog_label.setText(QtGui.QApplication.translate("TaskWidget", "TimeLog", None, QtGui.QApplication.UnicodeUTF8))
        self.other_label.setText(QtGui.QApplication.translate("TaskWidget", "Other", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
