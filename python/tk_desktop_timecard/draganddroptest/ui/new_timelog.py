# -*- coding: utf-8 -*-



# Form implementation generated from reading ui file 'new_timelog.ui'

#

# Created: Tue Dec 12 16:03:33 2017

#      by: pyside-uic 0.2.15 running on PySide 1.2.4

#

# WARNING! All changes made in this file will be lost!



from PySide import QtCore, QtGui



class Ui_NewTimeLogForm(object):

    def setupUi(self, NewTimeLogForm):

        NewTimeLogForm.setObjectName("NewTimeLogForm")

        NewTimeLogForm.resize(283, 239)

        self.gridLayout = QtGui.QGridLayout(NewTimeLogForm)

        self.gridLayout.setObjectName("gridLayout")

        self.taskLabel = QtGui.QLabel(NewTimeLogForm)

        self.taskLabel.setObjectName("taskLabel")

        self.gridLayout.addWidget(self.taskLabel, 0, 0, 1, 1)

        self.dataLabel = QtGui.QLabel(NewTimeLogForm)

        self.dataLabel.setObjectName("dataLabel")

        self.gridLayout.addWidget(self.dataLabel, 2, 0, 1, 1)

        self.comboBox = QtGui.QComboBox(NewTimeLogForm)

        self.comboBox.setObjectName("comboBox")

        self.gridLayout.addWidget(self.comboBox, 1, 0, 1, 1)

        self.timeLabel = QtGui.QLabel(NewTimeLogForm)

        self.timeLabel.setObjectName("timeLabel")

        self.gridLayout.addWidget(self.timeLabel, 4, 0, 1, 1)

        self.dateEdit = QtGui.QDateEdit(NewTimeLogForm)

        self.dateEdit.setObjectName("dateEdit")

        self.gridLayout.addWidget(self.dateEdit, 3, 0, 1, 1)

        self.DescriptionLabel = QtGui.QLabel(NewTimeLogForm)

        self.DescriptionLabel.setObjectName("DescriptionLabel")

        self.gridLayout.addWidget(self.DescriptionLabel, 6, 0, 1, 1)

        self.textBrowser = QtGui.QTextBrowser(NewTimeLogForm)

        self.textBrowser.setOverwriteMode(True)

        self.textBrowser.setObjectName("textBrowser")

        self.gridLayout.addWidget(self.textBrowser, 7, 0, 1, 1)

        self.buttonBox = QtGui.QDialogButtonBox(NewTimeLogForm)

        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)

        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)

        self.buttonBox.setObjectName("buttonBox")

        self.gridLayout.addWidget(self.buttonBox, 10, 0, 1, 1)

        self.horizontalLayout_2 = QtGui.QHBoxLayout()

        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.horizontalSlider = QtGui.QSlider(NewTimeLogForm)

        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)

        self.horizontalSlider.setObjectName("horizontalSlider")

        self.horizontalLayout_2.addWidget(self.horizontalSlider)

        self.doubleSpinBox = QtGui.QDoubleSpinBox(NewTimeLogForm)

        self.doubleSpinBox.setObjectName("doubleSpinBox")

        self.horizontalLayout_2.addWidget(self.doubleSpinBox)

        self.gridLayout.addLayout(self.horizontalLayout_2, 5, 0, 1, 1)



        self.retranslateUi(NewTimeLogForm)

        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), NewTimeLogForm.accept)

        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), NewTimeLogForm.reject)

        QtCore.QMetaObject.connectSlotsByName(NewTimeLogForm)



    def retranslateUi(self, NewTimeLogForm):

        NewTimeLogForm.setWindowTitle(QtGui.QApplication.translate("NewTimeLogForm", "New Timelog", None, QtGui.QApplication.UnicodeUTF8))

        self.taskLabel.setText(QtGui.QApplication.translate("NewTimeLogForm", "Task", None, QtGui.QApplication.UnicodeUTF8))

        self.dataLabel.setText(QtGui.QApplication.translate("NewTimeLogForm", "Date", None, QtGui.QApplication.UnicodeUTF8))

        self.timeLabel.setText(QtGui.QApplication.translate("NewTimeLogForm", "Log Time", None, QtGui.QApplication.UnicodeUTF8))

        self.DescriptionLabel.setText(QtGui.QApplication.translate("NewTimeLogForm", "Description", None, QtGui.QApplication.UnicodeUTF8))



