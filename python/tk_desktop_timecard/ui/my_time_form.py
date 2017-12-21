# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'my_time_form.ui'
#
# Created: Thu Dec 21 15:32:16 2017
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
        self.random_cb = QtGui.QCheckBox(MyTimeForm)
        self.random_cb.setObjectName("random_cb")
        self.horizontalLayout.addWidget(self.random_cb)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.refresh_btn = QtGui.QPushButton(MyTimeForm)
        self.refresh_btn.setObjectName("refresh_btn")
        self.horizontalLayout.addWidget(self.refresh_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(1, -1, 1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.search_ctrl = SearchWidget(MyTimeForm)
        self.search_ctrl.setMinimumSize(QtCore.QSize(0, 20))
        self.search_ctrl.setStyleSheet("#search_ctrl {\n"
"background-color: rgb(255, 128, 0);\n"
"}")
        self.search_ctrl.setObjectName("search_ctrl")
        self.horizontalLayout_2.addWidget(self.search_ctrl)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(MyTimeForm)
        QtCore.QMetaObject.connectSlotsByName(MyTimeForm)

    def retranslateUi(self, MyTimeForm):
        MyTimeForm.setWindowTitle(QtGui.QApplication.translate("MyTimeForm", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.random_cb.setText(QtGui.QApplication.translate("MyTimeForm", "Some Filter", None, QtGui.QApplication.UnicodeUTF8))
        self.refresh_btn.setToolTip(QtGui.QApplication.translate("MyTimeForm", "<html><head/><body><p>Refresh (F5)</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.refresh_btn.setText(QtGui.QApplication.translate("MyTimeForm", "Refresh", None, QtGui.QApplication.UnicodeUTF8))

from ..framework_qtwidgets import SearchWidget
from . import resources_rc
