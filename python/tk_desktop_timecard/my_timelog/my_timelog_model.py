"""
Implementation of the 'My Timelog' data model
"""
from ..framework_qtwidgets import shotgun_model

ShotgunModel = shotgun_model.ShotgunModel


class MyTimelogModel(ShotgunModel):
    """
    Specialisation of Shotgun model that represents a single users timelogs
    """

    def __init__(self, parent, bg_task_manager):
        # create a SG model to retrieve our data
        ShotgunModel.__init__(
            self,
            parent=parent,
            download_thumbs=False,
            bg_load_thumbs=False,
            bg_task_manager=bg_task_manager,
        )

    def _before_data_processing(self, data):
        """
        Called after data has been retrieved from Shotgun but before any
        processing takes place
        Convert duration field from minutes to hours

        :param data: a shotgun dictionary, as returned by a CRUD SG API call.
        """
        # self._bundle.logger.debug("My Timelog Model {}".format(data))
        for timelog in data:
            if "duration" in timelog:
                timelog["duration"] = timelog["duration"] / 60.0
        return data

    def _get_additional_columns(self, primary_item, is_leaf, columns):
        """
        Called when an item is about to be inserted into the model, to get additional items
        to be included in the same row as the specified item. This provides an opportunity
        for subclasses to create one or more additional columns for each item in the model.
        Note that this method is always called before inserting an item, even when loading
        from the cache. Any data that is expensive to compute or query should be added
        to the ShotgunStandardItem in _populate_item, since column data is not cached.
        Also note that item population methods (_populate_item, _populate_thumbnail, etc)
        will not be called on the return columns.
        This method should return a list of QStandardItems, one for each additional column.
        The original ShotgunStandardItem is always the first item in each row and should
        NOT be included in the returned list. Any empty value returned by this method
        is guaranteed to be treated as an empty list (i.e. you may return None).
        This method is called after _finalize_item.
        :param primary_item: :class:`~PySide.QtGui.QStandardItem` that is about to be added to the model
        :param is_leaf: boolean that is True if the item is a leaf item
        :param columns: list of Shotgun field names requested as the columns from _load_data
        :returns: list of :class:`~PySide.QtGui.QStandardItem`
        """
        # default implementation will create items for the given fields from the item if it is a leaf
        # with the display role being the string value for the field and the actual data value in
        # SG_ASSOCIATED_FIELD_ROLE

        # this implementation add a special case for duration field
        # add hrs or hr after duration
        items = []
        try:
            if is_leaf and columns:
                data = shotgun_model.get_sg_data(primary_item)
                for column in columns:
                    # set the display role to the string representation of the value
                    column_item = shotgun_model.ShotgunStandardItem(
                        self._ShotgunModel__generate_display_name(column, data)
                    )
                    column_item.setEditable(
                        column in self._ShotgunModel__editable_fields
                    )
                    self._log_debug(column_item.__repr__())
                    # set associated field role to be the column value itself
                    value = data.get(column)
                    if column == "duration":
                        unit = "hrs"
                        if value == 1.0 or value == 0:
                            unit = "hr"
                        value = "{} {}".format(value, unit)
                    column_item.setData(
                        shotgun_model.sanitize_for_qt_model(value),
                        self.SG_ASSOCIATED_FIELD_ROLE,
                    )
                    items.append(column_item)
        except Exception as e:
            self._log_debug(e)
        return items
