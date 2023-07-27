# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'my_time_form.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from  . import resources_rc

class Ui_MyTimeForm(object):
    def setupUi(self, MyTimeForm):
        if not MyTimeForm.objectName():
            MyTimeForm.setObjectName("MyTimeForm")
        MyTimeForm.resize(349, 367)
        self.verticalLayout = QVBoxLayout(MyTimeForm)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(2, 6, 2, 2)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(2, -1, 2, 1)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.addnew_btn = QPushButton(MyTimeForm)
        self.addnew_btn.setObjectName("addnew_btn")

        self.horizontalLayout.addWidget(self.addnew_btn)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(1, -1, 1, -1)

        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(MyTimeForm)

        QMetaObject.connectSlotsByName(MyTimeForm)
    # setupUi

    def retranslateUi(self, MyTimeForm):
        MyTimeForm.setWindowTitle(QCoreApplication.translate("MyTimeForm", "Form", None))
#if QT_CONFIG(tooltip)
        self.addnew_btn.setToolTip(QCoreApplication.translate("MyTimeForm", "<html><head/><body><p>Refresh (F5)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.addnew_btn.setText(QCoreApplication.translate("MyTimeForm", "Add New Preset", None))
    # retranslateUi

