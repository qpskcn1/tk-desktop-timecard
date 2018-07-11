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
import traceback
from datetime import date, timedelta

import sgtk
from sgtk.platform.qt import QtCore, QtGui
from ..ui.my_tasks_form import Ui_MyTasksForm
from .my_task_item_delegate import MyTaskItemDelegate
from ..util import monitor_qobject_lifetime, map_to_source, get_source_model
from ..entity_proxy_model import EntityProxyModel

from ..my_time.my_time_model import timelogEvent
from ..my_time.new_timelog_form import NewTimeLogForm

logger = sgtk.platform.get_logger(__name__)


class MyTasksTree(QtGui.QTreeView):
    '''
    a treeView whose items allow drops
    '''
    def __init__(self, parent=None):
        QtGui.QTreeView.__init__(self, parent)
        self.setAcceptDrops(True)
        self.parent = parent

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-timelogevent"):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        try:
            if event.mimeData().hasFormat("application/x-timelogevent"):
                # adjust y coordinate for task_widget
                # position = event.pos() - QtCore.QPoint(0, 70)
                hoverIndex = self.indexAt(event.pos())
                self.selectionModel().select(hoverIndex,
                                             QtGui.QItemSelectionModel.SelectCurrent)
                event.setDropAction(QtCore.Qt.MoveAction)
                event.accept()
            else:
                event.ignore()
        except Exception as e:
            logger.error("dragMoveEvent Exception: %s" % e)

    def dragLeaveEvent(self, event):
        pass

    def dropEvent(self, event):
        try:
            data = event.mimeData()
            bstream = data.retrieveData("application/x-timelogevent", bytearray)
            selected = pickle.loads(bstream)
            task = self.parent._get_selected_task()
            if task:
                logger.debug("Drop to task %s" % task)
                timelog_dl = NewTimeLogForm(selected, task, preset=True)
                timelog_dl.exec_()
                self.parent.parent._on_refresh_triggered()
            event.accept()
        except Exception as e:
            logger.error("dropEvent Exception: %s %s" % (e, traceback.format_exc()))


