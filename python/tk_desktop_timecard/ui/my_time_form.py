# -*- coding: utf-8 -*-



# Form implementation generated from reading ui file 'my_time_form.ui'

#

# Created: Wed Jul 18 15:35:43 2018

#      by: pyside-uic 0.2.15 running on PySide 1.2.4

#

# WARNING! All changes made in this file will be lost!



from tank.platform.qt import QtCore, QtGui



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

        self.horizontalLayout_3 = QtGui.QHBoxLayout()

        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(spacerItem1)

        self.sum_label = QtGui.QLabel(MyTimeForm)

        self.sum_label.setObjectName("sum_label")

        self.horizontalLayout_3.addWidget(self.sum_label)

        self.result_label = QtGui.QLabel(MyTimeForm)

        self.result_label.setObjectName("result_label")

        self.horizontalLayout_3.addWidget(self.result_label)

        self.verticalLayout.addLayout(self.horizontalLayout_3)



        self.retranslateUi(MyTimeForm)

        QtCore.QMetaObject.connectSlotsByName(MyTimeForm)



    def retranslateUi(self, MyTimeForm):

        MyTimeForm.setWindowTitle(QtGui.QApplication.translate("MyTimeForm", "Form", None, QtGui.QApplication.UnicodeUTF8))

        self.addnew_btn.setToolTip(QtGui.QApplication.translate("MyTimeForm", "<html><head/><body><p>Refresh (F5)</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

        self.addnew_btn.setText(QtGui.QApplication.translate("MyTimeForm", "Add New Preset", None, QtGui.QApplication.UnicodeUTF8))

        self.sum_label.setText(QtGui.QApplication.translate("MyTimeForm", "You have already logged in", None, QtGui.QApplication.UnicodeUTF8))

        self.result_label.setText(QtGui.QApplication.translate("MyTimeForm", "0 hrs today", None, QtGui.QApplication.UnicodeUTF8))



from . import resources_rc

