# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'task_widget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from  . import resources_rc

class Ui_TaskWidget(object):
    def setupUi(self, TaskWidget):
        if not TaskWidget.objectName():
            TaskWidget.setObjectName("TaskWidget")
        TaskWidget.resize(383, 107)
        self.horizontalLayout = QHBoxLayout(TaskWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.background = QFrame(TaskWidget)
        self.background.setObjectName("background")
        self.background.setAcceptDrops(True)
        self.background.setStyleSheet("#background {\n"
"	border-bottom-style: solid;\n"
"	border-bottom-width: 1px;\n"
"	border-bottom-color: rgb(64,64,64);\n"
"}\n"
"\n"
"#background[selected=false] {\n"
"	background-color: rgb(0, 0, 0,0);\n"
"}\n"
"\n"
"#background[selected=true] {\n"
"	background-color: rgb(0, 178, 236);\n"
"}\n"
"\n"
"/*Font colour for all QLabels in form*/\n"
"#background[selected=false] QLabel {\n"
"}\n"
"\n"
"#background[selected=true] QLabel {\n"
"	color: rgb(255,255,255);\n"
"}")
        self.background.setFrameShape(QFrame.NoFrame)
        self.background.setFrameShadow(QFrame.Plain)
        self.background.setLineWidth(0)
        self.background.setProperty("selected", True)
        self.horizontalLayout_2 = QHBoxLayout(self.background)
#ifndef Q_OS_MAC
        self.horizontalLayout_2.setSpacing(6)
#endif
        self.horizontalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.thumbnail = QLabel(self.background)
        self.thumbnail.setObjectName("thumbnail")
        self.thumbnail.setMinimumSize(QSize(100, 60))
        self.thumbnail.setMaximumSize(QSize(100, 60))
        self.thumbnail.setStyleSheet("#thumbnail {\n"
"background-color: rgb(32,32, 32);\n"
"}")

        self.horizontalLayout_2.addWidget(self.thumbnail)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalSpacer_2 = QSpacerItem(3, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.horizontalLayout_1 = QHBoxLayout()
        self.horizontalLayout_1.setSpacing(6)
        self.horizontalLayout_1.setObjectName("horizontalLayout_1")
        self.project_icon = QLabel(self.background)
        self.project_icon.setObjectName("project_icon")

        self.horizontalLayout_1.addWidget(self.project_icon)

        self.project_label = QLabel(self.background)
        self.project_label.setObjectName("project_label")

        self.horizontalLayout_1.addWidget(self.project_label)

        self.horizontalLayout_1.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.entity_icon = QLabel(self.background)
        self.entity_icon.setObjectName("entity_icon")

        self.horizontalLayout_3.addWidget(self.entity_icon)

        self.entity_label = QLabel(self.background)
        self.entity_label.setObjectName("entity_label")

        self.horizontalLayout_3.addWidget(self.entity_label)

        self.horizontalLayout_3.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.task_icon = QLabel(self.background)
        self.task_icon.setObjectName("task_icon")

        self.horizontalLayout_4.addWidget(self.task_icon)

        self.task_label = QLabel(self.background)
        self.task_label.setObjectName("task_label")

        self.horizontalLayout_4.addWidget(self.task_label)

        self.horizontalLayout_4.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.timelog_icon = QLabel(self.background)
        self.timelog_icon.setObjectName("timelog_icon")

        self.horizontalLayout_5.addWidget(self.timelog_icon)

        self.timelog_label = QLabel(self.background)
        self.timelog_label.setObjectName("timelog_label")

        self.horizontalLayout_5.addWidget(self.timelog_label)

        self.horizontalLayout_5.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.other_label = QLabel(self.background)
        self.other_label.setObjectName("other_label")

        self.verticalLayout.addWidget(self.other_label)

        self.verticalSpacer = QSpacerItem(3, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(6, 1)

        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.horizontalLayout_2.setStretch(1, 1)

        self.horizontalLayout.addWidget(self.background)


        self.retranslateUi(TaskWidget)

        QMetaObject.connectSlotsByName(TaskWidget)
    # setupUi

    def retranslateUi(self, TaskWidget):
        TaskWidget.setWindowTitle(QCoreApplication.translate("TaskWidget", "Form", None))
        self.thumbnail.setText("")
        self.project_icon.setText("")
        self.project_label.setText(QCoreApplication.translate("TaskWidget", "Project", None))
        self.entity_icon.setText("")
        self.entity_label.setText(QCoreApplication.translate("TaskWidget", "Entity", None))
        self.task_icon.setText("")
        self.task_label.setText(QCoreApplication.translate("TaskWidget", "Task", None))
        self.timelog_icon.setText("")
        self.timelog_label.setText(QCoreApplication.translate("TaskWidget", "TimeLog", None))
        self.other_label.setText(QCoreApplication.translate("TaskWidget", "Other", None))
    # retranslateUi

