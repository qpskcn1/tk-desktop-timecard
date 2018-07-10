# Copyright (c) 2015 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

"""

"""
import sgtk
from sgtk.platform.qt import QtCore, QtGui

from ..ui.task_widget import Ui_TaskWidget
from ..util import set_widget_property

logger = sgtk.platform.get_logger(__name__)


class TaskWidget(QtGui.QWidget):
    """
    """
    def __init__(self, parent):
        """
        Construction
        """
        QtGui.QWidget.__init__(self, parent)

        # set up the UI
        self._ui = Ui_TaskWidget()
        self._ui.setupUi(self)
        self.setAcceptDrops(True)

    def set_selected(self, selected=True):
        """
        """
        set_widget_property(self._ui.background, "selected", selected,
                            refresh_style=True, refresh_children=True)

    def set_thumbnail(self, thumb):
        """
        """
        geom = self._ui.thumbnail.geometry()
        self._set_label_image(self._ui.thumbnail, thumb, geom.width(), geom.height())

    def set_entity(self, name, typ, icon):
        """
        """
        self._ui.entity_label.setText(name)
        if name is None or typ is None:
            self._ui.entity_label.setText("<font color=red>undefined</font>")
        if not icon:
            self._ui.entity_icon.hide()
        else:
            self._ui.entity_icon.show()
            self._set_label_image(self._ui.entity_icon, icon, 20, 20)

    def set_task(self, name, icon):
        """
        """
        self._ui.task_label.setText("%s" % name)
        if not icon:
            self._ui.task_icon.hide()
        else:
            self._ui.task_icon.show()
            self._set_label_image(self._ui.task_icon, icon, 20, 20)

    def set_timelog(self, time, icon):
        """
        """
        # self._ui.timelog_label.setText("%.1f hrs" % (time / 60.0))
        self._ui.timelog_label.setText("%.2f hrs" % (time / 60.0))
        if not icon:
            self._ui.timelog_icon.hide()
        else:
            self._ui.timelog_icon.show()
            self._set_label_image(self._ui.timelog_icon, icon, 20, 20)

    def set_project(self, name, icon):
        """
        """
        self._ui.project_label.setText(name)
        if not icon:
            self._ui.project_icon.hide()
        else:
            self._ui.project_icon.show()
            self._set_label_image(self._ui.project_icon, icon, 20, 20)

    def set_other(self, text):
        """
        """
        self._ui.other_label.setVisible(bool(text))
        self._ui.other_label.setText(text)

    def _set_label_image(self, label, image, w, h):
        """
        """
        if not image:
            # make sure it's cleared
            image = QtGui.QPixmap(":/res/thumb_empty.png")
            #return

        pm = image
        if isinstance(pm, QtGui.QIcon):
            # extract the largest pixmap from the icon:
            max_sz = max([(sz.width(), sz.height()) for sz in image.availableSizes()] or [(256, 256)])
            pm = image.pixmap(max_sz[0], max_sz[1])

        # and scale the pm if needed:
        scaled_pm = pm
        if pm.width() > w or pm.height() > h:
            scaled_pm = pm.scaled(w, h, QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
        label.setPixmap(scaled_pm)
