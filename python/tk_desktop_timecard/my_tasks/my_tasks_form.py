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
Implementation of the my tasks list widget consisting of a list view displaying the contents
of a Shotgun data model of my tasks, a text search and a filter control.
"""
import pickle

import sgtk
from sgtk.platform.qt import QtCore, QtGui
from ..ui.my_tasks_form import Ui_MyTasksForm
from .my_task_item_delegate import MyTaskItemDelegate
from ..util import monitor_qobject_lifetime, map_to_source, get_source_model
from ..entity_proxy_model import EntityProxyModel

from ..my_time.new_timelog_form import NewTimeLogForm

logger = sgtk.platform.get_logger(__name__)


class MyTasksForm(QtGui.QWidget):
    """
    My Tasks widget class
    """

    def __init__(self, tasks_model, allow_task_creation, parent):
        """
        Construction

        :param model:   The Shotgun Model this widget should connect to
        :param parent:  The parent QWidget for this control
        """
        QtGui.QWidget.__init__(self, parent)

        # set up the UI
        self._ui = Ui_MyTasksForm()
        self._ui.setupUi(self)

        search_label = "My Tasks"
        self._ui.search_ctrl.set_placeholder_text("Search %s" % search_label)
        self._ui.search_ctrl.setToolTip("Press enter to complete the search")

        # enable/hide the new task button if we have tasks and task creation is allowed:
        have_tasks = (tasks_model and tasks_model.get_entity_type() == "Task")
        if have_tasks and allow_task_creation:
            # enable and connect the new task button
            self._ui.new_task_btn.clicked.connect(self._on_new_task)
            self._ui.new_task_btn.setEnabled(False)
        # Sets an item delete to show a list of tiles for tasks instead of nodes in a tree.
        self._item_delegate = None
        if True:
            # create the item delegate - make sure we keep a reference to the delegate otherwise
            # things may crash later on!
            self._item_delegate = MyTaskItemDelegate(tasks_model.extra_display_fields, self._ui.task_tree)
            monitor_qobject_lifetime(self._item_delegate)
            self._ui.task_tree.setItemDelegate(self._item_delegate)
        filter_model = EntityProxyModel(self, ["content", {"entity": "name"}, "time_logs_sum"] + tasks_model.extra_display_fields)
        monitor_qobject_lifetime(filter_model, "%s entity filter model" % search_label)
        filter_model.setSourceModel(tasks_model)
        self._ui.task_tree.setModel(filter_model)
        # connect up the filter controls:
        self._ui.search_ctrl.search_changed.connect(self._on_search_changed)

        self.setAcceptDrops(True)

    # def shut_down(self):
    #     """
    #     Clean up as much as we can to help the gc once the widget is finished with.
    #     """
    #     signals_blocked = self.blockSignals(True)
    #     try:
    #         EntityTreeForm.shut_down(self)
    #         # detach and clean up the item delegate:
    #         self._ui.entity_tree.setItemDelegate(None)
    #         if self._item_delegate:
    #             self._item_delegate.setParent(None)
    #             self._item_delegate.deleteLater()
    #             self._item_delegate = None
    #     finally:
    #         self.blockSignals(signals_blocked)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-awevent"):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-awevent"):
            hoverIndex = self.indexAt(event.pos())
            self.selectionModel().select(hoverIndex, QtGui.QItemSelectionModel.SelectCurrent)
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        pass

    def dropEvent(self, event):
        data = event.mimeData()
        bstream = data.retrieveData("application/x-awevent", bytearray)
        selected = pickle.loads(bstream)
        logger.debug("Drop data: %s%s" % (selected, event.pos()))
        timelog_dl = NewTimeLogForm(selected)
        timelog_dl.exec_()
        event.accept()

    def _on_search_changed(self, search_text):
        """
        Slot triggered when the search text has been changed.

        :param search_text: The new search text
        """
        # reset the current selection without emitting any signals:
        prev_selected_item = self._reset_selection()
        try:
            # update the proxy filter search text:
            logger.debug("search %s in my tasks" % search_text)
            filter_reg_exp = QtCore.QRegExp(search_text, QtCore.Qt.CaseInsensitive, QtCore.QRegExp.FixedString)
            self._ui.entity_tree.model().setFilterRegExp(filter_reg_exp)
        finally:
            # and update the selection - this will restore the original selection if possible.
            self._update_selection(prev_selected_item)

    def _reset_selection(self):
        """
        Reset the current selection, returning the currently selected item if any.  This
        doesn't result in any signals being emitted by the current selection model.

        :returns:   The selected item before the selection was reset if any
        """
        prev_selected_item = self._get_selected_item()
        # reset the current selection without emitting any signals:
        self._ui.entity_tree.selectionModel().reset()
        self._update_ui()
        return prev_selected_item

    def _get_selected_item(self):
        """
        Get the currently selected item.

        :returns:   The currently selected model item if any
        """
        item = None
        indexes = self._ui.entity_tree.selectionModel().selectedIndexes()

        if len(indexes) == 1:
            item = self._item_from_index(indexes[0])
        return item

    def _item_from_index(self, idx):
        """
        Find the corresponding model item from the specified index.  This handles
        the indirection introduced by the filter model.

        :param idx: The model index to find the item for
        :returns:   The item in the model represented by the index
        """
        src_idx = map_to_source(idx)
        return src_idx.model().itemFromIndex(src_idx)

    def _update_ui(self):
        """
        Update the UI to reflect the current selection, etc.
        """
        enable_new_tasks = False

        selected_indexes = self._ui.task_tree.selectionModel().selectedIndexes()
        if len(selected_indexes) == 1:
            item = self._item_from_index(selected_indexes[0])
            tasks_model = get_source_model(selected_indexes[0].model())
            if item and tasks_model:
                entity = tasks_model.get_entity(item)
                if entity and entity["type"] != "Step":
                    if entity["type"] == "Task":
                        if entity.get("entity"):
                            enable_new_tasks = True
                    else:
                        enable_new_tasks = True

        self._ui.new_task_btn.setEnabled(enable_new_tasks)

    def _update_selection(self, prev_selected_item):
        """
        Update the selection to either the to-be-selected entity if set or the current item if known.  The
        current item is the item that was last selected but which may no longer be visible in the view due
        to filtering.  This allows it to be tracked so that the selection state is correctly restored when
        it becomes visible again.
        """
        tasks_model = get_source_model(self._ui.entity_tree.model())
        if not tasks_model:
            return

        # we want to make sure we don't emit any signals whilst we are
        # manipulating the selection:
        signals_blocked = self.blockSignals(True)
        try:
            # try to get the item to select:
            item = None
            if self._entity_to_select:
                # we know about an entity we should try to select:
                if tasks_model.get_entity_type() == self._entity_to_select["type"]:
                    item = tasks_model.item_from_entity(self._entity_to_select["type"], self._entity_to_select["id"])
            elif self._current_item_ref:
                # no item to select but we do know about a current item:
                item = self._current_item_ref()

            if item:
                idx = item.index()
                if isinstance(self._ui.entity_tree.model(), QtGui.QAbstractProxyModel):
                    # map the index to the proxy model:
                    idx = self._ui.entity_tree.model().mapFromSource(idx)

                if idx.isValid():
                    # make sure the item is expanded and visible in the tree:
                    self._ui.entity_tree.scrollTo(idx)

                    # select the item:
                    self._ui.entity_tree.selectionModel().setCurrentIndex(idx, QtGui.QItemSelectionModel.SelectCurrent)

        finally:
            self.blockSignals(signals_blocked)