# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'my_tasks_form.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ..framework_qtwidgets import SearchWidget


class Ui_MyTasksForm(object):
    def setupUi(self, MyTasksForm):
        if not MyTasksForm.objectName():
            MyTasksForm.setObjectName("MyTasksForm")
        MyTasksForm.resize(359, 541)
        self.verticalLayout = QVBoxLayout(MyTasksForm)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(2, 6, 2, 2)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(2, -1, 2, 1)
        self.filter_btn = QToolButton(MyTasksForm)
        self.filter_btn.setObjectName("filter_btn")
        self.filter_btn.setStyleSheet("")
        self.filter_btn.setPopupMode(QToolButton.MenuButtonPopup)
        self.filter_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.filter_btn.setAutoRaise(False)

        self.horizontalLayout.addWidget(self.filter_btn)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.new_task_btn = QPushButton(MyTasksForm)
        self.new_task_btn.setObjectName("new_task_btn")

        self.horizontalLayout.addWidget(self.new_task_btn)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(1, -1, 1, -1)
        self.search_ctrl = SearchWidget(MyTasksForm)
        self.search_ctrl.setObjectName("search_ctrl")
        self.search_ctrl.setMinimumSize(QSize(0, 20))
        self.search_ctrl.setStyleSheet("#search_ctrl {\n"
"background-color: rgb(255, 128, 0);\n"
"}")

        self.horizontalLayout_2.addWidget(self.search_ctrl)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(MyTasksForm)

        QMetaObject.connectSlotsByName(MyTasksForm)
    # setupUi

    def retranslateUi(self, MyTasksForm):
        MyTasksForm.setWindowTitle(QCoreApplication.translate("MyTasksForm", "Form", None))
        self.filter_btn.setText(QCoreApplication.translate("MyTasksForm", "Filter", None))
        self.new_task_btn.setText(QCoreApplication.translate("MyTasksForm", "+ New Task", None))
    # retranslateUi

