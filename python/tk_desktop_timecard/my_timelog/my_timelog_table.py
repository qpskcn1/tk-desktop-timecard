# Copyright (c) 2016 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import sgtk
import datetime
from sgtk.platform.qt import QtCore, QtGui
from ..framework_qtwidgets import shotgun_fields, shotgun_globals
from ..framework_qtwidgets import shotgun_model, task_manager, views
from .my_timelog_model import MyTimelogModel

logger = sgtk.platform.get_logger(__name__)


class MyTimelogTable(QtGui.QWidget):
    """
    Demonstrates how to override one of the default Shotgun field widgets.
    """

    def __init__(self, parent=None, bg_task_manager=None):
        """
        Initialize the demo widget.
        """

        # call the base class init
        super(MyTimelogTable, self).__init__(parent)

        # create a background task manager for each of our components to use
        self.parent = parent
        self._bg_task_manager = bg_task_manager

        # the fields manager is used to query which fields are supported
        # for display. it can also be used to find out which fields are
        # visible to the user and editable by the user. the fields manager
        # needs time to initialize itself. once that's done, the widgets can
        # begin to be populated.
        self._fields_manager = shotgun_fields.ShotgunFieldManager(
            parent=self,
            bg_task_manager=self._bg_task_manager
        )
        self._fields_manager.initialized.connect(self._populate_ui)
        self._fields_manager.initialize()

    def _populate_ui(self):
        """Populate the ui after the fields manager has been initialized."""

        # create a SG model to retrieve our data
        self._model = MyTimelogModel(self.parent, self._bg_task_manager)

        # and a table view to display our SG model
        table_view = views.ShotgunTableView(self._fields_manager, self)
        table_view.horizontalHeader().setStretchLastSection(True)

        # the filters to query
        filters = [
            ["user", "is", self.parent.user],
        ]
        # the fields to query
        fields = [
            "id",
            "project",
            "entity",
            "date",
            "duration",
            "description",
        ]
        order = [{'column': 'id', 'direction': 'desc'}]
        columns = [
            "project",
            "entity",
            "date",
            "duration",
            "description",
        ]
        # load the data into the model
        self._model._load_data(
            "TimeLog",
            filters=filters,
            fields=fields,
            hierarchy=["id"],
            order=order,
            limit=10,
            columns=columns,
            editable_columns=["date", "duration", "description"]
        )
        self._model._refresh_data()
        # now apply the model to the table view
        table_view.setModel(self._model)
        table_view.hideColumn(0)

        # info label
        # info_lbl = QtGui.QLabel(
        #     "Recent timelogs"
        # )
        # info_lbl.setWordWrap(True)

        # lay out the widgets
        layout = QtGui.QVBoxLayout(self)
        # layout.setSpacing(20)
        # layout.addWidget(info_lbl)
        layout.addWidget(table_view)

    def destroy(self):
        """
        Clean up the object when deleted.
        """
        self._bg_task_manager.shut_down()
        shotgun_globals.unregister_bg_task_manager(self._bg_task_manager)