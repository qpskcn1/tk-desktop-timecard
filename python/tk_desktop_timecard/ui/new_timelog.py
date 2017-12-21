# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_timelog.ui'
#
# Created: Thu Dec 21 14:57:07 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from tank.platform.qt import QtCore, QtGui

class Ui_NewTimeLogForm(object):
    def setupUi(self, NewTimeLogForm):
        NewTimeLogForm.setObjectName("NewTimeLogForm")
        NewTimeLogForm.resize(283, 381)
        self.gridLayout = QtGui.QGridLayout(NewTimeLogForm)
        self.gridLayout.setObjectName("gridLayout")
        self.DescriptionLabel = QtGui.QLabel(NewTimeLogForm)
        self.DescriptionLabel.setObjectName("DescriptionLabel")
        self.gridLayout.addWidget(self.DescriptionLabel, 8, 0, 1, 1)
        self.dateEdit = QtGui.QDateEdit(NewTimeLogForm)
        self.dateEdit.setObjectName("dateEdit")
        self.gridLayout.addWidget(self.dateEdit, 5, 0, 1, 1)
        self.dataLabel = QtGui.QLabel(NewTimeLogForm)
        self.dataLabel.setObjectName("dataLabel")
        self.gridLayout.addWidget(self.dataLabel, 4, 0, 1, 1)
        self.taskLabel = QtGui.QLabel(NewTimeLogForm)
        self.taskLabel.setObjectName("taskLabel")
        self.gridLayout.addWidget(self.taskLabel, 2, 0, 1, 1)
        self.task_cbBox = QtGui.QComboBox(NewTimeLogForm)
        self.task_cbBox.setObjectName("task_cbBox")
        self.gridLayout.addWidget(self.task_cbBox, 3, 0, 1, 1)
        self.timeLabel = QtGui.QLabel(NewTimeLogForm)
        self.timeLabel.setObjectName("timeLabel")
        self.gridLayout.addWidget(self.timeLabel, 6, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(NewTimeLogForm)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 12, 0, 1, 1)
        self.logTimeLayout = QtGui.QHBoxLayout()
        self.logTimeLayout.setObjectName("logTimeLayout")
        self.horizontalSlider = QtGui.QSlider(NewTimeLogForm)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.logTimeLayout.addWidget(self.horizontalSlider)
        self.doubleSpinBox = QtGui.QDoubleSpinBox(NewTimeLogForm)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.logTimeLayout.addWidget(self.doubleSpinBox)
        self.hourLabel = QtGui.QLabel(NewTimeLogForm)
        self.hourLabel.setObjectName("hourLabel")
        self.logTimeLayout.addWidget(self.hourLabel)
        self.gridLayout.addLayout(self.logTimeLayout, 7, 0, 1, 1)
        self.textEdit = QtGui.QTextEdit(NewTimeLogForm)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 9, 0, 1, 1)
        self.projectLabel = QtGui.QLabel(NewTimeLogForm)
        self.projectLabel.setObjectName("projectLabel")
        self.gridLayout.addWidget(self.projectLabel, 0, 0, 1, 1)
        self.project_cbBox = QtGui.QComboBox(NewTimeLogForm)
        self.project_cbBox.setObjectName("project_cbBox")
        self.gridLayout.addWidget(self.project_cbBox, 1, 0, 1, 1)

        self.retranslateUi(NewTimeLogForm)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), NewTimeLogForm.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), NewTimeLogForm.reject)
        QtCore.QMetaObject.connectSlotsByName(NewTimeLogForm)

    def retranslateUi(self, NewTimeLogForm):
        NewTimeLogForm.setWindowTitle(QtGui.QApplication.translate("NewTimeLogForm", "New Timelog", None, QtGui.QApplication.UnicodeUTF8))
        self.DescriptionLabel.setText(QtGui.QApplication.translate("NewTimeLogForm", "Description", None, QtGui.QApplication.UnicodeUTF8))
        self.dataLabel.setText(QtGui.QApplication.translate("NewTimeLogForm", "Date", None, QtGui.QApplication.UnicodeUTF8))
        self.taskLabel.setText(QtGui.QApplication.translate("NewTimeLogForm", "Task", None, QtGui.QApplication.UnicodeUTF8))
        self.timeLabel.setText(QtGui.QApplication.translate("NewTimeLogForm", "Log Time", None, QtGui.QApplication.UnicodeUTF8))
        self.hourLabel.setText(QtGui.QApplication.translate("NewTimeLogForm", "hrs", None, QtGui.QApplication.UnicodeUTF8))
        self.projectLabel.setText(QtGui.QApplication.translate("NewTimeLogForm", "Project", None, QtGui.QApplication.UnicodeUTF8))

