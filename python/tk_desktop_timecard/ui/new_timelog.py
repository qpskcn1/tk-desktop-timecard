# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_timelog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_NewTimeLogForm(object):
    def setupUi(self, NewTimeLogForm):
        if not NewTimeLogForm.objectName():
            NewTimeLogForm.setObjectName("NewTimeLogForm")
        NewTimeLogForm.resize(283, 381)
        self.gridLayout = QGridLayout(NewTimeLogForm)
        self.gridLayout.setObjectName("gridLayout")
        self.DescriptionLabel = QLabel(NewTimeLogForm)
        self.DescriptionLabel.setObjectName("DescriptionLabel")

        self.gridLayout.addWidget(self.DescriptionLabel, 8, 0, 1, 1)

        self.dateEdit = QDateEdit(NewTimeLogForm)
        self.dateEdit.setObjectName("dateEdit")

        self.gridLayout.addWidget(self.dateEdit, 5, 0, 1, 1)

        self.dataLabel = QLabel(NewTimeLogForm)
        self.dataLabel.setObjectName("dataLabel")

        self.gridLayout.addWidget(self.dataLabel, 4, 0, 1, 1)

        self.taskLabel = QLabel(NewTimeLogForm)
        self.taskLabel.setObjectName("taskLabel")

        self.gridLayout.addWidget(self.taskLabel, 2, 0, 1, 1)

        self.task_cbBox = QComboBox(NewTimeLogForm)
        self.task_cbBox.setObjectName("task_cbBox")

        self.gridLayout.addWidget(self.task_cbBox, 3, 0, 1, 1)

        self.timeLabel = QLabel(NewTimeLogForm)
        self.timeLabel.setObjectName("timeLabel")

        self.gridLayout.addWidget(self.timeLabel, 6, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(NewTimeLogForm)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 12, 0, 1, 1)

        self.logTimeLayout = QHBoxLayout()
        self.logTimeLayout.setObjectName("logTimeLayout")
        self.horizontalSlider = QSlider(NewTimeLogForm)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.setOrientation(Qt.Horizontal)

        self.logTimeLayout.addWidget(self.horizontalSlider)

        self.doubleSpinBox = QDoubleSpinBox(NewTimeLogForm)
        self.doubleSpinBox.setObjectName("doubleSpinBox")

        self.logTimeLayout.addWidget(self.doubleSpinBox)

        self.hourLabel = QLabel(NewTimeLogForm)
        self.hourLabel.setObjectName("hourLabel")

        self.logTimeLayout.addWidget(self.hourLabel)


        self.gridLayout.addLayout(self.logTimeLayout, 7, 0, 1, 1)

        self.textEdit = QTextEdit(NewTimeLogForm)
        self.textEdit.setObjectName("textEdit")

        self.gridLayout.addWidget(self.textEdit, 9, 0, 1, 1)

        self.projectLabel = QLabel(NewTimeLogForm)
        self.projectLabel.setObjectName("projectLabel")

        self.gridLayout.addWidget(self.projectLabel, 0, 0, 1, 1)

        self.project_cbBox = QComboBox(NewTimeLogForm)
        self.project_cbBox.setObjectName("project_cbBox")

        self.gridLayout.addWidget(self.project_cbBox, 1, 0, 1, 1)


        self.retranslateUi(NewTimeLogForm)
        self.buttonBox.accepted.connect(NewTimeLogForm.accept)
        self.buttonBox.rejected.connect(NewTimeLogForm.reject)

        QMetaObject.connectSlotsByName(NewTimeLogForm)
    # setupUi

    def retranslateUi(self, NewTimeLogForm):
        NewTimeLogForm.setWindowTitle(QCoreApplication.translate("NewTimeLogForm", "New Timelog", None))
        self.DescriptionLabel.setText(QCoreApplication.translate("NewTimeLogForm", "Description", None))
        self.dataLabel.setText(QCoreApplication.translate("NewTimeLogForm", "Date", None))
        self.taskLabel.setText(QCoreApplication.translate("NewTimeLogForm", "Task", None))
        self.timeLabel.setText(QCoreApplication.translate("NewTimeLogForm", "Log Time", None))
        self.hourLabel.setText(QCoreApplication.translate("NewTimeLogForm", "hrs", None))
        self.projectLabel.setText(QCoreApplication.translate("NewTimeLogForm", "Project", None))
    # retranslateUi

