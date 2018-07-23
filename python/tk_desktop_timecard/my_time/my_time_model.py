import os
import csv
from math import ceil

import sgtk
from datetime import timedelta, date
from sgtk.platform.qt import QtCore, QtGui


logger = sgtk.platform.get_logger(__name__)


class timelogEvent(object):
    '''
    a custom data structure for shotgun time log
    '''
    def __init__(self, name, timestamp, duration):
        self.name = name
        self.timestamp = timestamp
        self.duration = duration

    def __repr__(self):
        return "{name: %s, date: %s, duration: %s}" % (self.name, self.timestamp, self.duration)

    def subtract_logged_time(self, logged_time):
        self.duration = self.duration - self.logged_time


class MyTimeModel(QtCore.QAbstractListModel):
    """
    Time Model used to display autotracked time or preset
    """
    def __init__(self, parent=None):
        super(MyTimeModel, self).__init__(parent)
        self.list = []
        preset_path = os.path.join(os.path.dirname(__file__), "preset.csv")
        with open(preset_path, 'rb') as preset:
            presets = csv.reader(preset, delimiter=',')
            for row in presets:
                row[1] = timedelta(seconds=int(row[1]))
                self.addRow(*row)

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.list)

    def data(self, index, role=QtCore.Qt.UserRole):
        if role == QtCore.Qt.DisplayRole:  # show just the name
            timelogevent = self.list[index.row()]
            duration = ceil(timelogevent.duration.total_seconds() / 36) / 100
            if duration < 0:
                duration = "any "
            return "{0} ({1}hrs)".format(timelogevent.name, duration)
        elif role == QtCore.Qt.UserRole:  # return the whole python object
            timelogevent = self.list[index.row()]
            return timelogevent
        else:
            return

    def addRow(self, name, duration):
        self.list.append(timelogEvent(name, date.today(), duration))
        self.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())

    def removeRow(self, position):
        event = self.data(position)
        logger.debug("Time left: {}".format(event.duration))
        if event.duration <= timedelta(0):
            self.list = self.list[:position] + self.list[position + 1:]
            self.reset()

    def async_refresh(self):
        QtGui.QApplication.processEvents()
        try:
            self.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())
        except Exception as e:
            logger.error(e)

    def destroy(self):
        pass