class MyTasksForm(QtGui.QWidget):
    """
    My Tasks widget class
    """

    def __init__(self, tasks_model, UI_filters_action, allow_task_creation, parent):
        """
        Construction

        :param model:   The Shotgun Model this widget should connect to
        :param UI_filters_action: previous selected filter
        :param parent:  The parent QWidget for this control
        """
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent

        # set up the UI
        self._ui = Ui_MyTasksForm()
        self._ui.setupUi(self)

        search_label = "My Tasks"
        self._ui.search_ctrl.set_placeholder_text("Search %s" % search_label)
        self._ui.search_ctrl.setToolTip("Press enter to complete the search")
        self.task_tree = MyTasksTree(self)
        self.task_tree.setObjectName("task_tree")
        self.task_tree.header().setVisible(False)
        # enable/hide the new task button if we have tasks and task creation
        # is allowed:
        have_tasks = (tasks_model and tasks_model.get_entity_type() == "Task")
        if have_tasks and allow_task_creation:
            # enable and connect the new task button
            self._ui.new_task_btn.clicked.connect(self._on_new_task)
            self._ui.new_task_btn.setEnabled(False)
        else:
            self._ui.new_task_btn.hide()
        # Sets an item delete to show a list of tiles for tasks instead of
        # nodes in a tree.
        self._item_delegate = None
        if True:
            # create the item delegate - make sure we keep a reference to the
            # delegate otherwise things may crash later on!
            self._item_delegate = MyTaskItemDelegate(
                tasks_model.extra_display_fields, self.task_tree)
            monitor_qobject_lifetime(self._item_delegate)
            self.task_tree.setItemDelegate(self._item_delegate)
        filter_model = EntityProxyModel(self, ["content", {"project": "name"},
                                        {"entity": "name"}] +
                                        tasks_model.extra_display_fields)
        monitor_qobject_lifetime(filter_model, "%s entity filter model"
                                 % search_label)
        filter_model.setSourceModel(tasks_model)
        self.task_tree.setModel(filter_model)
        self._ui.verticalLayout.addWidget(self.task_tree)
        # connect up the filter controls:
        self._ui.search_ctrl.search_changed.connect(self._on_search_changed)
        self._show_filters(UI_filters_action)
        # connect context menu
        self.task_tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.task_tree.customContextMenuRequested.connect(self.open_menu)

    def open_menu(self, position):
        """
        Context menu in my task tree

        :param position: where the time event is dropped
        """
        menu = QtGui.QMenu()
        addTimeAction = menu.addAction("New Time Log")
        action = menu.exec_(self.task_tree.viewport().mapToGlobal(position))
        if action == addTimeAction:
            task = self._get_selected_task()
            time = timelogEvent("Custom Time", date.today(), timedelta(-1))
            if task:
                timelog_dl = NewTimeLogForm(time, task)
                timelog_dl.exec_()
                logger.debug("New timelog submitted to Shotgun")
                if self.task_tree.model():
                    self.task_tree.model().async_refresh()

    def shut_down(self):
        """
        Clean up as much as we can to help the gc once the widget is
        finished with.
        """
        signals_blocked = self.blockSignals(True)
        try:
            # detach and clean up the item delegate:
            self.task_tree.setItemDelegate(None)
            if self._item_delegate:
                self._item_delegate.setParent(None)
                self._item_delegate.deleteLater()
                self._item_delegate = None

            # clear the selection:
            if self.task_tree.selectionModel():
                self.task_tree.selectionModel().clear()

            # detach the filter model from the view:
            view_model = self.task_tree.model()
            if view_model:
                self.task_tree.setModel(None)
                if isinstance(view_model, EntityProxyModel):
                    view_model.setSourceModel(None)
        finally:
            self.blockSignals(signals_blocked)

    # ------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------

    def _get_selected_task(self):
        """
        Get information of currently selected item

        :returns:   The selected task entity
        """
        selected_indexes = self.task_tree.selectionModel().selectedIndexes()
        if len(selected_indexes) == 1:
            item = self._item_from_index(selected_indexes[0])
            tasks_model = get_source_model(selected_indexes[0].model())
            if item and tasks_model:
                entity = tasks_model.get_entity(item)
                return entity
        return None

    def _show_filters(self, UI_filters_action):
        """
        Initialized filter menu and selected default action or previous action

        :param UI_filters_action: previous selected filter
        """
        filters_menu = QtGui.QMenu()
        filters_group = QtGui.QActionGroup(self)
        project_filter = QtGui.QAction('Current Project Tasks', filters_menu,
                                       checkable=True)
        project_filter.setData([['project', 'is', '{context.project}']])
        filters_group.addAction(project_filter)
        filters_menu.addAction(project_filter)
        all_filter = QtGui.QAction('All Tasks', filters_menu,
                                   checkable=True)
        all_filter.setData([])
        filters_group.addAction(all_filter)
        filters_menu.addAction(all_filter)
        facility_filter = QtGui.QAction('Facility Tasks', filters_menu,
                                        checkable=True)
        facility_filter.setData([['project.Project.name', 'is', 'Facility']])
        filters_group.addAction(facility_filter)
        filters_menu.addAction(facility_filter)
        if UI_filters_action:
            for filter_action in filters_menu.findChildren(QtGui.QAction):
                if filter_action.text() == UI_filters_action.text():
                    filter_action.setChecked(True)
        else:
            project_filter.setChecked(True)
        self._ui.filter_btn.setMenu(filters_menu)
        filters_group.triggered.connect(self._on_filter_changed)

    def _on_filter_changed(self, filter_action):
        """
        Slot triggered when the filter menu has been changed.

        :param UI_filters_action: previous selected filter
        """
        try:
            logger.debug("filter changed to {}".format(filter_action.text()))
            logger.debug("filter: {}".format(filter_action.data()))
            self.parent.createTasksForm(filter_action)
        except Exception as e:
            logger.error(e)

    def _on_search_changed(self, search_text):
        """
        Slot triggered when the search text has been changed.

        :param search_text: The new search text
        """
        # reset the current selection without emitting any signals:
        prev_selected_item = self._reset_selection()
        try:
            # update the proxy filter search text:
            filter_reg_exp = QtCore.QRegExp(search_text,
                                            QtCore.Qt.CaseInsensitive,
                                            QtCore.QRegExp.FixedString)
            self.task_tree.model().setFilterRegExp(filter_reg_exp)
        finally:
            # and update the selection - this will restore the original
            # selection if possible.
            self._update_selection(prev_selected_item)

    def _reset_selection(self):
        """
        Reset the current selection, returning the currently selected item
        if any.  Thisdoesn't result in any signals being emitted by the
        current selection model.

        :returns:   The selected item before the selection was reset if any
        """
        prev_selected_item = self._get_selected_item()
        # reset the current selection without emitting any signals:
        self.task_tree.selectionModel().reset()
        self._update_ui()
        return prev_selected_item

    def _get_selected_item(self):
        """
        Get the currently selected item.

        :returns:   The currently selected model item if any
        """
        item = None
        indexes = self.task_tree.selectionModel().selectedIndexes()

        if len(indexes) == 1:
            item = self._item_from_index(indexes[0])
        return item

    def _item_from_index(self, idx):
        """
        Find the corresponding model item from the specified index.  This
        handles the indirection introduced by the filter model.

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

        selected_indexes = self.task_tree.selectionModel().selectedIndexes()
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
        Update the selection to either the to-be-selected entity if set or
        the current item if known.  The current item is the item that was
        last selected but which may no longer be visible in the view due
        to filtering.  This allows it to be tracked so that the selection
        state is correctly restored when it becomes visible again.
        """
        tasks_model = get_source_model(self.task_tree.model())
        if not tasks_model:
            logger.debug("Can found tasks model")
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
                    item = tasks_model.item_from_entity(
                        self._entity_to_select["type"],
                        self._entity_to_select["id"])
            elif self._current_item_ref:
                # no item to select but we do know about a current item:
                item = self._current_item_ref()

            if item:
                idx = item.index()
                if isinstance(self.task_tree.model(), QtGui.QAbstractProxyModel):
                    # map the index to the proxy model:
                    idx = self.task_tree.model().mapFromSource(idx)

                if idx.isValid():
                    # make sure the item is expanded and visible in the tree:
                    self.task_tree.scrollTo(idx)

                    # select the item:
                    self.task_tree.selectionModel().setCurrentIndex(idx, QtGui.QItemSelectionModel.SelectCurrent)

        finally:
            self.blockSignals(signals_blocked)
