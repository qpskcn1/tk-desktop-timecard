# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'my_time_form.ui'
#
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from sgtk.platform.qt import QtCore, QtGui

class Ui_MyTimeForm(object):
    def setupUi(self, MyTimeForm):
        MyTimeForm.setObjectName("MyTimeForm")
        MyTimeForm.resize(349, 367)
        self.verticalLayout = QtGui.QVBoxLayout(MyTimeForm)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setContentsMargins(2, 6, 2, 2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(2, -1, 2, 1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.addnew_btn = QtGui.QPushButton(MyTimeForm)
        self.addnew_btn.setObjectName("addnew_btn")
        self.horizontalLayout.addWidget(self.addnew_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(1, -1, 1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(MyTimeForm)
        QtCore.QMetaObject.connectSlotsByName(MyTimeForm)

    def retranslateUi(self, MyTimeForm):
        MyTimeForm.setWindowTitle(QtGui.QApplication.translate("MyTimeForm", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.addnew_btn.setToolTip(QtGui.QApplication.translate("MyTimeForm", "<html><head/><body><p>Refresh (F5)</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.addnew_btn.setText(QtGui.QApplication.translate("MyTimeForm", "Add New Preset", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
