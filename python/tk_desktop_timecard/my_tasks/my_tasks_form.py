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
import weakref

import sgtk
from sgtk.platform.qt import QtCore, QtGui

from .my_task_item_delegate import MyTaskItemDelegate
from ..ui.my_tasks_form import Ui_MyTasksForm
from ..util import monitor_qobject_lifetime


class MyTasksForm(QtGui.QWidget):
    """
    My Tasks widget class
    """

    # Signal emitted when an entity is selected in the tree.
    entity_selected = QtCore.Signal(object, object)# selection details, breadcrumbs

    # Signal emitted when the 'New Task' button is clicked.
    create_new_task = QtCore.Signal(object, object)# entity, step

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

        if tasks_model:
            # Every time the model is refreshed with data from Shotgun, we'll need to re-expand nodes
            # that were expanded and reapply the current selection.
            tasks_model.data_refreshed.connect(self._on_data_refreshed)

            # if True:
            #     # create a filter proxy model between the source model and the task tree view:
            #     filter_model = EntityTreeProxyModel(self, ["content", {"entity": "name"}] + extra_fields)
            #     monitor_qobject_lifetime(filter_model, "%s entity filter model" % search_label)
            #     filter_model.setSourceModel(entity_model)
            #     self._ui.entity_tree.setModel(filter_model)

            #     # connect up the filter controls:
            #     self._ui.search_ctrl.search_changed.connect(self._on_search_changed)
            #     self._ui.my_tasks_cb.toggled.connect(self._on_my_tasks_only_toggled)
            # else:
            #     self._ui.task_tree.setModel(tasks_model)
        self._expand_root_rows()
        # connect to the selection model for the tree view:
        selection_model = self._ui.task_tree.selectionModel()
        if selection_model:
            selection_model.selectionChanged.connect(self._on_selection_changed)

        # Sets an item delete to show a list of tiles for tasks instead of nodes in a tree.
        self._item_delegate = None
        if True:
            # create the item delegate - make sure we keep a reference to the delegate otherwise
            # things may crash later on!
            self._item_delegate = MyTaskItemDelegate(tasks_model.extra_display_fields, self._ui.task_tree)
            monitor_qobject_lifetime(self._item_delegate)
            self._ui.task_tree.setItemDelegate(self._item_delegate)

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

    def select_entity(self, entity_type, entity_id):
        """
        Select the specified entity in the tree.  If the tree is still being populated then the selection
        will happen when an item representing the entity appears in the model.

        Note that this doesn't emit an entity_selected signal.

        :param entity_type: The type of the entity to select
        :param entity_id:   The id of the entity to select
        """
        # track the selected entity - this allows the entity to be selected when
        # it appears in the model even if the model hasn't been fully populated yet:
        self._entity_to_select = {"type": entity_type, "id": entity_id}

        # reset the current selection without emitting a signal:
        prev_selected_item = self._reset_selection()
        self._current_item_ref = None

        self._update_ui()

        # try to update the selection to reflect the change:
        self._update_selection(prev_selected_item)

    def _expand_root_rows(self):
        """
        Expand all root rows in the Tree if they have never been expanded
        """
        view_model = self._ui.task_tree.model()
        if not view_model:
            return

        # check if we should automatically expand the root level of the tree
        if not self._auto_expand_tree:
            return

        # disable widget paint updates whilst we update the expanded state of the tree:
        self._ui.task_tree.setUpdatesEnabled(False)
        # and block signals so that the expanded signal doesn't fire during item expansion!
        signals_blocked = self._ui.task_tree.blockSignals(True)
        try:
            for row in range(view_model.rowCount()):
                idx = view_model.index(row, 0)
                item = self._item_from_index(idx)
                if not item:
                    continue

                ref = weakref.ref(item)
                if ref in self._auto_expanded_root_items:
                    # we already processed this item
                    continue

                # expand item:
                self._ui.task_tree.expand(idx)
                self._auto_expanded_root_items.add(ref)
                self._expanded_items.add(ref)
        finally:
            self._ui.task_tree.blockSignals(signals_blocked)
            # re-enable updates to allow painting to continue
            self._ui.task_tree.setUpdatesEnabled(True)

    def _on_data_refreshed(self, modifications_made):
        """
        Slot triggered when new rows are inserted into the filter model.  When this happens
        we just make sure that any new root rows are expanded.

        :param parent_idx:  The parent model index of the rows that were inserted
        :param first:       The first row id inserted
        :param last:        The last row id inserted
        """
        if not modifications_made:
            return

        # expand any new root rows:
        self._expand_root_rows()

        # try to select the current entity from the new items in the model:
        prev_selected_item = self._reset_selection()
        self._update_selection(prev_selected_item)

    def _on_selection_changed(self, selected, deselected):
        """
        Slot triggered when the selection changes due to user action

        :param selected:    QItemSelection containing any newly selected indexes
        :param deselected:  QItemSelection containing any newly deselected indexes
        """
        # As the model is being reset, the selection is getting updated constantly,
        # so ignore these selection changes.
        if self._is_resetting_model:
            return

        # our tree is single-selection so extract the newly selected item from the
        # list of indexes:
        selection_details = {}
        breadcrumbs = []
        item = None
        selected_indexes = selected.indexes()
        if len(selected_indexes) == 1:
            selection_details = self._get_entity_details(selected_indexes[0])
            breadcrumbs = self._build_breadcrumb_trail(selected_indexes[0])
            item = self._item_from_index(selected_indexes[0])

        # update the UI
        self._update_ui()

        # keep track of the current item:
        self._current_item_ref = weakref.ref(item) if item else None

        if self._current_item_ref:
            # clear the entity-to-select as the current item now takes precedence
            self._entity_to_select = None

        # emit selection_changed signal:
        self.entity_selected.emit(selection_details, breadcrumbs)
